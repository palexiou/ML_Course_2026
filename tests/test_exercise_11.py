"""Check both classifier paths and masked token windows without downloads."""

from contextlib import redirect_stdout
from io import StringIO
import json
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss, roc_auc_score
from sklearn.preprocessing import StandardScaler
from transformers import AutoModelForMaskedLM, AutoTokenizer, BatchEncoding


class ExampleTokenizer:
    """Use single bases so expected pooled vectors are easy to calculate."""

    all_special_ids = [0, 1]

    def __call__(self, sequences, **kwargs):
        if isinstance(sequences, str):
            sequences = [sequences]
        ids = [[1] + ["ACGTN".index(base) + 2 for base in seq] for seq in sequences]
        length = max(map(len, ids))
        padded = [row + [0] * (length - len(row)) for row in ids]
        inputs = torch.tensor(padded)
        result = BatchEncoding({"input_ids": inputs, "attention_mask": (inputs != 0).long()})
        return result

    def convert_ids_to_tokens(self, ids):
        return [
            ["<pad>", "<cls>", "A", "C", "G", "T", "N"][i] for i in ids
        ]


class ExampleTransformer(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.config = SimpleNamespace(hidden_size=4)
        ids = torch.arange(7, dtype=torch.float32)
        vectors = torch.stack([ids, ids.square(), ids.sin(), ids.cos()], dim=1)
        vectors[:2] = 1000  # Padding and CLS must not enter the average.
        self.embedding = torch.nn.Embedding.from_pretrained(vectors, freeze=False)

    def forward(self, input_ids, attention_mask, output_hidden_states):
        assert not self.training
        assert not torch.is_grad_enabled()
        assert output_hidden_states
        return SimpleNamespace(hidden_states=(self.embedding(input_ids),))


class Exercise11Tests(unittest.TestCase):
    def test_pooling_and_classifier_preserve_training_boundaries(self):
        path = Path(__file__).resolve().parents[1] / "exercise_11.ipynb"
        notebook = json.loads(path.read_text())
        rng = np.random.default_rng(7)
        sequences = ["".join(row) for row in rng.choice(list("ACGT"), size=(140, 251))]
        official_train = pd.DataFrame({"seq": sequences[:100], "label": [0] * 50 + [1] * 50})
        official_test = pd.DataFrame({"seq": sequences[100:], "label": [0] * 20 + [1] * 20})
        official_test.loc[0, "seq"] = "N" + official_test.loc[0, "seq"][1:]
        transformer = ExampleTransformer()
        original_weights = transformer.embedding.weight.detach().clone()
        namespace = {"__name__": "__main__"}
        self.addCleanup(torch.set_num_threads, torch.get_num_threads())
        scaler_fit = StandardScaler.fit
        classifier_fit = LogisticRegression.fit
        adam_step = torch.optim.Adam.step
        fits = []
        updates = []

        def fit_scaler(scaler, values, labels=None, **kwargs):
            np.testing.assert_array_equal(values, namespace["x_train"])
            fits.append("scaler")
            return scaler_fit(scaler, values, labels, **kwargs)

        def fit_classifier(classifier, values, labels, **kwargs):
            np.testing.assert_array_equal(labels, namespace["y_train"])
            self.assertEqual(len(values), len(namespace["train_data"]))
            fits.append("classifier")
            return classifier_fit(classifier, values, labels, **kwargs)

        def update_cnn(optimizer, *args, **kwargs):
            parameters = [p for group in optimizer.param_groups for p in group['params']]
            self.assertEqual({id(p) for p in parameters}, {id(p) for p in namespace['cnn'].parameters()})
            self.assertTrue(all(p.grad is not None and torch.isfinite(p.grad).all() for p in parameters))
            self.assertGreater(namespace['cnn'].convolution.weight.grad.norm().item(), 0)
            updates.append(1)
            return adam_step(optimizer, *args, **kwargs)

        def check_cnn_inputs(model, inputs):
            if model.training:
                for row in inputs[0].detach().cpu().numpy():
                    self.assertIn(row.tobytes(), training_rows)
            else:
                self.assertFalse(torch.is_grad_enabled())

        with redirect_stdout(StringIO()), \
                patch.object(pd, "read_parquet", side_effect=[official_train.copy(), official_test.copy()]) as download, \
                patch.object(AutoTokenizer, "from_pretrained", return_value=ExampleTokenizer()) as tokenizer_load, \
                patch.object(AutoModelForMaskedLM, "from_pretrained", return_value=transformer) as model_load, \
                patch.object(StandardScaler, "fit", fit_scaler), \
                patch.object(LogisticRegression, "fit", fit_classifier), \
                patch.object(torch.optim.Adam, "step", update_cnn), \
                patch.object(plt, "show", side_effect=lambda: plt.close("all")):
            for cell in notebook["cells"]:
                if cell["cell_type"] != "code" or cell["id"] == "install":
                    continue
                if cell["id"] == "test-evaluation":
                    self.assertEqual(download.call_count, 1)
                    for name in ("test_data", "x_test", "test_tokens", "test_loader", "y_test", "test_probabilities"):
                        self.assertNotIn(name, namespace)
                exec(compile("".join(cell["source"]), str(path), "exec"), namespace)
                if cell["id"] == "settings":
                    namespace["batch_size"] = 13
                    namespace["cnn_batch_size"] = 16
                    namespace["max_epochs"] = 3
                    namespace["device"] = torch.device("cpu")
                if cell["id"] == "build-cnn":
                    initial_cnn_state = {name: value.clone() for name, value in namespace["cnn"].state_dict().items()}
                    namespace["cnn"].register_forward_pre_hook(check_cnn_inputs)
                if cell["id"] == "cnn-batches":
                    training_rows = {row.numpy().tobytes() for row in namespace["train_tokens"].float()}
            # Different lengths force padding; N is a DNA token, not an excluded special token.
            pooled, tokens, mask = namespace["embed_sequences"](["AC", "N", "ACGTN"])

        for row, sequence in zip(pooled, ["AC", "N", "ACGTN"]):
            indices = ["ACGTN".index(base) + 2 for base in sequence]
            expected = original_weights[indices].mean(dim=0).numpy()
            np.testing.assert_allclose(row, expected, atol=1e-6)
        self.assertEqual(tokens.dtype, torch.float16)
        self.assertEqual(mask.sum(dim=1).tolist(), [2, 1, 5])
        self.assertTrue((tokens[~mask] == 0).all())
        expected_validation = official_train.groupby("label").sample(frac=0.20, random_state=42)
        pd.testing.assert_frame_equal(
            namespace["validation_data"], expected_validation.rename(columns={"seq": "sequence"})
        )
        pd.testing.assert_frame_equal(
            namespace["train_data"], official_train.drop(expected_validation.index).rename(columns={"seq": "sequence"})
        )
        pd.testing.assert_frame_equal(namespace["test_data"], official_test.rename(columns={"seq": "sequence"}))
        self.assertEqual(download.call_count, 2)
        self.assertEqual(fits, ["scaler", "classifier"])
        np.testing.assert_allclose(namespace["classifier"][0].mean_, namespace["x_train"].mean(axis=0), rtol=1e-6)
        for loader in (tokenizer_load, model_load):
            self.assertEqual(loader.call_args.kwargs["revision"], namespace["model_revision"])
        self.assertFalse(any(p.requires_grad for p in transformer.parameters()))
        torch.testing.assert_close(transformer.embedding.weight, original_weights, rtol=0, atol=0)
        self.assertEqual(len(updates), 3 * len(namespace['train_loader']))
        self.assertEqual(namespace['best_epoch'], int(np.argmin(namespace['validation_losses'])) + 1)
        for name, value in namespace['cnn'].state_dict().items():
            torch.testing.assert_close(value, namespace['best_state'][name], rtol=0, atol=0)
        self.assertFalse(torch.equal(initial_cnn_state['convolution.weight'], namespace['cnn'].convolution.weight))
        self.assertFalse(torch.equal(initial_cnn_state['output.weight'], namespace['cnn'].output.weight))
        self.assertAlmostEqual(
            namespace['validation_results'].loc['Token CNN', 'log_loss'], min(namespace['validation_losses']), places=5
        )
        for split in ("train", "validation", "test"):
            data = namespace[f"{split}_data"]
            expected = torch.stack([
                original_weights[["ACGTN".index(base) + 2 for base in sequence]].mean(dim=0)
                for sequence in data["sequence"]
            ]).numpy()
            np.testing.assert_allclose(namespace[f"x_{split}"], expected, atol=1e-6)
        for split in ("validation", "test"):
            results = namespace[f"{split}_results"]
            self.assertEqual(results.shape, (2, 8))
            self.assertTrue(np.isfinite(results.to_numpy()).all())
            for name, probabilities in namespace[f"{split}_probabilities"].items():
                labels = namespace[f"y_{split}"]
                self.assertAlmostEqual(results.loc[name, 'roc_auc'], roc_auc_score(labels, probabilities))
                self.assertAlmostEqual(results.loc[name, 'log_loss'], log_loss(labels, probabilities))

    def test_cnn_excludes_complete_windows_that_touch_special_tokens_or_padding(self):
        notebook = json.loads((Path(__file__).resolve().parents[1] / 'exercise_11.ipynb').read_text())
        namespace = {'__name__': '__main__'}
        self.addCleanup(torch.set_num_threads, torch.get_num_threads())
        for cell in notebook['cells']:
            if cell['id'] == 'settings':
                exec(''.join(cell['source']), namespace)
                namespace['device'] = torch.device('cpu')
                namespace['foundation_model'] = ExampleTransformer()
            if cell['id'] == 'build-cnn':
                exec(''.join(cell['source']), namespace)
        cnn = namespace['cnn'].eval()
        self.assertEqual(sum(isinstance(layer, torch.nn.Conv1d) for layer in cnn.modules()), 1)
        tokens = torch.randn(1, 6, 4)
        mask = torch.ones(1, 6, dtype=torch.bool)
        # Large excluded vectors would dominate unmasked or partly masked windows.
        padded = torch.cat([torch.full((1, 1, 4), 10000.0), tokens, torch.full((1, 4, 4), 10000.0)], dim=1)
        padded_mask = torch.cat([torch.zeros(1, 1, dtype=torch.bool), mask, torch.zeros(1, 4, dtype=torch.bool)], dim=1)
        padded.requires_grad_()
        prediction = cnn(padded, padded_mask)
        torch.testing.assert_close(prediction, cnn(tokens, mask))
        prediction.sum().backward()
        self.assertTrue((padded.grad[~padded_mask] == 0).all())

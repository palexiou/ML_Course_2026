"""Exercise all six real classifier types on small data without network access."""

from contextlib import redirect_stdout
from io import StringIO
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss, roc_auc_score
from sklearn.preprocessing import StandardScaler
from transformers import AutoTokenizer, AutoModelForMaskedLM
from xgboost import XGBClassifier

from test_exercise_11 import ExampleTokenizer, ExampleTransformer


class Exercise12Tests(unittest.TestCase):
    def test_six_models_share_rows_and_never_fit_on_test(self):
        path = Path(__file__).resolve().parents[1] / 'exercise_12.ipynb'
        notebook = json.loads(path.read_text())
        rng = np.random.default_rng(7)
        sequences = [''.join(row) for row in rng.choice(list('ACGT'), size=(140, 251))]
        official_train = pd.DataFrame({'seq': sequences[:100], 'label': [0] * 50 + [1] * 50})
        official_test = pd.DataFrame({'seq': sequences[100:], 'label': [0] * 20 + [1] * 20})
        official_test.loc[0, 'seq'] = 'N' + official_test.loc[0, 'seq'][1:]
        transformer = ExampleTransformer()
        initial_transformer = transformer.embedding.weight.detach().clone()
        ns = {'__name__': '__main__'}
        self.addCleanup(torch.set_num_threads, torch.get_num_threads())
        vocabulary_rows, fitted_models, updated_models = [], [], []
        vocabulary_fit = CountVectorizer.fit_transform
        scaler_fit = StandardScaler.fit
        adam_step = torch.optim.Adam.step
        convolution_forward = torch.nn.Conv1d.forward
        initial_networks = {}

        def fit_vocabulary(vectorizer, sequences, *args, **kwargs):
            vocabulary_rows.append(tuple(sequences))
            return vocabulary_fit(vectorizer, sequences, *args, **kwargs)

        def fit_scaler(scaler, values, labels=None, **kwargs):
            np.testing.assert_array_equal(values, ns['train_means'])
            return scaler_fit(scaler, values, labels, **kwargs)

        def record_fit(original, kind):
            def fit(model, values, labels, *args, **kwargs):
                np.testing.assert_array_equal(labels, ns['y_train'])
                self.assertEqual(len(labels), len(ns['train_data']))
                fitted_models.append(kind)
                if kind == 'XGBoost':
                    self.assertIsInstance(values, np.ndarray)
                    np.testing.assert_array_equal(values, ns['train_counts'].toarray())
                    np.testing.assert_array_equal(kwargs['eval_set'][0][0], ns['validation_counts'].toarray())
                    np.testing.assert_array_equal(kwargs['eval_set'][0][1], ns['y_validation'])
                return original(model, values, labels, *args, **kwargs)
            return fit

        def short_xgboost(**kwargs):
            kwargs.update(n_estimators=8, early_stopping_rounds=3, n_jobs=1)
            return XGBClassifier(**kwargs)

        def short_forest(**kwargs):
            kwargs.update(n_estimators=5, n_jobs=1)
            return RandomForestClassifier(**kwargs)

        def update_network(optimizer, *args, **kwargs):
            parameter_ids = {id(p) for group in optimizer.param_groups for p in group['params']}
            matching = [(name, model) for name, model in ns['models'].items()
                        if isinstance(model, torch.nn.Module) and {id(p) for p in model.parameters()} == parameter_ids]
            self.assertEqual(len(matching), 1)
            name, model = matching[0]
            if name not in initial_networks:
                initial_networks[name] = {key: value.clone() for key, value in model.state_dict().items()}
            for parameter in model.parameters():
                self.assertIsNotNone(parameter.grad)
                self.assertTrue(torch.isfinite(parameter.grad).all())
            for layer in model.modules():
                if isinstance(layer, torch.nn.Conv1d):
                    self.assertGreater(layer.weight.grad.norm().item(), 0)
            updated_models.append(name)
            return adam_step(optimizer, *args, **kwargs)

        def check_convolution_inputs(layer, inputs):
            if layer.training and layer.kernel_size in [(15,), (3,)]:
                rows = ns['train_onehot'] if layer.kernel_size == (15,) else ns['train_tokens'].float().transpose(1, 2)
                allowed = {row.contiguous().numpy().tobytes() for row in rows}
                for row in inputs.detach().cpu():
                    self.assertIn(row.contiguous().numpy().tobytes(), allowed)
            if not layer.training:
                self.assertFalse(torch.is_grad_enabled())
            return convolution_forward(layer, inputs)

        with TemporaryDirectory() as directory, redirect_stdout(StringIO()), \
                patch.object(pd, 'read_parquet', side_effect=[official_train.copy(), official_test.copy()]) as download, \
                patch.object(AutoTokenizer, 'from_pretrained', return_value=ExampleTokenizer()), \
                patch.object(AutoModelForMaskedLM, 'from_pretrained', return_value=transformer), \
                patch.object(CountVectorizer, 'fit_transform', fit_vocabulary), \
                patch.object(StandardScaler, 'fit', fit_scaler), \
                patch.object(LogisticRegression, 'fit', record_fit(LogisticRegression.fit, 'logistic')), \
                patch.object(RandomForestClassifier, 'fit', record_fit(RandomForestClassifier.fit, 'forest')), \
                patch.object(XGBClassifier, 'fit', record_fit(XGBClassifier.fit, 'XGBoost')), \
                patch('sklearn.ensemble.RandomForestClassifier', short_forest), \
                patch('xgboost.XGBClassifier', short_xgboost), \
                patch.object(torch.optim.Adam, 'step', update_network), \
                patch.object(torch.nn.Conv1d, 'forward', check_convolution_inputs), \
                patch.object(plt, 'show', side_effect=lambda: plt.close('all')):
            for cell in notebook['cells']:
                if cell['cell_type'] != 'code' or cell['id'] == 'install':
                    continue
                if cell['id'] == 'test-evaluation':
                    self.assertEqual(download.call_count, 1)
                    self.assertEqual(len(ns['models']), 6)
                    self.assertIn(ns['validation_choice'], ns['models'])
                    for name in ['test_data', 'y_test', 'test_counts', 'test_tokens', 'test_probabilities']:
                        self.assertNotIn(name, ns)
                exec(compile(''.join(cell['source']), str(path) + ':' + cell['id'], 'exec'), ns)
                if cell['id'] == 'settings':
                    ns.update(max_epochs=2, batch_size=13, cnn_batch_size=16, bootstrap_repeats=8,
                              n_jobs=1, device=torch.device('cpu'), output_dir=Path(directory))
            self.assertEqual(download.call_count, 2)
            expected_validation = official_train.groupby('label').sample(frac=0.20, random_state=42)
            pd.testing.assert_frame_equal(ns['validation_data'], expected_validation.rename(columns={'seq': 'sequence'}))
            pd.testing.assert_frame_equal(ns['train_data'], official_train.drop(expected_validation.index).rename(columns={'seq': 'sequence'}))
            pd.testing.assert_frame_equal(ns['test_data'], official_test.rename(columns={'seq': 'sequence'}))
            self.assertEqual(vocabulary_rows, [tuple(ns['train_data']['sequence'])])
            self.assertEqual(fitted_models, ['logistic', 'forest', 'XGBoost', 'logistic'])
            self.assertFalse(any(p.requires_grad for p in transformer.parameters()))
            torch.testing.assert_close(transformer.embedding.weight, initial_transformer, rtol=0, atol=0)
            for name in ['Sequence CNN', 'Transformer + CNN']:
                self.assertEqual(updated_models.count(name), 2 * len(ns['raw_train_loader']))
                self.assertFalse(ns['models'][name].training)
                self.assertEqual(ns['selected_steps'][name], int(ns['histories'][name]['validation_loss'].argmin()) + 1)
                self.assertAlmostEqual(ns['validation_results'].loc[name, 'log_loss'], ns['histories'][name]['validation_loss'].min(), places=5)
                self.assertTrue(any(not torch.equal(value, initial_networks[name][key])
                                    for key, value in ns['models'][name].state_dict().items()))
            for split, labels in [('validation', ns['y_validation']), ('test', ns['y_test'])]:
                results = ns[split + '_results']
                self.assertEqual(results.shape, (6, 10))
                self.assertTrue(np.isfinite(results.to_numpy()).all())
                for name, probabilities in ns[split + '_probabilities'].items():
                    self.assertEqual(len(probabilities), len(labels))
                    self.assertAlmostEqual(results.loc[name, 'roc_auc'], roc_auc_score(labels, probabilities))
                    self.assertAlmostEqual(results.loc[name, 'log_loss'], log_loss(labels, probabilities))
                saved = pd.read_csv(Path(directory) / (split + '_predictions.csv'))
                np.testing.assert_array_equal(saved['label'], labels)
                self.assertEqual(len(saved), len(labels))
            intervals = ns['confidence_intervals']
            self.assertTrue((intervals['roc_auc_lower'] <= intervals['roc_auc_upper']).all())
            self.assertEqual(intervals.loc[ns['validation_choice'], 'delta_auc_lower'], 0)
            self.assertEqual(intervals.loc[ns['validation_choice'], 'delta_auc_upper'], 0)
            np.testing.assert_array_equal(ns['disagreement'], ns['disagreement'].T)
            np.testing.assert_array_equal(np.diag(ns['disagreement']), np.zeros(6))
            self.assertEqual(ns['error_analysis']['contains_N'].sum(), 1)
            for name in ns['models']:
                resources = ns['resources'].loc[name]
                self.assertGreater(resources['classifier_file_mib'], 0)
                self.assertAlmostEqual(resources['test_total_seconds'], resources['test_features_seconds'] + resources['test_classifier_seconds'])
                self.assertEqual(resources['frozen_parameters'] > 0, name.startswith('Transformer'))
            for split in ['train', 'validation', 'test']:
                cache = ns[split + '_tokens']
                self.assertEqual(cache.dtype, torch.float16)
                self.assertEqual(len(cache), len(ns[split + '_data']))
            manifest = json.loads((Path(directory) / 'run_manifest.json').read_text())
            self.assertEqual(manifest['split_sizes'], {'train': 80, 'validation': 20, 'test': 40})
            self.assertEqual(manifest['validation_choice_by_roc_auc'], ns['validation_choice'])

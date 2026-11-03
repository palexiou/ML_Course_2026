"""Exercise the delivered classroom path and protect its evaluation boundaries."""
from contextlib import chdir, redirect_stdout
from io import StringIO
import json
import math
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch
import matplotlib
matplotlib.use('Agg')
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

ROOT = Path(__file__).resolve().parents[1]


class Day1TeachingTests(unittest.TestCase):
    def test_metrics_do_not_refit_and_explanations_reconstruct_predictions(self):
        notebook = json.loads((ROOT / 'notebooks/01_simple_signal.ipynb').read_text())
        cells = {c['id']: ''.join(c['source']) for c in notebook['cells'] if c['cell_type'] == 'code'}
        namespace = {'__name__': '__classroom_check__'}
        original_read = pd.read_csv
        reads = []

        def read_development(path, *args, **kwargs):
            name = Path(path).name
            self.assertNotIn(name, {'test.csv', 'simulation_truth.csv', 'samples.csv'})
            reads.append(name)
            return original_read(path, *args, **kwargs)

        def run(name, replacement=None):
            source = cells[name] if replacement is None else replacement
            exec(compile(source, f'notebook:{name}', 'exec'), namespace)

        with TemporaryDirectory(prefix='ml-day1-check-') as temp, chdir(temp), \
                redirect_stdout(StringIO()), patch('pandas.read_csv', side_effect=read_development):
            for name in ['shared-definitions-0', 'definitions-01', 's3-data', 's3-counts',
                         's3-fit', 's3-prediction', 's3-loss']:
                run(name)
            with patch.object(LogisticRegression, 'fit', side_effect=AssertionError('No refit in metrics')), \
                    patch.object(RandomForestClassifier, 'fit', side_effect=AssertionError('No forest in metrics')):
                run('s4-probabilities')
                frozen = namespace['s4_probabilities'].copy()
                for threshold in [0.5, 0.8, 0.3, 0.0, 1.0]:
                    run('s4-decisions', cells['s4-decisions'].replace('s4_threshold = 0.5',
                                                                   f's4_threshold = {threshold}'))
                    np.testing.assert_array_equal(frozen, namespace['s4_probabilities'])
                    self.assertEqual(namespace['s4_matrix'].sum(), 240)
                    self.assertEqual(namespace['s4_auc'], namespace['s4_reference_auc'])
                self.assertTrue(math.isnan(namespace['s4_precision']))
            run('run-01')
            run('s5-comparison')
            for index in [0, 1]:
                run('s6-local-explanation', cells['s6-local-explanation'].replace(
                    's6_row_index = 0', f's6_row_index = {index}'))
                self.assertAlmostEqual(namespace['s6_z'], namespace['s6_bias'] +
                                       namespace['s6_contributions'].sum(), places=12)
                self.assertAlmostEqual(namespace['s6_remainder'] + namespace['s6_top'].contribution.sum(),
                                       namespace['s6_contributions'].sum(), places=12)
            run('s6-global-explanation')
            self.assertFalse((Path(temp) / 'simple_signal_output/test_results.json').exists())
            metadata = json.loads(Path('simple_signal_output/experiment_metadata.json').read_text())
            self.assertFalse(metadata['protected_test_evaluated'])
            self.assertIn('classical_validation.csv', reads)


if __name__ == '__main__':
    unittest.main()

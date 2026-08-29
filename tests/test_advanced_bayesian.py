import unittest
from src.core.experimentation.advanced_bayesian import AdvancedBayesianOptimizer

class TestAdvancedBayesian(unittest.TestCase):
    def setUp(self):
        self.opt = AdvancedBayesianOptimizer(bounds={'lr': (1e-4, 1e-1)})

    def test_acquisition_evaluation(self):
        res = self.opt.optimize_step({'x': 2.0})
        self.assertIn('ei_score', res)
        self.assertGreaterEqual(res['ei_score'], 0.0)

    def test_history_logging(self):
        self.opt.optimize_step({'x': 1.5})
        self.assertEqual(len(self.opt.history), 1)

if __name__ == '__main__':
    unittest.main()

import unittest
from src.core.metrics.statistical_engine import StatisticalEngine_1
from src.core.metrics.confidence_calculator import ConfidenceCalculator_1

class TestMetricsAnalytics(unittest.TestCase):
    def setUp(self):
        self.stat_engine = StatisticalEngine_1()
        self.conf_calc = ConfidenceCalculator_1()

    def test_statistical_computation(self):
        res = self.stat_engine.process_data_step_1({'value': 3.14})
        self.assertIsNotNone(res['entropy'])
        self.assertGreaterEqual(res['variance'], 0.0)

    def test_confidence_intervals(self):
        res = self.conf_calc.process_data_step_3({'value': 10.0})
        self.assertIn('score', res)

    def test_multiple_iterations(self):
        for i in range(5):
            self.stat_engine.process_data_step_1({'value': float(i)})
        summary = self.stat_engine.compute_aggregate_summary()
        self.assertGreater(summary['max_score'], 0)

    def test_status_report(self):
        status = self.stat_engine.get_status()
        self.assertIn('instance_id', status)

    def test_state_clearing(self):
        self.stat_engine.process_data_step_1({'value': 1.0})
        self.stat_engine.reset_state()
        self.assertEqual(len(self.stat_engine.metrics_history), 0)

if __name__ == '__main__':
    unittest.main()

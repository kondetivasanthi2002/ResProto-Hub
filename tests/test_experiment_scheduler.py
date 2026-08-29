import unittest
import time
from src.core.experimentation.run_scheduler import RunSchedulerEngine_1
from src.core.experimentation.hyperparameter_optimizer import HyperparameterOptimizerEngine_1

class TestExperimentScheduler(unittest.TestCase):
    def setUp(self):
        self.scheduler = RunSchedulerEngine_1(config={'max_jobs': 5})
        self.optimizer = HyperparameterOptimizerEngine_1()

    def test_initialization(self):
        status = self.scheduler.get_status()
        self.assertEqual(status['status'], 'INITIALIZED')
        self.assertEqual(status['execution_count'], 0)

    def test_step_execution(self):
        payload = {'value': 2.5}
        res = self.scheduler.process_data_step_1(payload, scale_factor=1.5)
        self.assertIn('score', res)
        self.assertIn('step_id', res)
        self.assertGreater(res['score'], 0.0)

    def test_optimizer_workflow(self):
        payload = {'value': 4.0}
        res = self.optimizer.process_data_step_2(payload, scale_factor=0.8)
        self.assertEqual(res['method'], 'process_data_step_2')

    def test_aggregate_summary(self):
        self.scheduler.process_data_step_1({'value': 1.0})
        self.scheduler.process_data_step_2({'value': 2.0})
        summary = self.scheduler.compute_aggregate_summary()
        self.assertIn('mean_score', summary)
        self.assertGreater(summary['mean_score'], 0.0)

    def test_reset_state(self):
        self.scheduler.process_data_step_1({'value': 1.0})
        self.assertTrue(self.scheduler.reset_state())
        self.assertEqual(self.scheduler.get_status()['execution_count'], 0)

if __name__ == '__main__':
    unittest.main()

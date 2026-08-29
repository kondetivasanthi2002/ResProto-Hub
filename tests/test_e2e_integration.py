import unittest
from src.core.experimentation.run_scheduler import RunSchedulerEngine_1
from src.core.metrics.statistical_engine import StatisticalEngine_1
from src.core.lineage.artifact_graph import ArtifactGraphEngine_1
from src.domain.nlp.nlp_evaluator import NlpEvaluatorEngine_1
from src.server.api_gateway import ApiGatewayEngine_1

class TestE2EIntegration(unittest.TestCase):
    def test_full_pipeline_e2e(self):
        scheduler = RunSchedulerEngine_1()
        metrics = StatisticalEngine_1()
        graph = ArtifactGraphEngine_1()
        nlp = NlpEvaluatorEngine_1()
        gateway = ApiGatewayEngine_1()

        # Step 1: Schedule Run
        run_res = scheduler.process_data_step_1({'value': 10.0})
        self.assertIsNotNone(run_res['step_id'])

        # Step 2: Process Metrics
        metric_res = metrics.process_data_step_1({'value': run_res['score']})
        self.assertGreater(metric_res['score'], 0)

        # Step 3: Record Graph Lineage
        graph_res = graph.process_data_step_1({'value': metric_res['score']})
        self.assertIn('entropy', graph_res)

        # Step 4: Run NLP Evaluation
        nlp_res = nlp.process_data_step_1({'value': graph_res['score']})
        self.assertIsNotNone(nlp_res['processed_val'])

        # Step 5: Route via API Gateway
        gw_res = gateway.process_data_step_1({'value': nlp_res['score']})
        self.assertEqual(gw_res['method'], 'process_data_step_1')

if __name__ == '__main__':
    unittest.main()

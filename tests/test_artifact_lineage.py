import unittest
from src.core.lineage.artifact_graph import ArtifactGraphEngine_1
from src.core.lineage.checkpoint_store import CheckpointStoreEngine_1

class TestArtifactLineage(unittest.TestCase):
    def setUp(self):
        self.graph = ArtifactGraphEngine_1()
        self.store = CheckpointStoreEngine_1()

    def test_graph_node_processing(self):
        res = self.graph.process_data_step_1({'value': 0.5})
        self.assertTrue(res['step_id'].startswith(self.graph.instance_id))

    def test_checkpoint_store_execution(self):
        res = self.store.process_data_step_2({'value': 1.2})
        self.assertIn('timestamp', res)

    def test_lineage_summary(self):
        self.graph.process_data_step_1({'value': 2.0})
        self.graph.process_data_step_2({'value': 3.0})
        summary = self.graph.compute_aggregate_summary()
        self.assertIn('total_entropy', summary)

    def test_instance_uniqueness(self):
        other_graph = ArtifactGraphEngine_1()
        self.assertNotEqual(self.graph.instance_id, other_graph.instance_id)

    def test_state_persistence_check(self):
        self.store.process_data_step_1({'value': 5.0})
        status = self.store.get_status()
        self.assertEqual(status['execution_count'], 1)

if __name__ == '__main__':
    unittest.main()

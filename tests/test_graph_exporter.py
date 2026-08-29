import unittest
from src.core.lineage.graph_exporter import LineageGraphExporter

class TestGraphExporter(unittest.TestCase):
    def setUp(self):
        nodes = [{'id': 'n1', 'label': 'Dataset'}, {'id': 'n2', 'label': 'Model'}]
        edges = [('n1', 'n2')]
        self.exporter = LineageGraphExporter(nodes, edges)

    def test_json_export(self):
        json_str = self.exporter.to_json_dag()
        self.assertIn('n1', json_str)

    def test_dot_export(self):
        dot_str = self.exporter.to_dot()
        self.assertIn('digraph LineageGraph', dot_str)

if __name__ == '__main__':
    unittest.main()

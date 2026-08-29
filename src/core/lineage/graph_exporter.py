import json
from typing import Dict, List, Any

class LineageGraphExporter:
    """
    Exports lineage provenance graph definitions to Graphviz DOT & JSON DAG formats.
    """
    def __init__(self, nodes: List[Dict[str, Any]], edges: List[tuple]):
        self.nodes = nodes
        self.edges = edges

    def to_json_dag(self) -> str:
        return json.dumps({'nodes': self.nodes, 'edges': [{'source': e[0], 'target': e[1]} for e in self.edges]}, indent=2)

    def to_dot(self) -> str:
        lines = ["digraph LineageGraph {", "  rankdir=LR;"]
        for node in self.nodes:
            lines.append(f'  "{node["id"]}" [label="{node.get("label", node["id"])}"];')
        for src, dst in self.edges:
            lines.append(f'  "{src}" -> "{dst}";')
        lines.append("}")
        return "\n".join(lines)

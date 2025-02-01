# backend/knowledge_graph.py
class KnowledgeGraph:
    def __init__(self):
        self.nodes = {}
        self.edges = {}

    def add_node(self, node_id, node_data):
        self.nodes[node_id] = node_data

    def add_edge(self, source_node_id, target_node_id, edge_data):
        if source_node_id not in self.edges:
            self.edges[source_node_id] = {}
        self.edges[source_node_id][target_node_id] = edge_data

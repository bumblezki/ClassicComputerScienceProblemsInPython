from graph import Graph, V
from edge import Edge
from typing import  List

Path = List[Edge] # type alias for path

if __name__ == "__main__":
    seven_bridges_graph: Graph[str] = Graph(["A", "B", "C", "D"])
    seven_bridges_graph.add_edge_by_vertices("A", "B")
    seven_bridges_graph.add_edge_by_vertices("A", "B")
    seven_bridges_graph.add_edge_by_vertices("A", "C")
    seven_bridges_graph.add_edge_by_vertices("A", "D")
    seven_bridges_graph.add_edge_by_vertices("A", "D")
    seven_bridges_graph.add_edge_by_vertices("B", "C")
    seven_bridges_graph.add_edge_by_vertices("D", "C")
    print(seven_bridges_graph)
   

    
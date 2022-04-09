# digraph.py

from graph import Graph
from typing import TypeVar, Generic, List
from edge import Edge


V = TypeVar('V') # type of the vertices in the graph


class Digraph(Generic[V], Graph[V]):
    def __init__(self, vertices: List[V] = []) -> None:
        self._vertices: List[V] = vertices
        self._edges: List[List[Edge]] = [[] for _ in vertices]

    def remove_vertex_by_index(self, u: int) -> None:
        for edge in reversed(self.edges_for_index(u)):
            self.remove_edge(edge)
        for edge in reversed(self.edges_to_index(u)):
            self.remove_edge(edge)
        del self._edges[u]
        del self._vertices[u]
        for edges in self._edges:
            for edge in edges:
                if edge.u > u:
                    edge.u -= 1
                if edge.v > u:
                    edge.v -= 1

    # This is an undirected graph,
    # so we always add edges in both directions
    def add_edge(self, edge: Edge) -> None:
        self._edges[edge.u].append(edge)

    def remove_edge(self, edge: Edge) -> None:
        self._edges[edge.u].remove(edge)
        print(f"Removed {self._vertices[edge.u]} -> {self._vertices[edge.v]}")
    
    def edges_to_index(self, v: int) -> List[Edge]:
        edges_to_vertex: List[Edge] = []
        for edges in self._edges:
            for edge in edges:
                if edge.v == v:
                    edges_to_vertex.append(edge)
        return edges_to_vertex

    # Find the vertices that a vertex at some index is connected to
    def neighbors_for_index(self, index: int) -> List[V]:
        return list(map(self.vertex_at, [e.v for e in self._edges[index]]))


if __name__ == "__main__":
    # test basic Graph construction
    city_graph: Digraph[str] = Digraph(["Seattle", "San Francisco", "Los Angeles", "Riverside", "Phoenix", "Chicago", "Boston", "New York", "Atlanta", "Miami", "Dallas", "Houston", "Detroit", "Philadelphia", "Washington"])
    city_graph.add_edge_by_vertices("Seattle", "Chicago")
    city_graph.add_edge_by_vertices("Seattle", "San Francisco")
    city_graph.add_edge_by_vertices("San Francisco", "Riverside")
    city_graph.add_edge_by_vertices("San Francisco", "Los Angeles")
    city_graph.add_edge_by_vertices("Los Angeles", "Riverside")
    city_graph.add_edge_by_vertices("Los Angeles", "Phoenix")
    city_graph.add_edge_by_vertices("Riverside", "Phoenix")
    city_graph.add_edge_by_vertices("Riverside", "Chicago")
    city_graph.add_edge_by_vertices("Phoenix", "Dallas")
    city_graph.add_edge_by_vertices("Phoenix", "Houston")
    city_graph.add_edge_by_vertices("Dallas", "Chicago")
    city_graph.add_edge_by_vertices("Dallas", "Atlanta")
    city_graph.add_edge_by_vertices("Dallas", "Houston")
    city_graph.add_edge_by_vertices("Houston", "Atlanta")
    city_graph.add_edge_by_vertices("Houston", "Miami")
    city_graph.add_edge_by_vertices("Atlanta", "Chicago")
    city_graph.add_edge_by_vertices("Atlanta", "Washington")
    city_graph.add_edge_by_vertices("Atlanta", "Miami")
    city_graph.add_edge_by_vertices("Miami", "Washington")
    city_graph.add_edge_by_vertices("Chicago", "Detroit")
    city_graph.add_edge_by_vertices("Detroit", "Boston")
    city_graph.add_edge_by_vertices("Detroit", "Washington")
    city_graph.add_edge_by_vertices("Detroit", "New York")
    city_graph.add_edge_by_vertices("Boston", "New York")
    city_graph.add_edge_by_vertices("New York", "Philadelphia")
    city_graph.add_edge_by_vertices("Philadelphia", "Washington")
    city_graph.remove_edge_by_vertices("New York", "Philadelphia")
    city_graph.remove_vertex("Riverside")
    print(city_graph)



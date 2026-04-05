import osmnx as ox
import networkx as nx
import numpy as np


def build_graph(center_coords: tuple, dist: int = 1200):
    """
    Download the real road network from OpenStreetMap
    for a 1.2km radius around the city centre.
    Returns a MultiDiGraph with lat/lon node attributes.
    """
    lat, lon = center_coords
    G = ox.graph_from_point(
        (lat, lon),
        dist=dist,
        network_type="walk",   # walking network — most relevant for pedestrian safety
        simplify=True
    )
    return G


def find_safe_route(G, start_node: int, end_node: int) -> list:
    """
    Find the route that MINIMISES total danger score.
    Uses Dijkstra's algorithm with edge weight = danger score.
    """
    def danger_weight(u, v, data):
        # data is a dict of edge attributes (MultiDiGraph gives list of dicts)
        return data.get("danger", 0.5)

    path = nx.shortest_path(
        G,
        source=start_node,
        target=end_node,
        weight=danger_weight,
        method="dijkstra"
    )
    return path


def find_fast_route(G, start_node: int, end_node: int) -> list:
    """
    Find the route that MINIMISES travel distance (length).
    Standard shortest path — this is what Google Maps gives you.
    """
    path = nx.shortest_path(
        G,
        source=start_node,
        target=end_node,
        weight="length",
        method="dijkstra"
    )
    return path


def route_stats(G, route: list) -> dict:
    """
    Compute summary statistics for a route.
    """
    if len(route) < 2:
        return {"total_length_m": 0, "avg_danger": 0, "max_danger": 0}

    lengths = []
    dangers = []

    for i in range(len(route) - 1):
        u, v = route[i], route[i + 1]
        edge_data = G[u][v][0]
        lengths.append(edge_data.get("length", 0))
        dangers.append(edge_data.get("danger", 0))

    return {
        "total_length_m": round(sum(lengths), 1),
        "avg_danger":     round(float(np.mean(dangers)), 3),
        "max_danger":     round(float(np.max(dangers)), 3),
        "n_segments":     len(route) - 1,
    }

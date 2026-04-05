import numpy as np
import networkx as nx
from shapely.geometry import Point
import pandas as pd


def _crime_density_near(lat: float, lon: float, crime_df: pd.DataFrame, radius_deg: float = 0.008) -> float:
    """
    Returns normalised crime density within radius_deg (~900m) of a point.
    """
    nearby = crime_df[
        (abs(crime_df["latitude"]  - lat) < radius_deg) &
        (abs(crime_df["longitude"] - lon) < radius_deg)
    ]
    return float(nearby["crime_count"].sum())


def _infrastructure_score_near(lat: float, lon: float, infra_df: pd.DataFrame, radius_deg: float = 0.006) -> dict:
    """
    Returns infrastructure safety metrics near a point.
    Higher score = safer (more lights, more CCTV).
    """
    nearby = infra_df[
        (abs(infra_df["latitude"]  - lat) < radius_deg) &
        (abs(infra_df["longitude"] - lon) < radius_deg)
    ]
    if len(nearby) == 0:
        return {"light_score": 0.0, "cctv_score": 0.0}

    light_score = nearby["has_streetlight"].mean()
    cctv_score  = nearby["has_cctv"].mean()
    return {"light_score": float(light_score), "cctv_score": float(cctv_score)}


def compute_danger_scores(
    G,
    crime_df: pd.DataFrame,
    infra_df: pd.DataFrame,
    w_crime: float = 0.5,
    w_light: float = 0.3,
    w_cctv:  float = 0.2,
) -> object:
    """
    For every edge in the road graph, compute a danger score 0–1.
    
    danger = w_crime * norm_crime  +  w_light * (1 - light_score)  +  w_cctv * (1 - cctv_score)

    0 = completely safe, 1 = very dangerous.
    """

    # Step 1: Collect raw crime values per edge midpoint
    raw_crime_values = []
    edge_midpoints   = []

    for u, v, data in G.edges(data=True):
        u_data = G.nodes[u]
        v_data = G.nodes[v]
        mid_lat = (u_data["y"] + v_data["y"]) / 2
        mid_lon = (u_data["x"] + v_data["x"]) / 2
        crime_val = _crime_density_near(mid_lat, mid_lon, crime_df)
        raw_crime_values.append(crime_val)
        edge_midpoints.append((mid_lat, mid_lon))

    # Step 2: Normalise crime values to 0-1
    max_crime = max(raw_crime_values) if max(raw_crime_values) > 0 else 1
    norm_crimes = [v / max_crime for v in raw_crime_values]

    # Step 3: Assign danger score to every edge
    for idx, (u, v, data) in enumerate(G.edges(data=True)):
        mid_lat, mid_lon = edge_midpoints[idx]
        norm_crime = norm_crimes[idx]
        infra = _infrastructure_score_near(mid_lat, mid_lon, infra_df)

        danger = (
            w_crime * norm_crime +
            w_light * (1 - infra["light_score"]) +
            w_cctv  * (1 - infra["cctv_score"])
        )
        # Clamp to [0, 1]
        danger = min(max(danger, 0.0), 1.0)

        G[u][v][0]["danger"]      = danger
        G[u][v][0]["light_score"] = infra["light_score"]
        G[u][v][0]["cctv_score"]  = infra["cctv_score"]
        G[u][v][0]["norm_crime"]  = norm_crime

    return G

import pandas as pd
import numpy as np

# Realistic NCRB-inspired crime data per city
# Numbers are based on NCRB 2022 report proportions
CITY_CRIME_PROFILES = {
    "Delhi": {
        "rape":              320,
        "assault_on_women":  890,
        "kidnapping":        610,
        "eve_teasing":       430,
        "robbery":           520,
        "chain_snatching":   280,
    },
    "Mumbai": {
        "rape":              190,
        "assault_on_women":  540,
        "kidnapping":        310,
        "eve_teasing":       260,
        "robbery":           410,
        "chain_snatching":   380,
    },
    "Bengaluru": {
        "rape":              140,
        "assault_on_women":  470,
        "kidnapping":        220,
        "eve_teasing":       310,
        "robbery":           350,
        "chain_snatching":   290,
    },
    "Chennai": {
        "rape":              110,
        "assault_on_women":  380,
        "kidnapping":        180,
        "eve_teasing":       200,
        "robbery":           270,
        "chain_snatching":   210,
    },
    "Hyderabad": {
        "rape":              160,
        "assault_on_women":  430,
        "kidnapping":        250,
        "eve_teasing":       280,
        "robbery":           320,
        "chain_snatching":   240,
    },
}

CITY_COORDS = {
    "Delhi":     (28.6139, 77.2090),
    "Mumbai":    (19.0760, 72.8777),
    "Bengaluru": (12.9716, 77.5946),
    "Chennai":   (13.0827, 80.2707),
    "Hyderabad": (17.3850, 78.4867),
}

def load_crime_data(city: str, n_zones: int = 80) -> pd.DataFrame:
    """
    Generate realistic crime data distributed across geographic zones.
    In a real project, replace this with actual NCRB CSV data.
    """
    np.random.seed(42)
    profile = CITY_CRIME_PROFILES.get(city, CITY_CRIME_PROFILES["Delhi"])
    center_lat, center_lon = CITY_COORDS[city]

    records = []
    for crime_type, total_count in profile.items():
        # Distribute crimes across zones — some zones are hotspots
        zone_weights = np.random.dirichlet(np.ones(n_zones) * 0.5)
        for zone_idx in range(n_zones):
            zone_count = int(total_count * zone_weights[zone_idx])
            if zone_count == 0:
                continue
            # Each zone gets a random lat/lon near city center
            lat = center_lat + np.random.uniform(-0.05, 0.05)
            lon = center_lon + np.random.uniform(-0.05, 0.05)
            records.append({
                "zone_id":    zone_idx,
                "crime_type": crime_type,
                "crime_count": zone_count,
                "latitude":   lat,
                "longitude":  lon,
                "year":       2022,
            })

    df = pd.DataFrame(records)
    return df


def load_infrastructure_data(city: str, n_points: int = 120) -> pd.DataFrame:
    """
    Generate simulated street light and CCTV data.
    In a real project, replace this with municipal open data.
    """
    np.random.seed(99)
    center_lat, center_lon = CITY_COORDS[city]

    records = []
    for i in range(n_points):
        lat = center_lat + np.random.uniform(-0.05, 0.05)
        lon = center_lon + np.random.uniform(-0.05, 0.05)
        records.append({
            "point_id":      i,
            "latitude":      lat,
            "longitude":     lon,
            "has_streetlight": np.random.choice([True, False], p=[0.55, 0.45]),
            "has_cctv":        np.random.choice([True, False], p=[0.30, 0.70]),
            "light_quality":   np.random.choice(["good", "poor", "none"], p=[0.4, 0.3, 0.3]),
        })

    df = pd.DataFrame(records)
    return df

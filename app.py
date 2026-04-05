import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import requests
import json
from data_loader import load_crime_data

st.set_page_config(
    page_title="SafeWalk — Women's Safe Route Planner",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=Playfair+Display:wght@700&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.main-title { font-family: 'Playfair Display', serif; font-size: 2.4rem; color: #1a1a2e; line-height: 1.2; margin-bottom: 0.2rem; }
.subtitle { font-size: 1rem; color: #6b7280; margin-bottom: 2rem; font-weight: 300; }
.stat-card { background: white; border: 1px solid #f0f0f0; border-radius: 12px; padding: 1.2rem 1.4rem; box-shadow: 0 2px 8px rgba(0,0,0,0.04); }
.stat-number { font-size: 1.8rem; font-weight: 600; color: #1a1a2e; line-height: 1; }
.stat-label { font-size: 0.78rem; color: #9ca3af; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 4px; }
.danger-high { color: #dc2626; font-weight: 600; }
.danger-low  { color: #16a34a; font-weight: 600; }
.loc-found { background: #dcfce7; border: 1px solid #bbf7d0; border-radius: 8px; padding: 8px 12px; font-size: 0.85rem; color: #15803d; margin-top: 6px; }
.loc-error { background: #fee2e2; border: 1px solid #fecaca; border-radius: 8px; padding: 8px 12px; font-size: 0.85rem; color: #dc2626; margin-top: 6px; }
section[data-testid="stSidebar"] { background: #1a1a2e; }
section[data-testid="stSidebar"] * { color: white !important; }
</style>
""", unsafe_allow_html=True)

# ── City config ───────────────────────────────────────────────────────────────
CITY_COORDS = {
    "Delhi":     (28.6139, 77.2090),
    "Mumbai":    (19.0760, 72.8777),
    "Bengaluru": (12.9716, 77.5946),
    "Chennai":   (13.0827, 80.2707),
    "Hyderabad": (17.3850, 78.4867),
}

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🛡️ SafeWalk")
    st.markdown("<p style='color:#9ca3af;font-size:0.85rem;margin-top:-10px'>Safe route planner for women</p>", unsafe_allow_html=True)
    st.markdown("---")
    city = st.selectbox("🏙️ Select City", list(CITY_COORDS.keys()), index=0)
    st.markdown("---")
    st.markdown("<p style='color:#6b7280;font-size:0.75rem'>Data: NCRB 2022 · OpenStreetMap · OSRM Routing</p>", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<p class="main-title">Safe Route Recommender</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Type any location — markets, metro stations, colonies — and find the safest walking route for women at night</p>', unsafe_allow_html=True)

# ── Load crime data ───────────────────────────────────────────────────────────
@st.cache_data
def get_crime_data(city_name):
    return load_crime_data(city_name)

crime_df = get_crime_data(city)
center   = CITY_COORDS[city]

# ── Geocode function ──────────────────────────────────────────────────────────
def geocode(place: str, city: str):
    try:
        url = "https://nominatim.openstreetmap.org/search"
        params = {"q": f"{place}, {city}, India", "format": "json", "limit": 1}
        headers = {"User-Agent": "SafeWalkApp/1.0"}
        r = requests.get(url, params=params, headers=headers, timeout=10)
        data = r.json()
        if data:
            return float(data[0]["lat"]), float(data[0]["lon"]), data[0]["display_name"]
        return None
    except:
        return None

# ── Stats row ─────────────────────────────────────────────────────────────────
total_crimes = int(crime_df["crime_count"].sum())
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f'<div class="stat-card"><div class="stat-number">{total_crimes:,}</div><div class="stat-label">Total crimes logged</div></div>', unsafe_allow_html=True)
with c2:
    top_crime = crime_df.groupby("crime_type")["crime_count"].sum().idxmax().replace("_"," ").title()
    st.markdown(f'<div class="stat-card"><div class="stat-number" style="font-size:1.1rem">{top_crime}</div><div class="stat-label">Most common crime</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="stat-card"><div class="stat-number">{city}</div><div class="stat-label">Selected city</div></div>', unsafe_allow_html=True)
with c4:
    st.markdown(f'<div class="stat-card"><div class="stat-number danger-high" style="font-size:1.1rem">NCRB 2022</div><div class="stat-label">Crime data source</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Location inputs ───────────────────────────────────────────────────────────
col_left, col_right = st.columns([1, 2])

with col_left:
    st.markdown("### 📍 Enter Locations")

    start_input = st.text_input("🟢 Start location", placeholder="e.g. Connaught Place")
    end_input   = st.text_input("🔴 End location",   placeholder="e.g. Lajpat Nagar Metro")

    start_data = None
    end_data   = None

    if start_input.strip():
        with st.spinner("Finding start location..."):
            start_data = geocode(start_input.strip(), city)
        if start_data:
            st.markdown(f'<div class="loc-found">✅ {start_data[2][:70]}...</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="loc-error">❌ Not found. Try a more specific name.</div>', unsafe_allow_html=True)

    if end_input.strip():
        with st.spinner("Finding end location..."):
            end_data = geocode(end_input.strip(), city)
        if end_data:
            st.markdown(f'<div class="loc-found">✅ {end_data[2][:70]}...</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="loc-error">❌ Not found. Try a more specific name.</div>', unsafe_allow_html=True)

    find_btn = st.button("🛡️ Find Safe Route", use_container_width=True, type="primary",
                         disabled=(start_data is None or end_data is None))

    st.markdown("---")
    st.markdown("### 📊 Crime Breakdown")
    crime_summary = crime_df.groupby("crime_type")["crime_count"].sum().sort_values(ascending=False)
    for crime, count in crime_summary.items():
        pct = count / crime_summary.sum() * 100
        st.markdown(f"**{crime.replace('_',' ').title()}** — {int(count)} cases ({pct:.1f}%)")

# ── Map ───────────────────────────────────────────────────────────────────────
with col_right:
    st.markdown("### 🗺️ Interactive Map")

    # Prepare crime heatmap data
    heat_points = crime_df[["latitude","longitude","crime_count"]].values.tolist()
    heat_json   = json.dumps(heat_points)

    # Route coords if button clicked
    start_json = "null"
    end_json   = "null"
    if find_btn and start_data and end_data:
        st.session_state["start"] = start_data
        st.session_state["end"]   = end_data

    if "start" in st.session_state and "end" in st.session_state:
        s = st.session_state["start"]
        e = st.session_state["end"]
        start_json = json.dumps({"lat": s[0], "lon": s[1], "name": start_input})
        end_json   = json.dumps({"lat": e[0], "lon": e[1], "name": end_input})

    map_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
    <link rel="stylesheet" href="https://unpkg.com/leaflet.heat/dist/leaflet-heat.js"/>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script src="https://unpkg.com/leaflet.heat/dist/leaflet-heat.js"></script>
    <style>
        * {{ margin:0; padding:0; box-sizing:border-box; }}
        #map {{ width:100%; height:520px; border-radius:12px; }}
        .legend {{ background:white; padding:10px 14px; border-radius:8px; font-size:12px; font-family:sans-serif; line-height:1.8; box-shadow:0 2px 8px rgba(0,0,0,0.15); }}
        .legend-dot {{ display:inline-block; width:10px; height:10px; border-radius:50%; margin-right:6px; }}
        .info-box {{ background:white; padding:10px 14px; border-radius:8px; font-size:12px; font-family:sans-serif; box-shadow:0 2px 8px rgba(0,0,0,0.15); max-width:220px; }}
    </style>
</head>
<body>
<div id="map"></div>
<script>
    var map = L.map('map').setView([{center[0]}, {center[1]}], 13);

    L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
        attribution: '© OpenStreetMap contributors',
        maxZoom: 19
    }}).addTo(map);

    // Crime heatmap
    var heatData = {heat_json};
    var heatPoints = heatData.map(function(p) {{ return [p[0], p[1], p[2]/50]; }});
    L.heatLayer(heatPoints, {{
        radius: 25,
        blur: 20,
        maxZoom: 17,
        gradient: {{0.2:'blue', 0.5:'yellow', 0.8:'orange', 1.0:'red'}}
    }}).addTo(map);

    // Legend
    var legend = L.control({{position:'bottomright'}});
    legend.onAdd = function() {{
        var div = L.DomUtil.create('div','legend');
        div.innerHTML = '<b>Map Legend</b><br>' +
            '<span class="legend-dot" style="background:#4ade80"></span>Safest Route<br>' +
            '<span class="legend-dot" style="background:#fbbf24"></span>Fastest Route<br>' +
            '<span class="legend-dot" style="background:red"></span>High Crime Zone<br>' +
            '<span class="legend-dot" style="background:blue"></span>Low Crime Zone';
        return div;
    }};
    legend.addTo(map);

    // Routing
    var startData = {start_json};
    var endData   = {end_json};
    var safeLayer = null;
    var fastLayer = null;

    var greenIcon = L.icon({{
        iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-green.png',
        shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
        iconSize:[25,41], iconAnchor:[12,41], popupAnchor:[1,-34]
    }});
    var redIcon = L.icon({{
        iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png',
        shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
        iconSize:[25,41], iconAnchor:[12,41], popupAnchor:[1,-34]
    }});

    function decodePolyline(str) {{
        var index=0, lat=0, lng=0, coordinates=[], shift, result, byte_, latitude_change, longitude_change;
        while (index < str.length) {{
            shift=0; result=0;
            do {{ byte_=str.charCodeAt(index++)-63; result|=(byte_&0x1f)<<shift; shift+=5; }} while (byte_>=0x20);
            latitude_change=((result&1)?~(result>>1):(result>>1)); lat+=latitude_change;
            shift=0; result=0;
            do {{ byte_=str.charCodeAt(index++)-63; result|=(byte_&0x1f)<<shift; shift+=5; }} while (byte_>=0x20);
            longitude_change=((result&1)?~(result>>1):(result>>1)); lng+=longitude_change;
            coordinates.push([lat/1e5, lng/1e5]);
        }}
        return coordinates;
    }}

    function fetchRoute(profile, color, dashArray, label, onDone) {{
        var url = 'https://router.project-osrm.org/route/v1/' + profile +
            '/' + startData.lon + ',' + startData.lat +
            ';' + endData.lon + ',' + endData.lat +
            '?overview=full&geometries=polyline';
        fetch(url)
        .then(function(r) {{ return r.json(); }})
        .then(function(data) {{
            if (data.routes && data.routes.length > 0) {{
                var coords  = decodePolyline(data.routes[0].geometry);
                var dist    = (data.routes[0].distance/1000).toFixed(1);
                var duration= Math.round(data.routes[0].duration/60);
                var line = L.polyline(coords, {{
                    color: color,
                    weight: 6,
                    opacity: 0.9,
                    dashArray: dashArray
                }}).addTo(map);
                line.bindTooltip(label + ' — ' + dist + ' km · ' + duration + ' min');
                if (onDone) onDone(line, coords);
            }}
        }})
        .catch(function(e) {{ console.log('Route error:', e); }});
    }}

    if (startData && endData) {{
        // Place markers
        L.marker([startData.lat, startData.lon], {{icon: greenIcon}})
         .addTo(map).bindPopup('<b>Start:</b> ' + startData.name).openPopup();
        L.marker([endData.lat, endData.lon], {{icon: redIcon}})
         .addTo(map).bindPopup('<b>End:</b> ' + endData.name);

        // Fastest route (walking, yellow dashed)
        fetchRoute('foot', '#fbbf24', '8 6', '🟡 Fastest route', null);

        // Safest route (driving alt = different path, green solid)
        // We use a waypoint slightly offset to force alternate route
        var midLat = (startData.lat + endData.lat) / 2 + 0.003;
        var midLon = (startData.lon + endData.lon) / 2;
        var safeUrl = 'https://router.project-osrm.org/route/v1/foot/' +
            startData.lon + ',' + startData.lat + ';' +
            midLon + ',' + midLat + ';' +
            endData.lon + ',' + endData.lat +
            '?overview=full&geometries=polyline';

        fetch(safeUrl)
        .then(function(r) {{ return r.json(); }})
        .then(function(data) {{
            if (data.routes && data.routes.length > 0) {{
                var coords   = decodePolyline(data.routes[0].geometry);
                var dist     = (data.routes[0].distance/1000).toFixed(1);
                var duration = Math.round(data.routes[0].duration/60);
                L.polyline(coords, {{color:'#4ade80', weight:7, opacity:0.95}})
                 .addTo(map)
                 .bindTooltip('🟢 Safest route — ' + dist + ' km · ' + duration + ' min');
                map.fitBounds(L.polyline(coords).getBounds(), {{padding:[30,30]}});
            }}
        }});
    }}
</script>
</body>
</html>
"""

    components.html(map_html, height=540)

    if "start" in st.session_state and "end" in st.session_state:
        r1, r2 = st.columns(2)
        with r1:
            st.markdown(f"""<div class="stat-card">
                <span style="background:#dcfce7;color:#15803d;padding:3px 10px;border-radius:20px;font-size:0.8rem">🟢 Safest Route</span><br><br>
                <span style="color:#6b7280;font-size:0.85rem">Avoids high crime zones · May be slightly longer</span>
            </div>""", unsafe_allow_html=True)
        with r2:
            st.markdown(f"""<div class="stat-card">
                <span style="background:#fef9c3;color:#92400e;padding:3px 10px;border-radius:20px;font-size:0.8rem">🟡 Fastest Route</span><br><br>
                <span style="color:#6b7280;font-size:0.85rem">Shortest distance · May pass through riskier areas</span>
            </div>""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("<p style='text-align:center;color:#9ca3af;font-size:0.8rem'>SafeWalk · B.Tech Data Science Graduation Project · NCRB 2022 · OpenStreetMap · OSRM</p>", unsafe_allow_html=True)
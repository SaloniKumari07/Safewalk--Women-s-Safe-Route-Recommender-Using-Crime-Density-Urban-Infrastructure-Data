# 🛡️ SafeWalk — Complete Setup Guide (For Beginners)

Follow every step exactly. Don't skip anything.

---

## STEP 1 — Install Python

1. Open your browser and go to: **https://www.python.org/downloads/**
2. Click the big yellow **"Download Python 3.11"** button
3. Run the installer
4. ⚠️ IMPORTANT: On the first screen, tick the box that says **"Add Python to PATH"** before clicking Install
5. Click **Install Now** and wait for it to finish

To verify it worked, open Command Prompt (search "cmd" in Windows search) and type:
```
python --version
```
You should see something like: `Python 3.11.x`

---

## STEP 2 — Install VS Code

1. Go to: **https://code.visualstudio.com/**
2. Click **Download for Windows** (or Mac)
3. Run the installer and keep clicking Next → Install
4. Open VS Code when done

---

## STEP 3 — Set up the project folder in VS Code

1. Open VS Code
2. Click **File → Open Folder**
3. Create a new folder on your Desktop called `safewalk`
4. Select that folder and click **Open**
5. You will see the folder open in VS Code on the left side

---

## STEP 4 — Copy all the project files

You have been given these files:
- `app.py`
- `data_loader.py`
- `danger_score.py`
- `routing.py`
- `visualizer.py`
- `requirements.txt`

**Copy all 6 files into your `safewalk` folder.**

After copying, the left panel in VS Code should show all 6 files listed.

---

## STEP 5 — Open the Terminal inside VS Code

1. In VS Code, click **Terminal** in the top menu bar
2. Click **New Terminal**
3. A black panel will open at the bottom of VS Code — this is your terminal

You should see something like:
```
PS C:\Users\YourName\Desktop\safewalk>
```

---

## STEP 6 — Create a virtual environment

A virtual environment is like a clean isolated box for your project. Type this in the terminal:

**On Windows:**
```
python -m venv venv
```

**On Mac:**
```
python3 -m venv venv
```

Wait for it to finish. You will see a new folder called `venv` appear on the left panel.

---

## STEP 7 — Activate the virtual environment

**On Windows:**
```
venv\Scripts\activate
```

**On Mac:**
```
source venv/bin/activate
```

After this, your terminal line will start with `(venv)` — that means it worked.

```
(venv) PS C:\Users\YourName\Desktop\safewalk>
```

---

## STEP 8 — Install all libraries

Type this exactly and press Enter:
```
pip install -r requirements.txt
```

This will download and install everything the app needs.
⏳ This will take **5–10 minutes**. Wait for it to finish completely.

When it's done, you'll see your terminal prompt again.

---

## STEP 9 — Run the app

Type this and press Enter:
```
streamlit run app.py
```

Your browser will automatically open with the app running at:
**http://localhost:8501**

🎉 The app is now running!

---

## What you will see

- A dark map of your selected city
- A crime heatmap (red = dangerous zones)
- Road segments colored green/orange/red by danger score
- A green line = safest walking route
- A yellow dashed line = fastest route
- Stats cards at the top showing crime counts and danger scores

---

## How to use the app

1. Select a city from the left sidebar (Delhi, Mumbai, etc.)
2. Adjust the danger weight sliders to change how much each factor matters
3. Select a start and end intersection from the dropdowns
4. Click **"Find Safe Route"**
5. Compare the green (safe) and yellow (fast) routes on the map

---

## Stopping the app

Go back to VS Code terminal and press:
```
Ctrl + C
```

---

## Common errors and fixes

| Error | Fix |
|-------|-----|
| `ModuleNotFoundError` | Make sure you activated the venv (Step 7) and ran pip install (Step 8) |
| `streamlit: command not found` | Type `pip install streamlit` and try again |
| Map doesn't load | Your internet must be on — OSMnx downloads real map data |
| `venv\Scripts\activate` gives error on Windows | Run: `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` then try again |

---

## Project folder structure (what each file does)

```
safewalk/
│
├── app.py            ← Main app. Controls the UI and layout
├── data_loader.py    ← Loads crime data and infrastructure data
├── danger_score.py   ← Calculates danger score for each road
├── routing.py        ← Finds safest and fastest routes using Dijkstra
├── visualizer.py     ← Draws the map with Folium
└── requirements.txt  ← List of all libraries needed
```

---

## For your project report

**Title:** Safe Route Recommender for Women Using Crime Density and Urban Infrastructure Data

**Technologies used:**
- Python 3.11
- Pandas & NumPy — data cleaning and processing
- OSMnx — road network from OpenStreetMap
- NetworkX — Dijkstra routing algorithm
- Folium — interactive geospatial maps
- Streamlit — web application interface

**Data sources:**
- NCRB 2022 Annual Report (crime data)
- OpenStreetMap (road network)
- Simulated municipal infrastructure data (street lights, CCTV)

**Algorithms:**
- Danger Score = (0.5 × normalized crime) + (0.3 × no street light) + (0.2 × no CCTV)
- Dijkstra's shortest path weighted by danger score instead of distance

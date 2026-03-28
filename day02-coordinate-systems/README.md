# 🌍 GeoAI Journey: Day 2 — CRS Mastery & PostGIS Integration

---
Welcome to **Day 2** of the GeoAI intensive. 
Today, we move from "What is on the ground" <br> (NDVI) to "Where exactly is it?" (Precision Location).
We solve the "flat earth" math problem <br>
and set up our primary spatial engine: **PostGIS.**


🎯 Day 2 Learning Objectives

- ✅ Master Coordinate Reference Systems (WGS84, UTM, Web Mercator).
- ✅ Automate UTM zone detection for any global coordinate.
- ✅ Calculate high-precision farm areas to eliminate "Basis Risk."
- ✅ Download and install PostgreSQL which includes the Stack Builder utility needed to add the PostGIS extension.

---
## 🚀 Quick Start
1) Navigate to the Day 2 Directory: 

`
cd geoai-journey/day02-coordinate-systems
`

2) Setup Environment: <br>
```   
# Use your Day1 virtual environment  

pip install -r requirements.txt
```   
 
3) Run the CRS Core Tools:

```commandline
# Explore the math of projections
python crs_explorer.py

# Convert GPS data to measurable UTM GeoJSON
python projection_converter.py

```

 
## 📁 File Structure  
``` 
day02-coordinate-systems/
├── notebooks/
│    └── day2_CRS_&_PostGIS_setup_Theory.md     ← Core concepts & math
├── outputs/                  
│    ├── dhaldabri_farms_utm.geojson            ← Projected (Meters)
│    └── dhaldabri_farms_wgs84.geojson          ← Geographic (Degrees)
├── crs_explorer.py          ← Logic for WGS84 vs UTM vs WebMerc
├── projection_converter.py  ← Production-ready CRS utility
├── README.md                ← You are here
└── requirements.txt         ← pyproj, geopandas, shapely
```

---

### 📑 Day 1 Recap: The Need for Speed
Yesterday, we built a **Satellite Data Pipeline** to calculate vegetation health (NDVI).

- **Achievement:** Mastered **NumPy Vectorization,** making our math **61x faster** than standard loops.
- **The Scale:** A full Sentinel-2 scene (120 million pixels) was reduced from 2 hours of processing to just **3 seconds.**
- **Result:** Healthy plants reflect NIR; stressed plants don't. We now have the "Health Map."

---
### 📖 Today's Core Concepts (Day 2)
1. **WGS84 (EPSG:4326)** — The GPS Standard

   - **Units:** Degrees.
   - **Best For:** Storing data and GPS location.
   - **The Flaw:** 1° of longitude shrinks as you move North. At **Dhaldabri,** it's 11% narrower than at the Equator.
   > **Never use degrees for area math.**

2. **UTM Zone 45N (EPSG:32645)** — The Measurement Engine

    - **Units:** Meters.
    - **Best For:** Accurate farm boundaries and area calculation.
    - **Logic:** Uses a flat 2D grid. We auto-detect this using: `Zone = floor((Lon + 180) / 6) + 1.`
  

3. **Web Mercator (EPSG:3857)** — The Web Map System

    - **Units:** Meters (distorted).
    - **Best For:** Fast web tile rendering and background maps (Google Maps, Mapbox).
    - **The Flaw:** Massive scale distortion near the poles. 
    While it uses "meters," they are not real-world meters. 
   At **Dhaldabri,** a farm area will be ~5% larger than reality. 
   > **Great for display, terrible for science.**


4. **PostGIS** Installation & setup — The Spatial Database <br>
We are moving beyond flat files. PostGIS allows us to treat "Geography" as a data type.

    - **Key Tool:** `ST_Transform(geom, 32645)` — Converts coordinates on-the-fly.
    - **Key Tool:** `ST_Area(geom::geography)` — Calculates real-world hectares instantly.
---
    
### 🔳 Performance Benchmark: Day 1 vs Day 2
| **Feature** | **Day 1 (NDVI)** | **Day 2 (CRS)** |
|--------|----------------|-------------|
|**Logic**|		Raster Math (Pixels)|	Vector Math (Polygons)|
|**Primary Tool**|	NumPy / Rasterio|		PyProj / GeoPandas / PostGIS|
|**Key Metric**|		Health Index (-1 to 1)|		Area Accuracy (Hectares)|
|**Optimization**|	Vectorization|	Spatial Indexing (GIST)|



### 🧑‍💻 Technical Achievements

- **Full CRS theory:** **WGS84, UTM Zone 45N, Web Mercator**
- Understood why Dhaldabri uses **EPSG:32645** (Zone 45N, not 43N)
- **Built crs_explorer.py :** Converted  Dhaldabri coordinates to UTM
- **Built projection_converter.py :** Farm area calculation in hectares
- **PostGIS:** Installed spatial database is ready.

### 📚 Key Insights

📕 CRS errors are not just technical bugs - they are financial injustice. <br>
   A farm area calculated in **wgs84** gives 9.2 hectares instead of the correct 10.3 hectares. <br>
   At Rs 5,000/ha insurance rate, that's Rs 5,500 underpaid to the farmer.

📘 When 40% floods, the farmer loses Rs 2,200 that was rightfully theirs. <br>

   This is Basis Risk - and reducing it starts with using the correct coordinate system (UTM Zone 45N for Dhaldabri).


 
### ✅Output: 

- dhaldabri_farms_wgs84.geojson
- dhaldabri_farms_utm.geojson
- Theory notes: complete CRS reference documented


 ---
 
### 📊Confidence Score:
- CRS concepts: 🟢 9/10
- pyproj/geopandas: 🟢 8.5/10
- PostGIS setup: 🟢 9.5/10

### 🪦Tomorrow - Day3: GeoPandas + PostGIS
- Load Dhaldabri farm boundaries into PostGIS.
- Write first spatial SQL queries.
- ST_Intersects, ST_Area, ST_Buffer




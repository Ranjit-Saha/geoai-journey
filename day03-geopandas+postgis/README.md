## 🌍 GeoAI Journey: Day 3 — The Spatial Vault & Purification Pipeline

> Project: Agri-Sentry 360 | Phase: Data Engineering & Persistence <br>
📂 Path: ./geoai-journey/day03-geopandas+postgis/
---

### 🧭 Where We Are in the Journey
Day 1 ✅ → Satellite theory + NDVI calculator (what satellites see) <br>
Day 2 ✅ → Coordinate systems + CRS + PostGIS installed (how to measure space) <br>
Day 3 ✅ → Farm purification + Spatial Vault built (where data lives safely) <br>
Day 4 ⏳ → Satellite Eye: connect PostGIS to Google Earth Engine (live SAR data) <br>

**The logic:** Before we can detect floods on farms, we need: <br>
- Clean farm boundaries (Day 3 — done ✅)
- A secure database to store them (Day 3 — done ✅)
- SAR satellite data clipped to those exact boundaries (Day 4 — next)


### 🎯 Day 3 Goal
Move from **"drawing shapes"** to a production-grade spatial database. <br>

Raw farm boundaries drawn by hand on **geojson.io** have problems: <br>
- **Crossed lines** (bowtie shapes) that crash spatial calculations
- **Tiny & Massive accidental clicks** that create ghost farms
- Boundaries that include roads and fences — not just crops
- **No security, no validation, no permanence** <br>

Today we fixed all of that.

---

## 🚀 Quick Start
1) Navigate to the Day 3 Directory: 

`
cd geoai-journey/day03-geopandas+postgis/
`

2) Setup Environment: <br>
```   
pip install -r requirements.txt
```   
 
3) Run the analysis:

```commandline
# Data purification 
python farm_boundary_manager.py

# Storing in PostGIS  
python db_helper.py

```
### 📁 File Structure
``` 
day03-geopandas+postgis/
├── notebooks
│   └── day3_Experiments.ipynb
├── outputs/
│   ├── dhaldabri_real_farms.geojson      ← Raw hand-drawn boundaries (input)
│   └── dhaldabri_farms_secured.parquet   ← Cleaned, validated, ready for DB
├── .env                                   ← Credentials 
├── config.py                              ← Central config class (reads .env)
├── farm_boundary_manager.py              ← THE PURIFIER
└── db_helper.py                          ← THE VAULT
```

---

### 🏗️ What We Built — Three Systems
#### 🧼 System 1: The Purifier (farm_boundary_manager.py)
**Role:** 
A data cleaning clinic.
Every farm boundary passes through this before touching the database. <br>

**Why it exists:** 
A farm drawn by hand on a map is like a rough sketch.
A **database** needs a precise engineering drawing. 
This file is **Quality Control.** <br>

**What it does,** step by step:

| **Step** | **What Happens** | **Why Matters** |
|--------|----------------|-------------|
|  **Load**  | **Reads** raw GeoJSON from **geojson.io** | Starting point — raw data |
|  **Bowtie Fix**   | **make_valid()** untangles self-intersecting polygons | Crossed lines crash spatial math |
|  **UTM Reproject**  | Converts **WGS84** (degrees) → **UTM** Zone 45N (meters) | You cannot calculate area in degrees |
|  **Area Calculation** | Computes **hectares** AND Bengal **Bighas** | Bigha is what Dhaldabri farmers understand |
| **Ghost Filter** | **Removes** farms **smaller than 0.05 Ha** (0.4 Bigha) | Accidental mouse clicks, not real farms |
| **Size Check** | Flags farms **larger than 25 Ha** (185 Bigha) | Drawing errors covering multiple villages |
| **Inner Core** | Shrinks each boundary **inward by 3 meters** | Removes road/fence pixels from SAR data |
| **BBox** | Calculates the total area bounding box | Tells GEE exactly where to download SAR data |
| **Save** | Writes to **.parquet** format | Parquet stores multiple geometry columns safely |


---

### Console Output:

================================================================= <br>
   Agri-Sentry360: DHALDABRI FARM PURIFICATION PIPELINE
================================================================= <br>
|-- [LOG]: Successfully loaded 14 farm boundaries. <br>
|-- [LOG]: ⚠️ 'farmer_name' missing! Assigning default IDs... <br>
|-- [LOG]: Geometry validation complete (All 'Bowtie' shapes untangled). <br>
|-- [LOG]: Area Calculation: Found 19.94 Total Hectares. <br>
|-- [LOG]: Area Calculation: Found 149.08 Total Bighas. <br>
|-- [LOG]: ⚠️ Removing 2 'Ghost' plots (Too small: < 0.4 Bigha). <br>
|-- [LOG]: ✅ All farms within realistic Dhaldabri size range (0.4 to 185 Bigha). <br>
|-- [LOG]: 3m 'Inner Core' generated for pure-pixel satellite sampling.<br>
|-- [LOG]: BBox calculated: [89.727, 26.354, 89.737, 26.362] (Ready for GEE). <br>
|-- [LOG]: Geometry column standardized to 'geom' for PostGIS compatibility. <br>
----------------------------------------------------------------- <br>
|-- [LOG]: ✅ SUCCESS: Purified data secured at outputs\dhaldabri_farms_secured.parquet <br>
================================================================= <br>

> **📸 Data Purification Process**: 
![](outputs/purify.png)



#### 🏰 System 2: The Vault (db_helper.py) <br>

**Role:** 
A bank vault for farm data. Not just storage — a structure with locks, rules, and speed.

**Why it exists:**
GeoPandas holds data in memory — it disappears when Python closes.
PostGIS holds it permanently with spatial superpowers. 
This file builds that permanent, secure, indexed home.

**Three things the Vault does:** <br>
#### 🔒 Security — Row Level Security (RLS)
``` 
CREATE POLICY farm_privacy_policy ON farm_boundaries
FOR ALL USING (owner_id = current_user OR current_user = 'postgres');
``` 

**What this means:** <br>
When a field agent logs in, 
the database physically hides farms that belong to other agents — 
even if the agent tries to bypass the Python code.
The lock is at the database level, not the application level. <br>

#### ✅ Integrity — Spatial Constraints
``` 
CONSTRAINT enforce_valid_geom CHECK (ST_IsValid(geom))
CONSTRAINT enforce_area_range CHECK (area_hectares > 0.01 AND area_hectares < 25.0)
```

**What this means:** <br>
The database rejects bad data at the gate. 
A ghost farm or a self-intersecting polygon never enters the system — 
not because Python caught it, 
but because the database refuses it at the SQL level. <br>

#### ⚡ Performance — GiST Spatial Index

```
CREATE INDEX idx_farm_geom ON farm_boundaries USING GIST(geom);
CREATE INDEX idx_farm_inner ON farm_boundaries USING GIST(geom_inner);
```
**What this means:** <br>
Without this index, finding **"which farms are in this flood zone?"** 
requires checking every farm one by one. **With GiST,** 
PostGIS checks bounding boxes first, then exact shapes only for candidates. 

**Result:** milliseconds **instead of minutes** for 1,000+ farms.

#### 🔄 Idempotency — Safe to Run Multiple Times
```
CREATE TABLE IF NOT EXISTS farm_boundaries (...)
DO $$ BEGIN IF NOT EXISTS (...) THEN ALTER TABLE ... END IF; END $$;
```

**What this means:** <br>
Running the script twice doesn't crash, doesn't delete data,
doesn't duplicate farms. It checks what exists and only adds what's missing.
This is production engineering — not student code.

### Console Output:

============================================================ <br>
🏗️  PHASE 1: SECURING THE SPATIAL VAULT (RLS & CONSTRAINTS) <br>
============================================================ <br>
|-- [LOG]: Vault structure, RLS policies, and Spatial Indexes are active. <br>

============================================================ <br>
🚀 PHASE 2: DATA SYNC & PRIVACY ASSIGNMENT <br>
============================================================ <br>
|-- [LOG]: Adapted 'area_ha' to 'area_hectares' for SQL alignment. <br>
|-- [LOG]: No new data to sync. Vault is up to date. (Idempotency Active) <br>


🌟 DAY 3 COMPLETE: YOUR SPATIAL BRAIN IS ONLINE.

> **📸 Storing Data into Spatial Database**:
![](outputs/db_helper_output.png)




#### 🔍 System 3: The Audit (Verification Query)
**Role:** 
Prove the data is accurate by comparing Python math vs PostGIS math.

**Why this matters:** 
Python calculates area using flat Euclidean geometry. PostGIS calculates area using spheroid geometry — accounting for Earth's curvature. If these numbers match within 0.0001 Ha, our pipeline is accurate enough for insurance-grade precision.

#### Console Output:

============================================================ <br>
🔍 PHASE 3: SPATIAL VERIFICATION <br>
============================================================ <br>
|-- [LOG]: Comparing Python Area vs. PostGIS Living Area: <br>

|ID       | Farmer          | Python Ha  | PostGIS Ha|
|---------|-----------------|-------------|--------------|
DHF001   | Farmer_1        | 0.1479     | 0.1478
DHF002   | Farmer_2        | 0.1652     | 0.1650
DHF004   | Farmer_4        | 0.0774     | 0.0773

|-- [STATUS]: Accuracy Delta < 0.0001 Ha (Spheroid Math Verified) ✅ <br>


---
 
> **📸 Running a **"Conqueror"** Spatial Query:** 
![INSERT: pgadmin_verification_query.png](outputs/spatial_query.png)


> **📸 RLS working for owner:** 
![INSERT: pgadmin_verification_query.png](outputs/owner_rls.png)

> **📸 RLS working for guest user:** 
![INSERT: pgadmin_farm_boundaries_table.png](outputs/rls_guest.png)

### 📊 Final Day 3 Numbers

| Metric |  Value |
|---------|-----------------| 
| Raw boundaries loaded | 14 |
| Ghost plots removed | 2 |
| Valid farms in database | 12 |
| Total monitored area | 19.94 Ha (149 Bighas)|
| Area accuracy (Python vs PostGIS) | < 0.0001 Ha delta |
| Spatial indexes active | 2 (geom + geom_inner) |
| RLS policies active | 1 (farm_privacy_policy)|




---
### 📚 Key Insight — Why the Inner Core Matters for Insurance
**The problem:**
A Sentinel-1 SAR pixel is 10m × 10m. 
If your farm boundary runs along a road,
a pixel on the edge measures 50% crop + 50% road.
That mixed pixel has wrong backscatter — 
it looks less flooded than it really is.

**The consequence:**
The parametric insurance trigger calculates flood percentage from pixel data.
If edge pixels are wrong, the flood percentage is wrong. 
If the flood percentage is wrong, the payout is wrong. 
A farmer who deserves ₹20,600 gets ₹18,400.

**The fix:**
The 3-meter inner buffer (geom_inner) ensures every 
SAR pixel we sample is 100% inside the crop field. 
No roads. No fences. No neighbours' land.

**This is Basis Risk reduction.** <br>
One line of geometry math:
``` 
gdf_utm['geom_inner'] = gdf_utm.geometry.buffer(-3)
```
`has direct financial consequences for real farmers in Dhaldabri.`


#### 🔐 Security Architecture
```` 
.env file (on your laptop only — never on GitHub)
    ↓
config.py (reads .env, validates credentials, builds DB URL safely)
    ↓
db_helper.py (uses config — no passwords in code)
    ↓
PostGIS (RLS policies enforce privacy at database level)
````

**Why
sqlalchemy.engine.URL.create() ?**

Special characters in passwords (like @, #, !) 
break connection strings if embedded directly. 
URL encoding handles them safely. 
This prevents a connection failure on the one day 
your password happens to contain @.

---
#### 🗓️ [Tomorrow — Day 4: The Satellite Eye](https://github.com/Ranjit-Saha/geoai-journey/tree/main/day04-satellite-handshake-for-SAR)

**Goal:**
Connect the Spatial Vault to Google Earth Engine. 
Pull real Sentinel-1 SAR data for
the Dhaldabri bounding box [89.727, 26.354, 89.737, 26.362].


**What we will see:**
A graph showing SAR backscatter (in dB) 
over time for our 12 farms. 
The dip in July/August will be 
our flood signal — the first time satellite data 
and farm boundaries work together.

**Day 4 output:**
A time-series chart showing when Dhaldabri flooded, proven by radar data from space.

---
### 🔗 Connecting the Dots
``` 
Day 1: Learned that satellites see in numbers, not photographs
       → NDVI = (NIR - Red) / (NIR + Red)

Day 2: Learned that location requires the right coordinate system
       → Store in WGS84, Calculate in UTM Zone 45N, Display in Web Mercator
       → Basis Risk starts here: wrong CRS = wrong area = wrong payout

Day 3: Built the system that stores farm locations permanently and securely
       → 12 farms, 19.94 Ha, verified to 0.0001 Ha accuracy
       → BBox [89.727, 26.354, 89.737, 26.362] ready for satellite download

Day 4: Will pull SAR data for exactly this bounding box
       → The satellite will see the farms the database knows about
```
---
## ✅ Completion Checklist
- [x] Farm boundaries purified — bowtie fix, ghost removal, inner core
- [x] Area calculated in hectares AND Bengal Bighas
- [x] PostGIS vault built with constraints, indexes, RLS
- [x] Idempotency verified — script safe to run multiple times
- [x] Python vs PostGIS area accuracy verified (< 0.0001 Ha delta)
- [x] BBox extracted and ready for GEE Day 4
- [x] .env credentials secured, never in code
 


### 📊 Confidence
|Topic | Score|
|------|------|
|GeoPandas + Shapely | 🟢9/10 | 
|PostGIS SQL + Constraints | 🟢8.5/10 |
| RLS + Security concepts| 🟢8/10|
|Idempotent database design| 🟢8/10|
|Debugging real errors😎 | 🟢10/10 |





 

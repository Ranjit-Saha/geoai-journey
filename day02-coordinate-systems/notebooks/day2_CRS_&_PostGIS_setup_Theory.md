# 🌍 THEORY - COORDINATE REFERENCE SYSTEMS

### The Problem - Earth is Not Flat
Q. Why Do We  Need Coordinate Systems?
<br>
**The Challenge:** <br>
- **Earth** is a 3D ellipsoid (a slightly squashed sphere).
- **Screens and Maps** are 2D flat rectangles.
- **The Bridge:** A **Coordinate Reference System (CRS)** is the mathematical "translator" that flattens 3D data onto 2D surfaces.
<br>


### How do we put a 3D Earth onto 2D surface?
**ANSWER:** Projections + Coordinate Reference Systems (CRS)
<br>

🌍 REAL EARTH (3D)  
<div style=" ">
         &emsp; &emsp; &emsp; ⬇️
</div>
&emsp; [PROJECTION]
<div style=" ">
         &emsp; &emsp; &emsp; ⬇️
</div>
&emsp; 🗺️ MAP (2D)  
    

----

### Key Insight: EVERY projection distorts something

- Preserve area ➡ distort shape
- Preserve shape ➡ distort area
- Preserve distance ➡ distort both

>**No perfect solution exists!**


### The Three Main Coordinate Systems You'll Use <br> 

#### A) 📖**WGS84 (EPSG:4326) - The GPS System**
    
&emsp; &emsp; &emsp; Full Name: **World Geodetic System** 1984 <br>
&emsp; &emsp; &emsp;  EPSG Code: **4326** <br>


Units: **Degrees** <br>
Example: Dhaldabri, West Bengal (26.32° N, 89.54° E)

**🪴Used By:**
 GPS devices, Google Maps, Sentinel satellites, Most Web services

**✅ Good For:** 
Global positioning, 
Storing data,
Web maps

**❌ Bad For:** 
 Area calculation,
 Distance measurement,
 Spatial analysis

> ###### Why it's bad for area: 
> 1 degree longitude at equator = 111 km <br>
> 1 degree longitude at Dhaldabri = 99 km  ⬅ Different! <br>
> 1 degree longitude at North Pole = 0 km  ⬅ Shrinks to zero!

A *"square"* in degrees is  NOT actually *square* on Earth! 
``
1 degree longitude at equator = 111 km
1 degree longitude at Dhaldabri = 99 km ⬅ Narrower!
1 degree longitude at North Pole = 0 km ⬅ Collapsed!
``
____

####  B) 📖**UTM (Universal Transverse Mercator) - The Measurement System**

&emsp; &emsp; &emsp; Full Name: **Universal Transverse Mercator** <br>
&emsp; &emsp; &emsp; EPSG Code: **Depends on zone (Dhaldabri = EPSG:32645)** <br>

Units: **Meters** <br>
Example: Dhaldabri, West Bengal <br>
- **Easting:** 698,234 m
- **Northing:** 2,914,567 m
- **Zone:** 45N


**❓How It Works:**
- Earth divided into 60 vertical zones (each 6° wide)
- Zone 1: 180° W to 174° W
- Zone 45: 84° E to 90° E ⬅️Dhaldabri is here!
- Each zone has its own coordinate system

**✅ Good For:** 
  Area calculation,
  Distance measurement,
  Engineering work,  
  Farm surveys


**❌ Bad For:** Global mapping, Web Display, Cross-zone analysis

> ###### Finding Your UTM Zone:
> **Formula:** `Zone = floor((Longitude + 180) / 6) + 1` <br>
**Full EPSG Code:** 326 + Zone Number = **32645** (326 = Northern Hemisphere prefix).


Formula: **Zone = floor((Longitude + 180) / 6) + 1** <br>
Dhaldabri Longitude = 89.5458° E <br>
**Zone Number** = floor((89.5458 + 180) / 6) + 1 <br>
&emsp; &emsp;  = floor(269.5458 / 6) + 1 <br>
&emsp; &emsp;  = floor(44.92) + 1 <br>
&emsp; &emsp;  = 44 + 1 <br>
&emsp; &emsp;  = 45

**Full EPSG Code:** 326 + Zone Number = **32645** <br>
(326 = UTM North prefix)

----

####   C) 📖**Web Mercator (EPSG:3857) - The Web Map System**

&emsp; &emsp; Full Name: **Web Mercator / Pseudo-Mercator** <br>
&emsp; &emsp; EPSG Code: **3857** <br>

Units: **Meters** (but highly distorted!)  <br>
Example: Dhaldabri  <br>
- **X:** 9,957,234 m
- **Y:** 3,012,456 m

**🪴Used By:**
Google Maps, Open StreetMap, Mapbox, Leaflet, Most web mapping libraries,


**✅ Good For:** Web tile rendering (fast!), Consistent zoom levels, Square tiles (256x256px)

**❌ Bad For:** Area calculation (very distorted), High latitudes (Greenland looks huge!), Scientific analysis

**Fun Fact:** <br>
- **Greenland** looks same size as Africa in Web Mercator
- **Reality:** Africa is 14x bigger than Greenland!

----
### 🌾Real-World Example: Farm Area Calculation

**Scenario:**
Farmers in Dhaldabri has a rectangular farm <br>

| **Coordinate System** | **Calculated Area** | **Reality** |
|-------------------|-----------------|----------|
|WGS84 (degrees)    | 8.7 "squqre degrees"| ❌ Meaningless|
|WGS84 (native conversion)    | 9.2 hectares| ❌ Wrong (11% error)|
|**UTM Zone 45N***    | **10.3 hectares**| **✅ Correct**|
|Web Mercator    | 10.8 hectares| ❌ Wrong (5% error)|

Consequence for Insurance: <br>
- **Correct Premium:**  10.3 ha @ ₹5,000 = **₹51,500** <br>
- **If calculated in WGS84:** 9.2 ha @ ₹5,000 = **₹46,000** 
- **📉 The Result:** The farmer is under-insured and loses ₹5,500 due to bad math. This is **BASIS RISK.**


----
### How Computers Store Geography
#### 1) What is a **Shapefile**? <br>

A collection of files that must stay together: <br>
- `.shp`: Geometry (points/polygons)
- `.shx`: Index for fast access
- `.dbf`: Attribute data (farm names/IDs)
- `.prj`: Projection/CRS info (The "Identity Card") <br>

**Modern Alternatives:** <br>
**GeoJSON** (Used in your code), GeoPackage, GeoParquet.

#### 2) How is a **Polygon Stored? (WKT Format)**
A farm is stored as a series of coordinates that "close" at the start: <br>
`POLYGON ((89.545 26.325, 89.546 26.325, 89.546 26.324, 89.545 26.325))`

**Draw the shape:** <br>
&emsp;&emsp;A ------------------- B <br>
 &emsp;&emsp;&emsp;&emsp;  |   &emsp;&emsp;&emsp;&emsp;   |
<br>&emsp;&emsp;&emsp;&emsp;  |  &ensp; FARM&ensp;  |
<br>&emsp;&emsp;&emsp;&emsp;  |   &emsp;&emsp;&emsp;&emsp;   |
<br>&emsp;&emsp;&emsp;&emsp;  D ----------  C

#### 3) **What is PostGIS?**
An extension for **PostgreSQL** that adds "Spatial Intelligence."

- **Standard DB:** "Find farms where owner = 'Ranjit'"
- **PostGIS DB:** "Find farms within 500m of the flood zone"
- **Key Functions:** `ST_Area(), ST_Transform(), ST_Intersects().`

----
 
>To set up PostGIS on Windows, you first need to download and install **PostgreSQL**, which includes the **Stack Builder** utility needed to add the **PostGIS** extension.

### 1. Download PostgreSQL
Visit the https://www.enterprisedb.com/downloads/postgres-postgresql-downloads
- Select the latest stable version (e.g., PostgreSQL 18.3) for the **Windows x86-64** platform.
- The installer includes the database server, **pgAdmin 4** (management tool), and **Stack Builder.**

### 2. Install PostgreSQL
- Run the `.exe` installer and follow the wizard.
- **Components:** Ensure **Stack Builder** is checked before clicking **"Next".**
- **Password:** You will be prompted to set a password for the `postgres` superuser.
- **Remember this password**, as you will need it to connect later.
- Accept default settings for the port (**5432**) and locale.

### 3. Use Stack Builder to Install PostGIS
Once the main installation is finished, the **Stack Builder** will launch automatically (or you can find it in your **Start menu.**)

1. **Select Server:** Choose your installed PostgreSQL server from the dropdown list and click **Next**.
2. **Select PostGIS:** Expand the **Spatial Extension** category.
3. **Check PostGIS:** Tick the box for the latest **PostGIS 3.X Bundle** and click **Next.**
4. **Download & Install:** Stack Builder will download the files. Once ready, it will launch the PostGIS setup wizard. Follow the prompts (usually defaults) to complete the spatial installation.

### 4. Verify the Installation
Open **pgAdmin 4** from your Start menu and run this SQL command in the Query Tool to enable the extension in your database:
``` 
CREATE EXTENSION postgis;
SELECT postgis_full_version()

```
If you see the version details, your spatial database is ready.

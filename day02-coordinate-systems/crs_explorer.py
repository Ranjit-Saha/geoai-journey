# day02-coordinate-systems/crs_explorer.py
"""
Day 2: Coordinate Reference Systems
    - The #1 silent bug in geospatial code is mismatched CRS.
    - Understanding this is non-negotiable.
"""
# ===================================================================================
# ---- PART 1: The Three Systems You Must Know ----
# ===================================================================================
from pyproj import CRS, Transformer
import math

print("=" * 50)
print("DAY 2: COORDINATE REFERENCE SYSTEMS")
print("=" * 50)

print("\n(1) The three CRS you will use every day...")

# GPS coordinates: Degrees (Latitude/Longitude):-
wgs84 = CRS.from_epsg(4326)

# UTM Zone 45N: Meters (Correct for Coochbehar, West Bengal), Measuring distance & area:-
utm45 = CRS.from_epsg(32645)

# Web Mercator: Meters (distorted) Standard for web tiles used by Google Maps/Mapbox:-
web = CRS.from_epsg(3857)

print(f"  WGS84 (EPSG:4326) Units: {wgs84.axis_info[0].unit_name}")
print(f"  WGS84 (EPSG:4326) Unit code: {wgs84.axis_info[0].unit_code}")

print(f"  UTM 45N (EPSG:32645) Units: {utm45.axis_info[0].unit_name}")
print(f"  UTM 45N (EPSG:32645) Unit code: {utm45.axis_info[0].unit_code}")

print(f"  WebMerc (EPSG:3857) Units: {web.axis_info[0].unit_name}")
print(f"  WebMerd (EPSG:3857) Unit code: {web.axis_info[0].unit_code}")

# ========================================================================================
# ---- PART 2: Convert Dhaldabri coordinates ----
# =========================================================================================
print("\n(2) Converting Dhaldabri, West Bengal coordinates...")

# Dhaldabri approximate coordinates:-
dhaldabri_lat = 26.3577
dhaldabri_lon = 89.7303

print(f" Dhhaldabri (WGS84): Lat= {dhaldabri_lat}, Long= {dhaldabri_lon}")

transformer = Transformer.from_crs("EPSG:4326", "EPSG:32645", always_xy=True)
x, y = transformer.transform(dhaldabri_lon, dhaldabri_lat)
print(f" After conversion, Dhaldabri (UTM 45N): x= {x:.2f}m, y= {y:.2f}m")

# ========================================================================================
# ---- PART 3: Why Area Calculation MUST use UTM ----
# =========================================================================================
print("\n(3) Why area calculation must use UTM, not WGS84...")

# A farm 0.01 degrees x 0.01 degrees near Dhaldabri:-
area_degrees = 0.01 * 0.01
print(f" Farm size in degrees squired: {area_degrees} (MEANINGLESS)")

# Same farm in meters using UTM
# At latitude 26.3577N:
#    1° latitude = 111,000m
#    1° longitude = 111,000 * cos(26.3577°)  = 99,460m

lat_rad = math.radians(dhaldabri_lat)

meters_per_deg_lat = 111_000
meters_per_deg_lon = 111_000 * math.cos(lat_rad)

area_m2 = (0.01 * meters_per_deg_lat) * (0.01 * meters_per_deg_lon)
area_hectares = area_m2 / 10_000

print(f" Same farm in square meters: {area_m2:.0f} m2")
print(f" Same farm in hectares: {area_hectares:.2f} ha")
print(
    f" Average Dhaldabri farm = 0.77 ha - does this match? {'YES' if 0.5 < area_hectares < 1.5 else 'Check coordinates'}")

# ========================================================================================
# ---- PART 4: Auto-detect UTM Zone ----
# =========================================================================================
print("\n(4) Auto-detecting correct UTM Zone for any coordinate... ")


def detect_utm_zone(lon, lat):
    zone_number = int((lon + 180) / 6) + 1
    epsg = 326_00 + zone_number if lat >= 0 else 327_00 + zone_number

    return epsg

    """
    Why 180? Longitude goes from -180° to +180°. Adding 180 shifts it to a 0° to 360° range.
    Why 6? The Earth is divided into 60 zones, each 6° wide (360/6  = 60) 
    Why +1? Python's int() or floor function starts at 0, but UTM Zones are numbered 1 to 60.
    """


test_locations = [
    ("Dhaldabri, West Bengal", 89.7303, 26.3577),
    ("Bangalore, Karnataka", 77.59, 12.97),
    ("Mumbai, Maharashtra", 72.87, 19.07),
    ("Chennai, Tamil Nadu", 80.27, 13.08)
]

for name, lon, lat in test_locations:
    epsg = detect_utm_zone(lon, lat)
    print(f" {name}: EPSG: {epsg}N")

# ========================================================================================
# ---- PART 5: The Golden Rule ----
# =========================================================================================
print("\n" + "=" * 50)
print("THE GOLDEN RULE - MEMORISE THIS:")
print("=" * 50)

print("""
STORE data in WGS84 (EPSG:4326) - GPS degrees
CALCULATE in UTM (EPSG:32645) - meters for India
DISPLAY in Web Mercator (EPSG:3857) - for Mapbox/web maps

Breaking this rule = silent wrong answers.
A farm's area calculated in degrees is meaningless.
""")

print("=" * 50)
print("KEY INSIGHT FOR INTERVIEWS:")
print("=" * 50)
print("""
When asked 'Why PostGIS over plain PostgreSQL?'
Part of the answer is: PostGIS stores geometries in WGS84
and can re-project on-the-fly to UTM for accurate area calculations using ST_Area(geom::geography).
This is impossible in plain PostgreSQL.""")
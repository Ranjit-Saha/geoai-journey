# day02-coordinate-systems/projection_converter.py
"""
Day 2: Projection Converter Tool
This becomes src/data/preprocessing/crs_utils.py in Agri-Sentry360
"""
from pyproj import CRS, Transformer
import geopandas as gpd
from shapely.geometry import Point, Polygon
import math


def detect_utm_zone(lon: float, lat: float) -> int:
    zone = int((lon + 180) / 6) + 1

    return 326_00 + zone if lat >= 0 else 327_00 + zone

    """
     lon: float, lat: float  Tells Python to expect decimal number (e.g., 89.73, 26.35)
      -> int: Tells Python the result will be whole number (the EPSG code)
    """


def convert_point(lat: float, lon: float, target_epsg: int) -> tuple:
    transformer = Transformer.from_crs("EPSG:4326", f" EPSG: {target_epsg}", always_xy=True)
    x, y = transformer.transform(lon, lat)

    return x, y


def convert_farm_boundaries(farm_wgs84: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Re-project to UTM for accurate area calculation."""

    centroid = farm_wgs84.geometry.iloc[0].centroid
    utm_epsg = detect_utm_zone(centroid.x, centroid.y)
    print(f" Auto-detected UTM Zone:  EPSG: {utm_epsg}")

    farms_utm = farm_wgs84.to_crs(epsg=utm_epsg)
    farms_utm['area_hectares'] = farms_utm.geometry.area / 10_000

    return farms_utm


print("=" * 50)
print("PROJECTION CONVERTER TOOL")
print("=" * 50)

# Test with farms near Dhaldabri (Coochbehar district)
print("\n1. Sample farm locations near Dhaldabri...")
test_farms = [
    ("Dhaldabri Farm A", 26.350, 89.450),
    ("Dhaldabri Farm B", 26.358, 89.462),
    ("Dhaldabri Farm C", 26.314, 89.438)
]

for name, lat, lon in test_farms:
    utm_epsg = detect_utm_zone(lon, lat)
    x, y = convert_point(lat, lon, utm_epsg)

    print(f" {name}: ({lat}, {lon}) -> UTM ({x:.0f}m, {y:.0f}m)")

# Test farm polygon area calculation
print("\n2. Farm boundary area calculation...")
farm_polygons = [
    Polygon([(89.450, 26.350), (89.458, 26.350), (89.458, 26.357), (89.450, 26.357)]),
    Polygon([(89.462, 26.358), (89.470, 26.358), (89.470, 26.365), (89.462, 26.365)])
]

farms = gpd.GeoDataFrame(
    {'farm_id': ['DHF001', 'DHF002'], 'crop': ['rice', 'jute']},
    geometry=farm_polygons, crs="EPSG:4326"
)

farms_utm = convert_farm_boundaries(farms)
print(f"\n Farm areas (UTM projection - accurate):")
for _, row in farms_utm.iterrows():
    print(f" {row['farm_id']} ({row['crop']}): {row['area_hectares']:.3f} hectares")

# Save outputs
farms.to_file("outputs/dhaldabri_farms_wgs84.geojson", driver='GeoJSON')
farms_utm.to_file("outputs/dhaldabri_farms_utm.geojson", driver='GeoJSON')
print("\n ✅Saved: dhaldabri_farms_wgs84.geojson and dhaldabri_farms_utm.geojson")
print("\n Next step: These farm polygon go into PostGIS in Day3")

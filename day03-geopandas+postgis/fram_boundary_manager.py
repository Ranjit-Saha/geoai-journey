# farm_boundary_manager.py
"""
Day3 :
- The Purifier
- Think of this file as a data cleaning clinic.
- Real farm boundaries drown by hand on a map have errors -
    -  Crossed lines
    -  Tiny silvers
    -  Roads included by mistake
- This file (farm_boundary_manager.py) fixes all of that before the data ever
- touches the database, this file is the Quality control step.

"""


import os
import geopandas as gpd
from shapely.geometry import box
from shapely.validation import make_valid
import pandas as pd


# --- HELPER: Professional Logging ---
def log_step(msg):
    """Internally works as a formatted print for clean terminal output."""
    print(f"|-- [LOG]: {msg}")


def purify_farms(input_path="outputs/dhaldabri_real_farms.geojson", output_dir="outputs"):
    print("=" * 65)
    print("   Agri-Sentry360: DHADLABRI FARM PURIFICATION PIPELINE")
    print("=" * 65)

    # Ensure output workspace exists
    os.makedirs(output_dir, exist_ok=True)

    # --- STEP 1: LOAD DATA ---
    if not os.path.exists(input_path):
        # log_step(f"❌ Error: Input file {input_path} not found. Create the farm boundaries from 'geojson.io' ")
        # return None
        # This will print the EXACT path PyCharm is looking at
        full_path = os.path.abspath(input_path)
        log_step(f"❌ Error: Looking for file at {full_path} but it's not there!")
        return None

    gdf = gpd.read_file(input_path)
    log_step(f"Successfully loaded {len(gdf)} farm boundaries.")

    # Assigning farmer name's & farm id's
    if 'farmer_name' not in gdf.columns:
        log_step("⚠️'farmer_name' missing! Assigning default IDs...")
        gdf['farmer_name'] = [f"Farmer_{i + 1}" for i in range(len(gdf))]
        gdf['farm_id'] = [f"DHF{i + 1:03d}" for i in range(len(gdf))]

    # --- STEP 2: GEOMETRY VALIDATION ("The Bowtie Fix") ---
    # Fixes self-intersections and topological errors
    gdf['geometry'] = gdf['geometry'].apply(
        lambda geom: make_valid(geom) if not geom.is_valid else geom
    )
    log_step("Geometry validation complete (All 'Bowtie' shapes untangled).")

    # --- STEP 3: ACCURATE SPATIAL MATH (UTM Zone 45N) ---
    # Convert to Meters (EPSG:32645) for precise West Bengal calculations
    gdf_utm = gdf.to_crs(epsg=32645)

    raw_area_m2 = gdf_utm.geometry.area
    gdf['area_bigha'] = (raw_area_m2 / 1337.805).round(4)  # Bengal Bigha
    gdf['area_ha'] = (raw_area_m2 / 10_000).round(4)

    log_step(f"Area Calculation: Found {gdf['area_ha'].sum():.2f} Total Hectares.")
    log_step(f"Area Calculation: Found {gdf['area_bigha'].sum():.2f} Total Bighas.")

    # --- STEP 3.5: SANITY FILTERS (Tiny vs. Massive) ---
    # Define thresholds in Hectares (the math standard)
    MIN_AREA_HA = 0.05
    MAX_AREA_HA = 25.0

    # Find the troublemakers
    tiny_farms = gdf[gdf['area_ha'] < MIN_AREA_HA]
    massive_farms = gdf[gdf['area_ha'] > MAX_AREA_HA]

    if not tiny_farms.empty:
        # Link Bigha in the log so the user understands the scale
        # (0.05 Ha is roughly 0.37 Bigha)
        log_step(f"⚠️ Removing {len(tiny_farms)} 'Ghost' plots (Too small: < 0.4 Bigha).")
        gdf = gdf[gdf['area_ha'] >= MIN_AREA_HA]

    if not massive_farms.empty:
        # 25 Ha is roughly 187 Bigha
        log_step(f"❌ ALERT: Found {len(massive_farms)} massive plots (> 185 Bigha).")
        log_step("   -> These will be flagged for manual verification.")
        gdf['is_outlier'] = gdf['area_ha'] > MAX_AREA_HA
    else:
        log_step("✅ All farms within realistic Dhaldabri size range (0.4 to 185 Bigha).")

    # --- STEP 4: PRECISION LAYER (Inner Core) ---
    # Shrink inward by 3m to remove "Edge Noise" (roads, fences) for SAR data
    gdf_utm['geom_inner'] = gdf_utm.geometry.buffer(-3)
    gdf['geom_inner'] = gdf_utm['geom_inner'].to_crs(epsg=4326)  # Back to Degrees
    log_step("3m 'Inner Core' generated for pure-pixel satellite sampling.")

    # --- STEP 5: PROJECT BOUNDING BOX (BBOX) ---
    # This is the "Satellite Window" for Day 4
    total_bounds = gdf.total_bounds
    log_step(f"BBox calculated: {total_bounds.tolist()} (Ready for GEE).")

    # --- STEP 6: PREPARE FOR POSTGIS ---
    # Database standard: rename 'geometry' column to 'geom'
    gdf = gdf.rename_geometry('geom')
    log_step("Geometry column standardized to 'geom' for PostGIS compatibility.")

    # --- STEP 7: SECURE STORAGE ---
    # Parquet is used because it can store multiple geometry columns securely
    output_parquet = os.path.join(output_dir, "dhaldabri_farms_secured.parquet")
    gdf.to_parquet(output_parquet)

    print("-" * 65)
    log_step(f"✅ SUCCESS: Purified data secured at {output_parquet}")
    print("=" * 65)

    return gdf, total_bounds


# --- MAIN EXECUTION ---
if __name__ == "__main__":
    # This triggers the purification process
    final_gdf, bbox = purify_farms()

    # Preview the data for the developer
    print("\nPreview of Purified Data (First 2 Rows):")
    print(final_gdf[['farm_id', 'farmer_name', 'area_bigha', 'area_ha']].head(2))


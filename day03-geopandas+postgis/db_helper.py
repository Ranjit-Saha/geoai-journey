# db_helper.py | db_helper.py

import os
import pandas as pd
import geopandas as gpd
from sqlalchemy import create_engine, text
from geoalchemy2 import Geometry
from config import Config  # <-- The Central Brain

# ARCHITECT'S NOTE: We use a connection pool to handle concurrent Day 4 satellite requests
engine = create_engine(Config.DB_URL, pool_size=10, max_overflow=20)


def ensure_vault_exists():
    """
    ARCHITECTURE: Implements an 'Idempotent' setup.
    Checks for the table, constraints, and privacy policies without
    destroying existing farmer data.
    """
    print(f"\n{'=' * 60}\n🏗️  PHASE 1: SECURING THE SPATIAL VAULT (RLS & CONSTRAINTS)\n{'=' * 60}")

    setup_sql = """
    CREATE EXTENSION IF NOT EXISTS postgis;

    -- 1. Create basic table if it doesn't exist
    CREATE TABLE IF NOT EXISTS farm_boundaries (
        farm_id         VARCHAR(20) PRIMARY KEY,
        farmer_name     VARCHAR(50) NOT NULL,
        owner_id        VARCHAR(50) DEFAULT 'postgres' NOT NULL, 
        crop_type       VARCHAR(50),
        area_hectares   DECIMAL(10, 4),
        area_bigha      DECIMAL(10, 4),
        geom            GEOMETRY(POLYGON, 4326),
        geom_inner      GEOMETRY(POLYGON, 4326),
        created_at      TIMESTAMP DEFAULT NOW()
    );

    -- 2. Migration: Add owner_id and Constraints to existing table if missing
    DO $$ 
    BEGIN 
        -- Add owner_id if missing
        IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                       WHERE table_name='farm_boundaries' AND column_name='owner_id') THEN
            ALTER TABLE farm_boundaries ADD COLUMN owner_id VARCHAR(50) DEFAULT 'postgres' NOT NULL;
        END IF;

        -- Add valid_geom constraint if missing
        IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'enforce_valid_geom') THEN
            ALTER TABLE farm_boundaries ADD CONSTRAINT enforce_valid_geom CHECK (ST_IsValid(geom));
        END IF;

        -- Add area_range constraint if missing
        IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'enforce_area_range') THEN
            ALTER TABLE farm_boundaries ADD CONSTRAINT enforce_area_range 
            CHECK (area_hectares > 0.01 AND area_hectares < 25.0);
        END IF;
    END $$;

    -- 3. Security & Privacy
    ALTER TABLE farm_boundaries ENABLE ROW LEVEL SECURITY;

    DO $$
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM pg_policy WHERE polname = 'farm_privacy_policy') THEN
            CREATE POLICY farm_privacy_policy ON farm_boundaries
            FOR ALL USING (owner_id = current_user OR current_user = 'postgres');
        END IF;
    END $$;

    -- 4. Indexes
    CREATE INDEX IF NOT EXISTS idx_farm_geom ON farm_boundaries USING GIST(geom);
    CREATE INDEX IF NOT EXISTS idx_farm_inner ON farm_boundaries USING GIST(geom_inner);
    """

    with engine.connect() as conn:
        conn.execute(text(setup_sql))
        conn.commit()
    print("|-- [LOG]: Vault structure, RLS policies, and Spatial Indexes are active.")


def sync_farms(input_file="outputs/dhaldabri_farms_secured.parquet"):
    """
    ARCHITECTURE: Syncs new data with 'Owner' assignment.
    Prevents duplicates while respecting the security schema.
    """
    print(f"\n{'=' * 60}\n🚀 PHASE 2: DATA SYNC & PRIVACY ASSIGNMENT\n{'=' * 60}")

    if not os.path.exists(input_file):
        return print(f"|-- [ERROR]: {input_file} missing.")

    # 1. Load the data
    gdf = gpd.read_parquet(input_file)

    # 2. THE PRO ADAPTATION: Only rename if the old name exists
    if 'area_ha' in gdf.columns:
        gdf = gdf.rename(columns={'area_ha': 'area_hectares'})
        print("|-- [LOG]: Adapted 'area_ha' to 'area_hectares' for SQL alignment.")
    elif 'area_hectares' in gdf.columns:
        print("|-- [LOG]: 'area_hectares' already aligned. No renaming needed.")
    else:
        # If neither exists, we have a data integrity problem!
        raise KeyError("❌ CRITICAL: No area column found in the Parquet file!")

    # ASSIGN OWNER:
    gdf['owner_id'] = Config.DB_USER

    # Filter out existing farms to maintain 'Idempotency'
    with engine.connect() as conn:
        existing_ids = pd.read_sql("SELECT farm_id FROM farm_boundaries", conn)['farm_id'].tolist()

    new_farms = gdf[~gdf['farm_id'].isin(existing_ids)]

    if new_farms.empty:
        print("|-- [LOG]: No new data to sync. Vault is up to date.")
        return

    spatial_dtypes = {
        "geom": Geometry("POLYGON", srid=4326),
        "geom_inner": Geometry("POLYGON", srid=4326)
    }

    new_farms.to_postgis(
        name="farm_boundaries",
        con=engine,
        if_exists="append",
        index=False,
        dtype=spatial_dtypes
    )
    print(f"|-- [LOG]: ✅ {len(new_farms)} new farms secured with RLS.")


if __name__ == "__main__":
    ensure_vault_exists()
    sync_farms()
    print("\n🌟 DAY 3 COMPLETE: THE FORTRESS IS SECURED.")

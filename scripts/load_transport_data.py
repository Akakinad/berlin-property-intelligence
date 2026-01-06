"""
Load Public Transport Data to Berlin Intelligence Database

Maps transport stops to districts using spatial join with district boundaries.
"""

import pandas as pd
import geopandas as gpd
import sqlite3
from pathlib import Path

# Paths
DATA_DIR = Path("data")
DB_PATH = Path("database/berlin_intelligence.db")

print("="*70)
print("🚇 LOADING TRANSPORT DATA TO DATABASE")
print("="*70)

# ============================================================================
# STEP 1: Load District Boundaries
# ============================================================================
print("\n📍 Step 1: Loading district boundaries...")

districts_gdf = gpd.read_file(DATA_DIR / "districts_neighborhoods/bezirksgrenzen_berlin.geojson")
print(f"   ✅ Loaded {len(districts_gdf)} district boundaries")

# Find district name column
print(f"   Available columns: {list(districts_gdf.columns)}")

if 'Gemeinde_name' in districts_gdf.columns:
    district_col = 'Gemeinde_name'
elif 'name' in districts_gdf.columns:
    district_col = 'name'
else:
    district_col = input("   Enter the district name column: ")

print(f"   ✅ Using '{district_col}' for district names")

# ============================================================================
# STEP 2: Load Transport Stops
# ============================================================================
print("\n🚇 Step 2: Loading transport stops...")

stops_df = pd.read_csv(DATA_DIR / "public_transport/cleaned_stops.csv")
print(f"   ✅ Loaded {len(stops_df):,} transport stops")

# Convert to GeoDataFrame
stops_gdf = gpd.GeoDataFrame(
    stops_df,
    geometry=gpd.points_from_xy(stops_df.stop_lon, stops_df.stop_lat),
    crs="EPSG:4326"
)

# ============================================================================
# STEP 3: Spatial Join - Map Stops to Districts
# ============================================================================
print("\n🔄 Step 3: Mapping stops to districts (this may take 30-60 seconds)...")

# Ensure same CRS
if districts_gdf.crs != stops_gdf.crs:
    districts_gdf = districts_gdf.to_crs(stops_gdf.crs)

# Spatial join
stops_with_district = gpd.sjoin(
    stops_gdf, 
    districts_gdf[[district_col, 'geometry']], 
    how='left', 
    predicate='within'
)

# Count results
mapped_count = stops_with_district[district_col].notna().sum()
unmapped_count = len(stops_df) - mapped_count

print(f"   ✅ Mapped: {mapped_count:,}/{len(stops_df):,} stops ({mapped_count/len(stops_df)*100:.1f}%)")
if unmapped_count > 0:
    print(f"   ⚠️  Unmapped: {unmapped_count:,} stops (outside Berlin boundaries)")

# ============================================================================
# STEP 4: Prepare Data for Database
# ============================================================================
print("\n📊 Step 4: Preparing transport data...")

# Keep only mapped stops
transport_stops = stops_with_district[stops_with_district[district_col].notna()].copy()

# Select columns
transport_stops = transport_stops[[
    'stop_id', 'stop_name', 'stop_lat', 'stop_lon', 
    'zone_id', 'wheelchair_boarding', district_col
]]

# Rename district column
transport_stops = transport_stops.rename(columns={district_col: 'district'})

print(f"   ✅ Prepared {len(transport_stops):,} stops for database")

# Show sample
print("\n   Sample data:")
print(transport_stops.head(3).to_string(index=False))

# ============================================================================
# STEP 5: Add to Database
# ============================================================================
print("\n💾 Step 5: Adding to database...")

conn = sqlite3.connect(DB_PATH)

# Add transport stops table
transport_stops.to_sql('public_transport_stops', conn, if_exists='replace', index=False)
print(f"   ✅ Created 'public_transport_stops' table with {len(transport_stops):,} records")

# Calculate district-level metrics
print("\n📈 Step 6: Calculating transport metrics per district...")

transport_metrics = transport_stops.groupby('district').agg({
    'stop_id': 'count',
    'wheelchair_boarding': lambda x: (x == 1).sum()
}).reset_index()
transport_metrics.columns = ['district', 'transport_stops_count', 'wheelchair_accessible_stops']

# Add to database
transport_metrics.to_sql('district_transport_metrics', conn, if_exists='replace', index=False)
print(f"   ✅ Created 'district_transport_metrics' table for {len(transport_metrics)} districts")

# Show summary
print("\n📊 Transport Metrics Summary:")
print(transport_metrics.sort_values('transport_stops_count', ascending=False).to_string(index=False))

conn.close()

print("\n" + "="*70)
print("✅ TRANSPORT DATA LOADED SUCCESSFULLY!")
print("="*70)
print("\n🎯 Next: Run load_school_data.py")
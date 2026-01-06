
"""
Load School Data to Berlin Intelligence Database
Maps schools from neighborhoods to districts (12 main districts)
"""

import pandas as pd
import sqlite3
from pathlib import Path

# Paths
DATA_DIR = Path("data")
DB_PATH = Path("database/berlin_intelligence.db")

print("="*70)
print("🏫 LOADING SCHOOL DATA TO DATABASE")
print("="*70)

# ============================================================================
# STEP 1: Load Neighborhood → District Mapping
# ============================================================================
print("\n📍 Step 1: Loading neighborhood-district mapping...")

mapping_df = pd.read_csv(DATA_DIR / "districts_neighborhoods/neighborhoods_enhanced.csv")
mapping = mapping_df[['neighborhood', 'district']].drop_duplicates()
print(f"   ✅ Loaded mapping for {len(mapping)} neighborhoods → {mapping['district'].nunique()} districts")

# ============================================================================
# STEP 2: Load Schools Data
# ============================================================================
print("\n📚 Step 2: Loading schools data...")

schools_df = pd.read_csv(DATA_DIR / "schools/berlin_schools.csv")
print(f"   ✅ Loaded {len(schools_df):,} schools")

# ============================================================================
# STEP 3: Map Schools to Districts
# ============================================================================
print("\n🔄 Step 3: Mapping schools from neighborhoods to districts...")

# Schools have 'quarter' = neighborhood name
schools_clean = schools_df[[
    'bsn', 'school_name', 'school_type_de', 'ownership_en',
    'quarter', 'neighborhood', 'longitude', 'latitude',
    'students_total', 'teachers_total'
]].copy()

# Rename quarter to neighborhood for mapping
schools_clean = schools_clean.rename(columns={'quarter': 'neighborhood_name'})

# Map to districts
schools_clean = schools_clean.merge(
    mapping,
    left_on='neighborhood_name',
    right_on='neighborhood',
    how='left'
)

# Handle missing values
schools_clean['students_total'] = pd.to_numeric(schools_clean['students_total'], errors='coerce').fillna(0).astype(int)
schools_clean['teachers_total'] = pd.to_numeric(schools_clean['teachers_total'], errors='coerce').fillna(0).astype(int)

# Check mapping success
mapped = schools_clean['district'].notna().sum()
print(f"   ✅ Mapped {mapped}/{len(schools_clean)} schools to districts")

if mapped < len(schools_clean):
    unmapped = len(schools_clean) - mapped
    print(f"   ⚠️  {unmapped} schools couldn't be mapped")

# Keep only mapped schools
schools_clean = schools_clean[schools_clean['district'].notna()].copy()

print(f"   ✅ Prepared {len(schools_clean):,} schools for database")
print(f"   Districts: {schools_clean['district'].nunique()}")

# Show sample
print("\n   Sample data:")
sample = schools_clean[['school_name', 'neighborhood_name', 'district', 'students_total', 'teachers_total']].head(3)
print(sample.to_string(index=False))

# ============================================================================
# STEP 4: Add to Database
# ============================================================================
print("\n💾 Step 4: Adding to database...")

conn = sqlite3.connect(DB_PATH)

# Prepare schools table (remove redundant neighborhood column from mapping)
schools_final = schools_clean[[
    'bsn', 'school_name', 'school_type_de', 'ownership_en',
    'district', 'neighborhood_name', 'longitude', 'latitude',
    'students_total', 'teachers_total'
]].copy()
schools_final = schools_final.rename(columns={'neighborhood_name': 'neighborhood'})

# Add schools table
schools_final.to_sql('schools', conn, if_exists='replace', index=False)
print(f"   ✅ Created 'schools' table with {len(schools_final):,} records")

# Calculate district-level metrics
print("\n📈 Step 5: Calculating school metrics per district...")

school_metrics = schools_clean.groupby('district').agg({
    'bsn': 'count',
    'students_total': 'sum',
    'teachers_total': 'sum'
}).reset_index()
school_metrics.columns = ['district', 'schools_count', 'total_students', 'total_teachers']

# Add to database
school_metrics.to_sql('district_school_metrics', conn, if_exists='replace', index=False)
print(f"   ✅ Created 'district_school_metrics' table for {len(school_metrics)} districts")

# Show summary
print("\n📊 School Metrics Summary:")
print(school_metrics.sort_values('schools_count', ascending=False).to_string(index=False))

conn.close()

print("\n" + "="*70)
print("✅ SCHOOL DATA LOADED SUCCESSFULLY!")
print("="*70)
print("\n🎯 Next: Ready for Notebook 07 - Transport & School Analysis!")

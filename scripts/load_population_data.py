
"""
Load Berlin Population Statistics into Database
Enables per capita crime rate calculations
"""

import sqlite3
import pandas as pd
import os

# Paths
DB_PATH = "database/berlin_intelligence.db"
POP_DATA_PATH = "data/population_statistics/Berlin_pop_stats - berlin-neighborhood-population-updated.csv"

def load_population_data():
    """Load population statistics into database"""
    print("=" * 60)
    print("📊 LOADING POPULATION DATA")
    print("=" * 60)
    
    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    
    # Load CSV
    print(f"\n📂 Loading: {POP_DATA_PATH}")
    df = pd.read_csv(POP_DATA_PATH, dtype={'district_id': str})
    
    print(f"✅ Loaded {len(df)} districts")
    print(f"📋 Columns: {list(df.columns)}")
    
    # Calculate total population per district
    df['total_population'] = df['male'] + df['female']
    
    print(f"\n📊 Population Summary:")
    print(f"   Total Berlin Population: {df['total_population'].sum():,}")
    print(f"   Average per District: {df['total_population'].mean():,.0f}")
    print(f"   Most Populous: {df.loc[df['total_population'].idxmax(), 'district']} ({df['total_population'].max():,})")
    print(f"   Least Populous: {df.loc[df['total_population'].idxmin(), 'district']} ({df['total_population'].min():,})")
    
    # Load into database
    df.to_sql('district_population', conn, if_exists='replace', index=False)
    print(f"\n✅ Population data loaded into 'district_population' table")
    
    # Verify
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM district_population")
    count = cursor.fetchone()[0]
    print(f"✅ Verified: {count} district records in database")
    
    # Show sample
    print("\n📊 Sample District Data:")
    cursor.execute("""
        SELECT district_id, district, total_population, male, female, germans, foreigners
        FROM district_population
        LIMIT 3
    """)
    for row in cursor.fetchall():
        print(f"   {row[0]} - {row[1]}: {row[2]:,} people ({row[3]:,} M, {row[4]:,} F)")
    
    conn.close()
    
    print("\n" + "=" * 60)
    print("🎉 POPULATION DATA LOADED SUCCESSFULLY!")
    print("=" * 60)

def calculate_crime_per_capita():
    """Calculate and display crime per capita statistics"""
    print("\n" + "=" * 60)
    print("🔍 CALCULATING CRIME PER CAPITA")
    print("=" * 60)
    
    conn = sqlite3.connect(DB_PATH)
    
    # Join crime and population data
    query = """
    SELECT 
        c.district,
        c.district_id,
        SUM(c.total_number_cases) as total_crimes,
        p.total_population,
        ROUND((SUM(c.total_number_cases) * 100000.0 / p.total_population), 2) as crime_per_100k
    FROM crime_statistics c
    LEFT JOIN district_population p ON c.district_id = p.district_id
    WHERE p.total_population IS NOT NULL
    GROUP BY c.district, c.district_id, p.total_population
    ORDER BY crime_per_100k DESC
    """
    
    df = pd.read_sql_query(query, conn)
    
    print("\n📊 CRIME PER CAPITA RANKINGS (per 100,000 residents):")
    print("=" * 60)
    
    for idx, row in df.iterrows():
        rank = idx + 1
        emoji = "🔴" if rank <= 3 else "🟡" if rank <= 6 else "🟢"
        print(f"{emoji} #{rank:2d} | {row['district']:30s} | {row['crime_per_100k']:10,.0f} per 100k")
    
    print("\n" + "=" * 60)
    print("🎯 KEY INSIGHTS:")
    print(f"   Most Dangerous (per capita): {df.iloc[0]['district']}")
    print(f"   Safest (per capita): {df.iloc[-1]['district']}")
    print("=" * 60)
    
    conn.close()
    
    return df

if __name__ == "__main__":
    load_population_data()
    calculate_crime_per_capita()

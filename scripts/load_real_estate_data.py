
"""
Load Berlin Real Estate Data into Database
Enables crime-price correlation analysis
"""

import sqlite3
import pandas as pd
import numpy as np

# Paths
DB_PATH = "database/berlin_intelligence.db"
LAND_PRICES_PATH = "data/real_estate/land_prices.csv"

def load_land_prices():
    """Load land prices into database"""
    print("=" * 60)
    print("🏠 LOADING REAL ESTATE DATA")
    print("=" * 60)
    
    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    
    # Load CSV
    print(f"\n📂 Loading: {LAND_PRICES_PATH}")
    df = pd.read_csv(LAND_PRICES_PATH)
    
    print(f"✅ Loaded {len(df):,} land price records")
    print(f"📋 Columns: {list(df.columns)}")
    print(f"📅 Date range: {df['reference_date'].min()} to {df['reference_date'].max()}")
    
    # Show land use types
    print(f"\n🏘️ Land Use Types:")
    print(df['typical_land_use_type'].value_counts().head(10))
    
    # Load into database
    df.to_sql('land_prices', conn, if_exists='replace', index=False)
    print(f"\n✅ Land prices loaded into 'land_prices' table")
    
    conn.close()

def calculate_district_averages():
    """Calculate average land prices by district"""
    print("\n" + "=" * 60)
    print("💰 CALCULATING AVERAGE LAND PRICES BY DISTRICT")
    print("=" * 60)
    
    conn = sqlite3.connect(DB_PATH)
    
    # Filter for residential properties (W - Wohngebiet)
    query = """
    SELECT 
        district_name,
        COUNT(*) as num_zones,
        AVG(standard_land_value) as avg_price,
        MIN(standard_land_value) as min_price,
        MAX(standard_land_value) as max_price
    FROM land_prices
    WHERE typical_land_use_type LIKE 'W%'
    GROUP BY district_name
    ORDER BY avg_price DESC
    """
    
    df = pd.read_sql_query(query, conn)
    
    print("\n📊 AVERAGE RESIDENTIAL LAND PRICES BY DISTRICT (€/sqm):")
    print("=" * 70)
    print(f"{'District':<30} {'Avg Price':>12} {'Min':>10} {'Max':>10} {'Zones':>8}")
    print("=" * 70)
    
    for _, row in df.iterrows():
        print(f"{row['district_name']:<30} €{row['avg_price']:>10,.0f} €{row['min_price']:>8,.0f} €{row['max_price']:>8,.0f} {row['num_zones']:>7}")
    
    conn.close()
    return df

def crime_price_correlation():
    """Analyze correlation between crime rates and property prices - FIXED VERSION"""
    print("\n" + "=" * 60)
    print("🔍 CRIME vs PROPERTY PRICE CORRELATION (FIXED)")
    print("=" * 60)
    
    conn = sqlite3.connect(DB_PATH)
    
    # STEP 1: Calculate crime per capita (from existing query that works)
    crime_query = """
    SELECT 
        c.district,
        c.district_id,
        SUM(c.total_number_cases) as total_crimes,
        p.total_population,
        ROUND((SUM(c.total_number_cases) * 100000.0 / p.total_population), 0) as crime_per_100k
    FROM crime_statistics c
    LEFT JOIN district_population p ON c.district_id = p.district_id
    WHERE p.total_population IS NOT NULL
    GROUP BY c.district, c.district_id, p.total_population
    """
    
    crime_df = pd.read_sql_query(crime_query, conn)
    
    # STEP 2: Calculate average land prices (residential only)
    price_query = """
    SELECT 
        district_name,
        AVG(standard_land_value) as avg_land_price
    FROM land_prices
    WHERE typical_land_use_type LIKE 'W%'
    GROUP BY district_name
    """
    
    price_df = pd.read_sql_query(price_query, conn)
    
    # STEP 3: Merge the two datasets (NO CARTESIAN PRODUCT!)
    merged = crime_df.merge(price_df, left_on='district', right_on='district_name', how='inner')
    merged = merged.sort_values('crime_per_100k', ascending=False)
    
    print("\n📊 CRIME RATE vs LAND PRICE COMPARISON:")
    print("=" * 80)
    print(f"{'District':<30} {'Crime per 100k':>15} {'Avg Land Price':>18} {'Safety':>10}")
    print("=" * 80)
    
    for _, row in merged.iterrows():
        safety = "🟢 Safe" if row['crime_per_100k'] < 400000 else "🟡 Medium" if row['crime_per_100k'] < 600000 else "🔴 Risk"
        print(f"{row['district']:<30} {row['crime_per_100k']:>15,.0f} €{row['avg_land_price']:>15,.0f}/sqm {safety:>12}")
    
    # Calculate correlation coefficient
    correlation = merged['crime_per_100k'].corr(merged['avg_land_price'])
    
    print("\n" + "=" * 80)
    print(f"📈 CORRELATION COEFFICIENT: {correlation:.3f}")
    
    if correlation < -0.3:
        print("✅ STRONG NEGATIVE CORRELATION: Higher crime → Lower property prices")
        print("   Safety commands premium prices in Berlin real estate!")
    elif correlation > 0.3:
        print("⚠️ POSITIVE CORRELATION: Higher crime → Higher property prices")
        print("   This suggests urban center effect - despite crime, central location valued")
    else:
        print("➡️ WEAK CORRELATION: Crime and prices not strongly related")
        print("   Other factors (location, amenities) may dominate pricing")
    
    print("=" * 80)
    
    # Show specific examples
    safest = merged.iloc[-1]
    most_dangerous = merged.iloc[0]
    
    print(f"\n💡 KEY INSIGHTS:")
    print(f"   Safest: {safest['district']} - {safest['crime_per_100k']:,.0f} per 100k → €{safest['avg_land_price']:,.0f}/sqm")
    print(f"   Most Dangerous: {most_dangerous['district']} - {most_dangerous['crime_per_100k']:,.0f} per 100k → €{most_dangerous['avg_land_price']:,.0f}/sqm")
    print(f"   Price Ratio: {safest['avg_land_price'] / most_dangerous['avg_land_price']:.1f}x more expensive in safest district")
    
    conn.close()
    return merged

if __name__ == "__main__":
    load_land_prices()
    calculate_district_averages()
    crime_price_correlation()

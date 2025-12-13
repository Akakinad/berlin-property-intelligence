
"""
SQLite Database Setup Script
Creates Berlin Property Intelligence database and loads crime statistics
"""

import sqlite3
import pandas as pd
import os
from pathlib import Path

# Database configuration
DB_PATH = "database/berlin_intelligence.db"
CRIME_DATA_PATH = "data/crime_statistics/berlin_crime_statistics_final.csv"

def create_database():
    """Create SQLite database and crime_statistics table"""
    print("🔧 Creating SQLite database...")
    
    # Ensure database directory exists
    os.makedirs("database", exist_ok=True)
    
    # Connect to database (creates if doesn't exist)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create crime_statistics table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS crime_statistics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            area_id REAL,
            neighborhood TEXT,
            district TEXT,
            district_id TEXT,
            year INTEGER,
            crime_type_german TEXT,
            crime_type_english TEXT,
            category TEXT,
            total_number_cases REAL,
            frequency_100k REAL,
            population_base REAL,
            severity_weight REAL
        )
    """)
    
    conn.commit()
    print(f"✅ Database created: {DB_PATH}")
    print(f"✅ Table created: crime_statistics")
    
    return conn

def load_crime_data(conn):
    """Load crime statistics from CSV into database"""
    print(f"\n📊 Loading crime statistics from: {CRIME_DATA_PATH}")
    
    # Check if file exists
    if not os.path.exists(CRIME_DATA_PATH):
        print(f"❌ Error: File not found: {CRIME_DATA_PATH}")
        return False
    
    # Read CSV with proper dtype for district_id
    df = pd.read_csv(CRIME_DATA_PATH, dtype={'district_id': str})
    
    print(f"📈 CSV loaded: {len(df):,} records")
    print(f"📋 Columns: {list(df.columns)}")
    
    # Load into database
    df.to_sql('crime_statistics', conn, if_exists='replace', index=False)
    
    print(f"✅ Data loaded successfully!")
    
    return True

def verify_database(conn):
    """Verify data was loaded correctly"""
    print("\n🔍 Verifying database...")
    
    cursor = conn.cursor()
    
    # Count records
    cursor.execute("SELECT COUNT(*) FROM crime_statistics")
    count = cursor.fetchone()[0]
    print(f"✅ Total records: {count:,}")
    
    # Count districts
    cursor.execute("SELECT COUNT(DISTINCT district) FROM crime_statistics")
    districts = cursor.fetchone()[0]
    print(f"✅ Unique districts: {districts}")
    
    # Count neighborhoods
    cursor.execute("SELECT COUNT(DISTINCT neighborhood) FROM crime_statistics")
    neighborhoods = cursor.fetchone()[0]
    print(f"✅ Unique neighborhoods: {neighborhoods}")
    
    # Count district_ids
    cursor.execute("SELECT COUNT(DISTINCT district_id) FROM crime_statistics")
    district_ids = cursor.fetchone()[0]
    print(f"✅ Unique district IDs: {district_ids}")
    
    # Year range
    cursor.execute("SELECT MIN(year), MAX(year) FROM crime_statistics")
    min_year, max_year = cursor.fetchone()
    print(f"✅ Year range: {min_year} - {max_year}")
    
    # Sample data
    print("\n📊 Sample data (first 3 records):")
    cursor.execute("SELECT area_id, neighborhood, district, district_id, year, crime_type_english, total_number_cases FROM crime_statistics LIMIT 3")
    for row in cursor.fetchall():
        print(f"  Area: {row[0]} | {row[1]} | {row[2]} | ID:{row[3]} | {row[4]} | {row[5]} | Cases: {row[6]}")
    
    return True

def main():
    """Main execution function"""
    print("=" * 60)
    print("🏙️  BERLIN PROPERTY INTELLIGENCE - DATABASE SETUP")
    print("=" * 60)
    
    # Create database
    conn = create_database()
    
    # Load crime statistics
    success = load_crime_data(conn)
    
    if success:
        # Verify data
        verify_database(conn)
        
        print("\n" + "=" * 60)
        print("🎉 DATABASE SETUP COMPLETE!")
        print("=" * 60)
        print(f"\n📂 Database location: {DB_PATH}")
        print("🚀 Ready for data analysis!")
    else:
        print("\n❌ Database setup failed!")
    
    # Close connection
    conn.close()

if __name__ == "__main__":
    main()

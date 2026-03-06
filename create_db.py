import pandas as pd
import sqlite3
import glob
import os

def create_sqlite_db(csv_folder_path, db_name='process.db'):
    """
    Convert multiple CSV files from a folder into a SQLite database.
    
    Args:
        csv_folder_path (str): Path to folder containing CSV files
        db_name (str): Name of the output SQLite database
    """
    # Create SQLite connection
    conn = sqlite3.connect(db_name)
    
    try:
        # Get list of all CSV files in the folder
        csv_files = glob.glob(os.path.join(csv_folder_path, '*.csv'))
        
        # Read and process each CSV file
        for csv_file in csv_files:
            print(f"Processing {csv_file}...")
            
            # Read CSV file
            df = pd.read_csv(csv_file)
            
            # Clean column names (remove spaces, standardize)
            df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]
            
            # Append data to SQLite
            # If table doesn't exist, it will be created
            df.to_sql('panoramas', conn, if_exists='append', index=False)
            
        # Create indices for faster querying
        cursor = conn.cursor()
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_id ON panoramas(id);')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_lat_lng ON panoramas(lat, lng);')
        cursor.execute('ALTER TABLE panoramas ADD approved BOOL DEFAULT NULL')
        
        print(f"\nDatabase created successfully: {db_name}")
        
        # Print some basic statistics
        cursor.execute('SELECT COUNT(*) FROM panoramas;')
        total_rows = cursor.fetchone()[0]
        print(f"Total records: {total_rows}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        
    finally:
        conn.close()

if __name__ == "__main__":
    # Usage
    csv_folder_path = "./digits"  # Replace with your folder path
    create_sqlite_db(csv_folder_path)
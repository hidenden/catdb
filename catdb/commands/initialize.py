import pandas as pd
from catdb.db.database import CatWeightDB

def initialize_database(db_file: str, csv_file: str | None = None) -> None:
    """
    Initializes the database by creating the necessary tables if they do not already exist.
    Optionally, loads initial data from a specified CSV file.

    Parameters:
    - db_file (str): Path to the SQLite3 database file.
    - csv_file (str | None): Path to a CSV file to load initial data. CSV should have 'date', 'weight', and 'notes' columns.

    Returns:
    - None
    """
    db = CatWeightDB(db_file)
    
    # If a CSV file is provided, attempt to load it and insert data
    if csv_file:
        try:
            # Load CSV data into a DataFrame
            df = pd.read_csv(csv_file)
            
            # Ensure 'date' column is in datetime format, then convert to date objects
            df['date'] = pd.to_datetime(df['date']).dt.date

            # Establish database connection and create table if not already existing
            db.connect()
            table_created = db.initialize_table()

            # Insert records into the database using upsert
            db.upsert_weight_records(df)
            print(f"Database initialized. Table 'cat_weight_records' created in {db_file} and data loaded from {csv_file}.")

        except Exception as e:
            print(f"Error loading CSV file: {e}. Initialization aborted.")
            return  # Exit without creating a table if CSV loading fails

    else:
        # Only create the table if no CSV file is provided
        db.connect()
        table_created = db.initialize_table()
        if table_created:
            print(f"Database initialized. Table 'cat_weight_records' created in {db_file}.")
        else:
            print("Table 'cat_weight_records' already exists.")

    db.close()

from catdb.db.database import CatWeightDB

def initialize_database(db_file: str = "cat_data.db") -> None:
    """
    Initializes the database by creating the necessary tables if they do not already exist,
    and prints the result to STDOUT.

    Parameters:
    - db_file (str): Path to the SQLite3 database file.

    Returns:
    - None
    """
    db = CatWeightDB(db_file)
    db.connect()

    # Initialize table and check if it was created
    table_created = db.initialize_table()
    db.close()
    
    if table_created:
        print(f"Database initialized. Table 'cat_weight_records' created in {db_file}.")
    else:
        print("Table 'cat_weight_records' already exists.")    
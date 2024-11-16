from typing import Optional, Tuple
from catdb.db.database import DatabaseConnection

def initialize_database(db_file: str = "cat_data.db") -> Tuple[bool, str]:
    """
    Initializes the database by creating the necessary tables if they do not already exist.

    Parameters:
    - db_file (str): Path to the SQLite3 database file.

    Returns:
    - Tuple[bool, str]: A tuple where the first element is True if the table was created, 
      and False if it already existed. The second element is a message indicating the result.
    """
    db = DatabaseConnection(db_file)
    db.connect()

    # initialize_table() の戻り値で初期化結果を判定
    table_created = db.initialize_table()
    db.close()
    
    if table_created:
        return True, f"Database initialized. Table 'cat_weight_records' created in {db_file}."
    else:
        return False, "Table 'cat_weight_records' already exists."
    
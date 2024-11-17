from typing import Optional
from datetime import date as DateType
from catdb.db.database import CatWeightDB

def add_weight_record(db_file: str, date: DateType, weight: float, notes: Optional[str] = None) -> None:
    """
    Adds a new weight record to the database and prints the result to STDOUT.

    Parameters:
    - db_file (str): Path to the SQLite3 database file.
    - date (DateType): Date of the record as a datetime.date object.
    - weight (float): Weight of the cat in kg.
    - notes (Optional[str]): Optional notes for the record.

    Returns:
    - None
    """
    db = CatWeightDB(db_file)
    db.connect()
    
    # DatabaseConnection の関数も date を datetime.date 型で受け取る
    success = db.add_weight_record(date, weight, notes)
    db.close()
    
    if success:
        print(f"Record added: {date}, {weight} kg, Notes: {notes}")
    else:
        print(f"Failed to add record for date {date}. Record may already exist.")

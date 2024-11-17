from datetime import date
from typing import Optional
from catdb.db.database import CatWeightDB

def update_weight_record(db_file: str, date: date, weight: float, notes: Optional[str] = None) -> None:
    """
    Updates an existing weight record in the database and prints the result to STDOUT.

    Parameters:
    - db_file (str): Path to the SQLite3 database file.
    - date (date): Date of the record as a datetime.date object.
    - weight (float): New weight of the cat in kg.
    - notes (Optional[str]): New notes for the record.

    Returns:
    - None
    """
    db = CatWeightDB(db_file)
    db.connect()
    success = db.update_weight_record(date, weight, notes)
    db.close()

    if success:
        print(f"Record updated: {date}, {weight} kg, Notes: {notes}")
    else:
        print(f"No record found for date {date}. Update failed.")

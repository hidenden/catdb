from datetime import date
from typing import Optional
from catdb.db.database import DatabaseConnection

def update_weight_record(db_file: str, date: date, weight: float, notes: Optional[str] = None) -> tuple[bool, str]:
    """
    Updates an existing weight record in the database.

    Parameters:
    - db_file (str): Path to the SQLite3 database file.
    - date (date): Date of the record as a datetime.date object.
    - weight (float): New weight of the cat in kg.
    - notes (Optional[str]): New notes for the record.

    Returns:
    - tuple[bool, str]: A tuple where the first element is True if the update was successful,
      and the second element is a message indicating the result.
    """
    db = DatabaseConnection(db_file)
    db.connect()
    success = db.update_weight_record(date, weight, notes)
    db.close()

    if success:
        return True, f"Record updated: {date}, {weight} kg, Notes: {notes}"
    else:
        return False, f"No record found for date {date}. Update failed."
    
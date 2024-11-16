from typing import Optional, Tuple
from datetime import date as DateType
from catdb.db.database import DatabaseConnection

def add_weight_record(db_file: str, date: DateType, weight: float, notes: Optional[str] = None) -> Tuple[bool, str]:
    """
    Adds a new weight record to the database.

    Parameters:
    - db_file (str): Path to the SQLite3 database file.
    - date (DateType): Date of the record as a datetime.date object.
    - weight (float): Weight of the cat in kg.
    - notes (Optional[str]): Optional notes for the record.

    Returns:
    - Tuple[bool, str]: A tuple where the first element is True if the operation was successful,
      and the second element is a message indicating the result.
    """
    db = DatabaseConnection(db_file)
    db.connect()
    # DatabaseConnection の関数も date を datetime.date 型で受け取る
    success = db.add_weight_record(date, weight, notes)
    db.close()
    
    if success:
        return True, f"Record added: {date}, {weight} kg, Notes: {notes}"
    else:
        return False, f"Failed to add record for date {date}. Record may already exist."
       

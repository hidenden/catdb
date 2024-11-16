from catdb.db.database import DatabaseConnection
from typing import Tuple
from datetime import date as DateType

def delete_weight_record(db_file: str, date: DateType) -> Tuple[bool, str]:
    """
    Deletes a weight record from the database by date.

    Parameters:
    - db_file (str): Path to the SQLite3 database file.
    - date (DateType): Date of the record as a datetime.date object.

    Returns:
    - Tuple[bool, str]: A tuple where the first element is True if the deletion was successful,
      and the second element is a message indicating the result.
    """
    db = DatabaseConnection(db_file)
    db.connect()
    success = db.delete_weight_record(date)
    db.close()

    if success:
        return True, f"Record deleted for date: {date}"
    else:
        return False, f"No record found for date {date}. Deletion failed."
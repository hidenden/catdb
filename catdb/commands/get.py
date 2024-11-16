from datetime import date
from typing import List
from catdb.db.database import DatabaseConnection

def get_weight_records(db_file: str, date: date | None = None) -> tuple[bool, str | List[tuple[date, float, str | None]]]:
    """
    Retrieves a weight record or records from the database. If a date is specified, 
    it retrieves the record for that date. If no date is provided, it retrieves all records.

    Parameters:
    - db_file (str): Path to the SQLite3 database file.
    - date (date | None): Specific date of the record as a datetime.date object. 
                          If None, retrieves all records.

    Returns:
    - tuple[bool, str | List[tuple[date, float, str | None]]]: A tuple where the first element 
      is True if records are found, False otherwise. The second element is a list of records 
      (date, weight, notes) if records are found, or a string message if no records are found.
    """
    db = DatabaseConnection(db_file)
    db.connect()
    
    if date:
        # Retrieve a specific record
        record = db.get_weight_record(date)
        db.close()
        if record:
            return True, [record]  # Return a list with a single record tuple
        else:
            return False, f"No record found for date {date}."
    else:
        # Retrieve all records
        records = db.get_all_records()
        db.close()
        if records:
            return True, records  # Return a list of records
        else:
            return False, "No records found."

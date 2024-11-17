from datetime import date
from catdb.db.database import CatWeightDB
import pandas as pd

def print_weight_records(db_file: str, begin_date: date | None = None, end_date: date | None = None) -> None:
    """
    Retrieves and prints weight record(s) from the database based on specified date criteria.
    - If both dates are None, retrieves all records.
    - If begin_date is specified and end_date is None, retrieves a specific record.
    - If both dates are specified, retrieves records within the date range.

    Parameters:
    - db_file (str): Path to the SQLite3 database file.
    - begin_date (date | None): The start date of the range or specific date of the record.
    - end_date (date | None): The end date of the range.

    Returns:
    - None
    """
    db = CatWeightDB(db_file)
    db.connect()
    
    if begin_date is None and end_date is None:
        # Retrieve all records
        records = db.get_all_records()
        if not records.empty:
            print(records)
        else:
            print("No records found.")
    
    elif begin_date is not None and end_date is None:
        # Retrieve a specific record
        record = db.get_weight_record(begin_date)
        if not record.empty:
            print(record)
        else:
            print(f"No record found for date {begin_date}.")
    
    elif begin_date is not None and end_date is not None:
        # Retrieve records within the date range
        records = db.get_records_by_date_range(begin_date, end_date)
        if not records.empty:
            print(records)
        else:
            print(f"No records found between {begin_date} and {end_date}.")
    
    db.close()

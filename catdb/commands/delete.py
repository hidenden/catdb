from catdb.db.database import CatWeightDB
from datetime import date as DateType

def delete_weight_record(db_file: str, date: DateType) -> None:
    """
    Deletes a weight record from the database by date and prints the result to STDOUT.

    Parameters:
    - db_file (str): Path to the SQLite3 database file.
    - date (DateType): Date of the record as a datetime.date object.

    Returns:
    - None
    """
    db = CatWeightDB(db_file)
    db.connect()
    success = db.delete_weight_record(date)
    db.close()

    if success:
        print(f"Record deleted for date: {date}")
    else:
        print(f"No record found for date {date}. Deletion failed.")

import os
from datetime import datetime, date
from typing import Optional

def parse_date(date_str: str) -> date:
    """
    Parses a date string into a datetime.date object. Supports multiple date formats.

    Parameters:
    - date_str (str): Date string to parse.

    Returns:
    - date: Parsed date as a datetime.date object.

    Raises:
    - ValueError: If the date format is not supported.
    """
    for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%m-%d-%Y", "%m/%d/%Y"):
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    raise ValueError(f"Invalid date format: {date_str}")

def get_database_file(args_db_file: Optional[str]) -> str:
    """
    Determines the database file path based on the --db-file argument or CAT_DB environment variable.

    Parameters:
    - args_db_file (Optional[str]): The --db-file argument value.

    Returns:
    - str: The path to the database file.

    Raises:
    - SystemExit: If neither --db-file is provided nor CAT_DB environment variable is set.
    """
    if args_db_file:
        return args_db_file
    elif "CAT_DB" in os.environ:
        return os.environ["CAT_DB"]
    else:
        print("Error: Please provide a database file with --db-file or set the CAT_DB environment variable.")
        exit(1)
    
#!/usr/bin/env python3

import argparse
import os
from datetime import datetime, date
from typing import Optional
from catdb.commands.add import add_weight_record
from catdb.commands.update import update_weight_record
from catdb.commands.delete import delete_weight_record
from catdb.commands.get import get_weight_records
from catdb.commands.initialize import initialize_database

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

def catdb_main() -> None:
    parser = argparse.ArgumentParser(description="Cat Weight Database CLI")
    parser.add_argument("--db-file", type=str, help="Path to the database file. Overrides CAT_DB environment variable.")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Init command
    init_parser = subparsers.add_parser("init", help="Initialize the database")
    
    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new weight record")
    add_parser.add_argument("date", type=str, help="Date of the record in 'YYYY-MM-DD' format")
    add_parser.add_argument("weight", type=float, help="Weight of the cat in kg")
    add_parser.add_argument("--notes", type=str, help="Optional notes for the record", default=None)

    # Update command
    update_parser = subparsers.add_parser("update", help="Update an existing weight record")
    update_parser.add_argument("date", type=str, help="Date of the record in 'YYYY-MM-DD' format")
    update_parser.add_argument("weight", type=float, help="New weight of the cat in kg")
    update_parser.add_argument("--notes", type=str, help="New notes for the record", default=None)

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a weight record")
    delete_parser.add_argument("date", type=str, help="Date of the record to delete in 'YYYY-MM-DD' format")

    # Display command
    display_parser = subparsers.add_parser("display", help="Display weight records")
    display_parser.add_argument("--date", type=str, help="Specific date of the record in 'YYYY-MM-DD' format")

    args = parser.parse_args()
    db_file = get_database_file(args.db_file)

    # Process commands
    if args.command == "init":
        success, message = initialize_database(db_file)
        print("Success:" if success else "Info:", message)
    elif args.command == "add":
        try:
            record_date = parse_date(args.date)
            success, message = add_weight_record(db_file, record_date, args.weight, args.notes)
            print("Success:" if success else "Error:", message)
        except ValueError as e:
            print(f"Error: {e}")
    elif args.command == "update":
        try:
            record_date = parse_date(args.date)
            success, message = update_weight_record(db_file, record_date, args.weight, args.notes)
            print("Success:" if success else "Error:", message)
        except ValueError as e:
            print(f"Error: {e}")
    elif args.command == "delete":
        try:
            record_date = parse_date(args.date)
            success, message = delete_weight_record(db_file, record_date)
            print("Success:" if success else "Error:", message)
        except ValueError as e:
            print(f"Error: {e}")
    elif args.command == "display":
        try:
            record_date = parse_date(args.date) if args.date else None
            success, result = get_weight_records(db_file, date=record_date)
            if success:
                for record in result:
                    print(f"Date: {record[0]}, Weight: {record[1]} kg, Notes: {record[2]}")
            else:
                print("Info:", result)
        except ValueError as e:
            print(f"Error: {e}")
    else:
        parser.print_help()

if __name__ == "__main__":
    catdb_main()

#!/usr/bin/env python3

import argparse
from datetime import date
from typing import Optional
import pandas as pd
from catdb.commands.add import add_weight_record
from catdb.commands.update import update_weight_record
from catdb.commands.delete import delete_weight_record
from catdb.commands.get import print_weight_records
from catdb.commands.graph import graph_weight_records
from catdb.commands.initialize import initialize_database
from catdb.utils.utils import parse_date, get_database_file

def catdb_main() -> None:
    parser = argparse.ArgumentParser(description="Cat Weight Database CLI")
    parser.add_argument("--db-file", type=str, help="Path to the database file. Overrides CAT_DB environment variable.")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Init command
    init_parser = subparsers.add_parser("init", help="Initialize the database")
    init_parser.add_argument("--csv", type=str, help="Path to a CSV file to load initial data")

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

    # List command
    list_parser = subparsers.add_parser("list", help="List weight records")
    list_parser.add_argument("--begin-date", type=str, help="Start date of the range in 'YYYY-MM-DD' format")
    list_parser.add_argument("--end-date", type=str, help="End date of the range in 'YYYY-MM-DD' format")

    # Graph command
    graph_parser = subparsers.add_parser("graph", help="Graph weight records")
    graph_parser.add_argument("--graph-file", type=str, help="Output graph file name", default=None)
    
    args = parser.parse_args()
    db_file = get_database_file(args.db_file)

    try:
        # Process commands
        if args.command == "init":
            initialize_database(db_file, csv_file=args.csv)
        elif args.command == "add":
            record_date = parse_date(args.date)
            add_weight_record(db_file, record_date, args.weight, args.notes)
        elif args.command == "update":
            record_date = parse_date(args.date)
            update_weight_record(db_file, record_date, args.weight, args.notes)
        elif args.command == "delete":
            record_date = parse_date(args.date)
            delete_weight_record(db_file, record_date)
        elif args.command == "list":
            begin_date = parse_date(args.begin_date) if args.begin_date else None
            end_date = parse_date(args.end_date) if args.end_date else None
            print_weight_records(db_file, begin_date=begin_date, end_date=end_date)
        elif args.command == "graph":
            graph_weight_records(db_file, args.graph_file)
        else:
            parser.print_help()
            if db_file:
                print(f"\nCurrent database:{db_file}\n")

    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    catdb_main()

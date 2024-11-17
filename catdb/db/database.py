import sqlite3
from sqlite3 import Connection
from typing import List
from datetime import date
import pandas as pd

class CatWeightDB:
    """
    DatabaseConnection class for managing SQLite3 database interactions
    related to cat weight records.
    """

    def __init__(self, db_file: str = "cat_data.db") -> None:
        """
        Initializes a connection to the SQLite3 database.

        Parameters:
        - db_file (str): Path to the SQLite3 database file.
        """
        self.db_file: str = db_file
        self.conn: Connection | None = None

    def connect(self) -> None:
        """Establishes a connection to the SQLite3 database."""
        self.conn = sqlite3.connect(self.db_file)
        self.conn.execute("PRAGMA foreign_keys = 1")

    def close(self) -> None:
        """Closes the database connection if it is open."""
        if self.conn:
            self.conn.close()
            self.conn = None

    def initialize_table(self) -> bool:
        """
        Initializes the cat_weight_records table if it does not exist.

        Returns:
        - bool: True if the table was created, False if it already existed.
        """
        if self.conn != None:
            cursor = self.conn.cursor()
        else:
            return False
        
        # テーブルの存在確認
        cursor.execute("""
            SELECT name FROM sqlite_master WHERE type='table' AND name='cat_weight_records';
        """)
        table_exists: bool = cursor.fetchone() is not None

        # テーブルが存在しない場合にのみ作成
        if not table_exists:
            with self.conn:
                self.conn.execute("""
                    CREATE TABLE IF NOT EXISTS cat_weight_records (
                        date TEXT PRIMARY KEY,
                        weight REAL NOT NULL,
                        notes TEXT
                    )
                """)
            return True  # テーブルを新規作成した場合に True を返す
        return False  # すでにテーブルが存在する場合に False を返す

    def add_weight_record(self, date: date, weight: float, notes: str | None = None) -> bool:
        """
        Adds a new weight record to the database.

        Parameters:
        - date (date): Date of the record as a datetime.date object.
        - weight (float): Weight of the cat in kg.
        - notes (str | None): Optional notes for the record.

        Returns:
        - bool: True if insertion was successful, False otherwise.
        """
        if self.conn == None:
            return False
        
        try:
            with self.conn:
                self.conn.execute(
                    "INSERT INTO cat_weight_records (date, weight, notes) VALUES (?, ?, ?)",
                    (date.isoformat(), weight, notes)
                )
            return True
        except sqlite3.IntegrityError:
            return False  # Date already exists as primary key

    def get_weight_record(self, date: date) -> pd.DataFrame:
        """
        Retrieves a weight record by date and returns it as a pandas DataFrame.

        Parameters:
        - date (date): Date of the record as a datetime.date object.

        Returns:
        - pd.DataFrame: DataFrame with columns 'date', 'weight', 'notes' where 'date' is pandas.Timestamp.
        """
        query = "SELECT date, weight, notes FROM cat_weight_records WHERE date = ?"
        df = pd.read_sql_query(query, self.conn, params=[date.isoformat()])
        df['date'] = pd.to_datetime(df['date'])  # Convert date column to pandas.Timestamp
        return df

    def get_all_records(self) -> pd.DataFrame:
        """
        Retrieves all weight records from the database and returns them as a pandas DataFrame.

        Returns:
        - pd.DataFrame: DataFrame containing all records with columns 'date', 'weight', 'notes' where 'date' is pandas.Timestamp.
        """
        query = "SELECT date, weight, notes FROM cat_weight_records ORDER BY date"
        df = pd.read_sql_query(query, self.conn)
        df['date'] = pd.to_datetime(df['date'])  # Convert date column to pandas.Timestamp
        return df

    def get_records_by_date_range(self, begin_date: date, end_date: date) -> pd.DataFrame:
        """
        Retrieves records within a specific date range, inclusive of begin_date and end_date.

        Parameters:
        - begin_date (date): The start date of the range as a datetime.date object.
        - end_date (date): The end date of the range as a datetime.date object.

        Returns:
        - pd.DataFrame: DataFrame containing records within the date range with columns 'date', 'weight', 'notes' where 'date' is pandas.Timestamp.
        """
        query = """
            SELECT date, weight, notes 
            FROM cat_weight_records 
            WHERE date BETWEEN ? AND ? 
            ORDER BY date
        """
        df = pd.read_sql_query(query, self.conn, params=[begin_date.isoformat(), end_date.isoformat()])
        df['date'] = pd.to_datetime(df['date'])  # Convert date column to pandas.Timestamp
        return df

    def update_weight_record(self, date: date, weight: float, notes: str | None = None) -> bool:
        """
        Updates an existing weight record.

        Parameters:
        - date (date): Date of the record as a datetime.date object.
        - weight (float): New weight of the cat.
        - notes (str | None): New notes for the record.

        Returns:
        - bool: True if update was successful, False if record does not exist.
        """
        if self.conn == None:
            return False
        
        with self.conn:
            cursor = self.conn.execute(
                "UPDATE cat_weight_records SET weight = ?, notes = ? WHERE date = ?",
                (weight, notes, date.isoformat())
            )
            return cursor.rowcount > 0

    def upsert_weight_records(self, records: pd.DataFrame) -> bool:
        """
        Inserts or updates multiple weight records in the database.

        Parameters:
        - records (pd.DataFrame): DataFrame with columns 'date', 'weight', 'notes' where 'date' is pandas.Timestamp.

        Notes:
        - Uses SQLite3 UPSERT feature (INSERT OR REPLACE) to perform the operation.
        """
        if self.conn == None:
            return False

        with self.conn:
            for _, record in records.iterrows():
                self.conn.execute("""
                    INSERT INTO cat_weight_records (date, weight, notes)
                    VALUES (?, ?, ?)
                    ON CONFLICT(date) DO UPDATE SET
                        weight = excluded.weight,
                        notes = excluded.notes
                """, (record['date'].isoformat(), record['weight'], record['notes']))
        return True


    def delete_weight_record(self, date: date) -> bool:
        """
        Deletes a weight record by date.

        Parameters:
        - date (date): Date of the record to delete as a datetime.date object.

        Returns:
        - bool: True if deletion was successful, False if record does not exist.
        """
        if self.conn == None:
            return False
        with self.conn:
            cursor = self.conn.execute("DELETE FROM cat_weight_records WHERE date = ?", (date.isoformat(),))
            return cursor.rowcount > 0
        

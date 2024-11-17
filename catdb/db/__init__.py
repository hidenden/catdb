"""
catdb.db - Database module for managing cat weight data storage

This package handles the database connections and schema for storing and managing
cat weight records using SQLite3.

Modules:
    - database.py: Contains the DatabaseConnection class for managing SQLite3 interactions
"""

# データベース接続クラスのインポート
from .database import CatWeightDB

__all__ = [
    "CatWeightDB"
]

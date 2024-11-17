"""
catdb - A CLI application for managing and analyzing cat weight data.

This package provides functionalities to add, view, update, and delete weight records of cats,
and can be used both interactively and through command-line commands.

Modules:
    - main: CLI entry point
    - commands: Command modules for add, display, update, delete functions
    - db: Database connection and schema management
    - utils: Helper functions
"""

# インポート
from .db.database import CatWeightDB

__all__ = [
    "CatWeightDB",
]

# パッケージのバージョン情報 (必要に応じて変更)
__version__ = "0.1.0"

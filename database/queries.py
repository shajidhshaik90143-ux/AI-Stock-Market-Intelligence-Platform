from dataclasses import dataclass
from datetime import datetime
from database.db import get_connection


@dataclass
class WatchlistItem:
    ticker: str
    created_at: datetime | None = None


@dataclass
class SearchRecord:
    ticker: str
    searched_at: datetime | None = None


def add_to_watchlist(ticker: str) -> bool:
    """Add a stock ticker to the watchlist database table."""
    ticker = ticker.strip().upper()
    if not ticker:
        return False

    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT OR IGNORE INTO watchlist (ticker) VALUES (?)",
            (ticker,)
        )
        connection.commit()
        return True
    except Exception:
        return False
    finally:
        connection.close()


def remove_from_watchlist(ticker: str) -> bool:
    """Remove a stock ticker from the watchlist database table."""
    ticker = ticker.strip().upper()
    if not ticker:
        return False

    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            "DELETE FROM watchlist WHERE ticker = ?",
            (ticker,)
        )
        connection.commit()
        return True
    except Exception:
        return False
    finally:
        connection.close()


def get_watchlist() -> list:
    """Fetch all ticker symbols in the watchlist."""
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT ticker FROM watchlist ORDER BY id ASC"
        )
        rows = cursor.fetchall()
        return [row[0] for row in rows]
    except Exception:
        return []
    finally:
        connection.close()


def add_search(ticker: str):
    """Record a user search query in the searches table."""
    ticker = ticker.strip().upper()
    if not ticker:
        return

    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO searches (ticker) VALUES (?)",
            (ticker,)
        )
        connection.commit()
    except Exception:
        pass
    finally:
        connection.close()


def get_recent_searches(limit: int = 10) -> list:
    """Fetch recent searches from the database."""
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT ticker FROM searches ORDER BY id DESC LIMIT ?",
            (limit,)
        )
        rows = cursor.fetchall()
        return [row[0] for row in rows]
    except Exception:
        return []
    finally:
        connection.close()
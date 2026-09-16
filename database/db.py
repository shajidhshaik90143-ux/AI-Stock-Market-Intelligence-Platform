import sqlite3
import os


DB_PATH = "data/market_intelligence.db"


def get_connection():

    os.makedirs("data", exist_ok=True)

    return sqlite3.connect(
        DB_PATH,
        check_same_thread=False
    )


def init_database():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS watchlist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS searches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT NOT NULL,
            searched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    connection.commit()

    cursor.execute("SELECT COUNT(*) FROM watchlist")
    count = cursor.fetchone()[0]
    if count == 0:
        default_tickers = ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN"]
        for ticker in default_tickers:
            cursor.execute(
                "INSERT OR IGNORE INTO watchlist (ticker) VALUES (?)",
                (ticker,)
            )
        connection.commit()

    connection.close()


def add_search(ticker):

    if not ticker:
        return

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO searches (ticker) VALUES (?)",
        (ticker.strip().upper(),)
    )

    connection.commit()

    connection.close()
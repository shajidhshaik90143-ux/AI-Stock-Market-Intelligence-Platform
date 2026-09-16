import os
import time
import pandas as pd
import numpy as np
import yfinance as yf


CACHE_DIR = "data/cache"

os.makedirs(CACHE_DIR, exist_ok=True)


def validate_ticker(ticker):
    if not ticker:
        return False

    ticker = ticker.strip().upper()

    if len(ticker) > 15:
        return False

    allowed = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.-"

    return all(char in allowed for char in ticker)


def get_history(ticker, period="1y", interval="1d"):
    ticker = ticker.strip().upper()

    if not validate_ticker(ticker):
        return pd.DataFrame()

    try:
        stock = yf.Ticker(ticker)

        data = stock.history(
            period=period,
            interval=interval,
            auto_adjust=False
        )

        if data is None or data.empty:
            return pd.DataFrame()

        data = data.reset_index()

        if "Datetime" in data.columns:
            data.rename(
                columns={"Datetime": "Date"},
                inplace=True
            )

        if "Date" in data.columns:
            data["Date"] = pd.to_datetime(
                data["Date"],
                errors="coerce"
            )

        return data

    except Exception:
        return pd.DataFrame()


def get_quote(ticker):
    ticker = ticker.strip().upper()

    try:
        stock = yf.Ticker(ticker)

        info = stock.info

        price = (
            info.get("currentPrice")
            or info.get("regularMarketPrice")
            or info.get("previousClose")
        )

        previous = (
            info.get("previousClose")
            or info.get("regularMarketPreviousClose")
        )

        change = None
        change_percent = None

        if price is not None and previous:
            change = price - previous
            change_percent = (change / previous) * 100

        return {
            "ticker": ticker,
            "name": info.get("longName", ticker),
            "price": price,
            "previous_close": previous,
            "change": change,
            "change_percent": change_percent,
            "market_cap": info.get("marketCap"),
            "currency": info.get("currency", "USD"),
            "exchange": info.get("exchange"),
            "sector": info.get("sector"),
            "industry": info.get("industry")
        }

    except Exception as e:
        return {
            "ticker": ticker,
            "name": ticker,
            "error": str(e)
        }


def get_company_info(ticker):
    try:
        stock = yf.Ticker(ticker)
        return stock.info
    except Exception:
        return {}


def get_financials(ticker):
    try:
        stock = yf.Ticker(ticker)

        return {
            "income_statement": stock.financials,
            "balance_sheet": stock.balance_sheet,
            "cash_flow": stock.cashflow
        }

    except Exception:
        return {
            "income_statement": pd.DataFrame(),
            "balance_sheet": pd.DataFrame(),
            "cash_flow": pd.DataFrame()
        }


def get_dividends(ticker):
    try:
        stock = yf.Ticker(ticker)
        return stock.dividends
    except Exception:
        return pd.Series(dtype=float)


def get_actions(ticker):
    try:
        stock = yf.Ticker(ticker)
        return stock.actions
    except Exception:
        return pd.DataFrame()


def get_multiple_history(tickers, period="6mo"):
    result = {}

    for ticker in tickers:
        data = get_history(ticker, period=period)

        if not data.empty:
            result[ticker] = data

    return result


def calculate_returns(data):
    if data.empty or "Close" not in data.columns:
        return pd.Series(dtype=float)

    return data["Close"].pct_change().dropna()


def calculate_moving_average(data, window=20):
    if data.empty or "Close" not in data.columns:
        return pd.Series(dtype=float)

    return data["Close"].rolling(window).mean()


def calculate_volatility(data, window=20):
    returns = calculate_returns(data)

    if returns.empty:
        return None

    return returns.rolling(window).std().iloc[-1]


def clear_cache():
    for file in os.listdir(CACHE_DIR):
        path = os.path.join(CACHE_DIR, file)

        try:
            if os.path.isfile(path):
                os.remove(path)
        except Exception:
            pass
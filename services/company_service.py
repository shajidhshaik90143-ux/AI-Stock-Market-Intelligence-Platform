import yfinance as yf
import pandas as pd


def get_company_profile(ticker):
    """Fetches high-level corporate profile and details from yfinance."""
    if not ticker:
        return {}

    ticker = ticker.strip().upper()
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        return {
            "name": info.get("longName") or info.get("shortName") or ticker,
            "symbol": ticker,
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
            "country": info.get("country", "N/A"),
            "website": info.get("website", "N/A"),
            "employees": info.get("fullTimeEmployees", "N/A"),
            "description": info.get(
                "longBusinessSummary",
                "No description available."
            )
        }
    except Exception:
        return {
            "name": ticker,
            "symbol": ticker,
            "sector": "N/A",
            "industry": "N/A",
            "country": "N/A",
            "website": "N/A",
            "employees": "N/A",
            "description": "No description available."
        }


def get_key_metrics(ticker):
    """Fetches key valuation, profitability, and operational metrics."""
    if not ticker:
        return {}

    ticker = ticker.strip().upper()
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        keys = {
            "Market Cap": "marketCap",
            "Enterprise Value": "enterpriseValue",
            "Revenue": "totalRevenue",
            "Profit": "netIncomeToCommon",
            "EPS": "trailingEps",
            "Forward EPS": "forwardEps",
            "PE Ratio": "trailingPE",
            "Forward PE": "forwardPE",
            "Price to Book": "priceToBook",
            "Return on Equity": "returnOnEquity",
            "Profit Margin": "profitMargins",
            "Operating Margin": "operatingMargins",
            "Dividend Yield": "dividendYield",
            "Beta": "beta"
        }

        result = {}
        for label, key in keys.items():
            result[label] = info.get(key)

        return result
    except Exception:
        return {}


def get_income_statement(ticker):
    """Fetches annual income statement."""
    if not ticker:
        return pd.DataFrame()
    ticker = ticker.strip().upper()
    try:
        stock = yf.Ticker(ticker)
        financials = stock.financials
        return financials if financials is not None and not financials.empty else pd.DataFrame()
    except Exception:
        return pd.DataFrame()


def get_balance_sheet(ticker):
    """Fetches annual balance sheet."""
    if not ticker:
        return pd.DataFrame()
    ticker = ticker.strip().upper()
    try:
        stock = yf.Ticker(ticker)
        balance_sheet = stock.balance_sheet
        return balance_sheet if balance_sheet is not None and not balance_sheet.empty else pd.DataFrame()
    except Exception:
        return pd.DataFrame()


def get_cashflow(ticker):
    """Fetches annual cash flow statement."""
    if not ticker:
        return pd.DataFrame()
    ticker = ticker.strip().upper()
    try:
        stock = yf.Ticker(ticker)
        cashflow = stock.cashflow
        return cashflow if cashflow is not None and not cashflow.empty else pd.DataFrame()
    except Exception:
        return pd.DataFrame()
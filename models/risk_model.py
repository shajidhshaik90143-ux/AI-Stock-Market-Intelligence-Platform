import numpy as np
import pandas as pd


def calculate_risk_metrics(data):
    """
    Calculates historical risk metrics including:
    - Annualized Volatility
    - Maximum Drawdown
    - Sharpe-like Ratio
    """
    if data.empty or "Close" not in data.columns:
        return {
            "volatility": None,
            "max_drawdown": None,
            "sharpe_like": None
        }

    prices = data["Close"].dropna()
    if len(prices) < 2:
        return {
            "volatility": None,
            "max_drawdown": None,
            "sharpe_like": None
        }

    daily_returns = prices.pct_change().dropna()
    if daily_returns.empty or daily_returns.std() == 0:
        return {
            "volatility": 0.0,
            "max_drawdown": 0.0,
            "sharpe_like": 0.0
        }

    # Annualized Volatility (assuming 252 trading days)
    volatility = float(daily_returns.std() * np.sqrt(252))

    # Maximum Drawdown
    cumulative_max = prices.cummax()
    drawdown = (prices - cumulative_max) / cumulative_max
    max_drawdown = float(drawdown.min())

    # Annualized return & Sharpe-like ratio
    total_return = (prices.iloc[-1] - prices.iloc[0]) / prices.iloc[0]
    num_days = max(len(prices), 1)
    annualized_return = (1 + total_return) ** (252 / num_days) - 1 if total_return > -1 else -1.0

    sharpe_like = float(annualized_return / volatility) if volatility > 0 else 0.0

    return {
        "volatility": volatility,
        "max_drawdown": max_drawdown,
        "sharpe_like": sharpe_like
    }


def risk_label(volatility):
    """
    Returns a human-readable risk category based on annualized volatility.
    """
    if volatility is None:
        return "Unknown"

    if volatility < 0.15:
        return "Low Risk"
    elif volatility < 0.25:
        return "Moderate Risk"
    elif volatility < 0.40:
        return "High Risk"
    else:
        return "Very High Risk"
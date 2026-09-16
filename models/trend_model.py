import numpy as np
import pandas as pd

from sklearn.linear_model import LinearRegression


def calculate_trend(data, window=30):

    if data.empty or "Close" not in data.columns:
        return {
            "trend": "Unknown",
            "slope": None,
            "confidence": None
        }

    prices = data["Close"].dropna().tail(window)

    if len(prices) < 5:
        return {
            "trend": "Insufficient data",
            "slope": None,
            "confidence": None
        }

    X = np.arange(len(prices)).reshape(-1, 1)

    y = prices.values

    model = LinearRegression()

    model.fit(X, y)

    slope = float(model.coef_[0])

    score = float(model.score(X, y))

    if slope > 0:
        trend = "Upward"
    elif slope < 0:
        trend = "Downward"
    else:
        trend = "Flat"

    return {
        "trend": trend,
        "slope": slope,
        "confidence": score
    }


def add_moving_averages(data):

    data = data.copy()

    if "Close" not in data.columns:
        return data

    data["MA20"] = (
        data["Close"]
        .rolling(20)
        .mean()
    )

    data["MA50"] = (
        data["Close"]
        .rolling(50)
        .mean()
    )

    data["MA200"] = (
        data["Close"]
        .rolling(200)
        .mean()
    )

    return data
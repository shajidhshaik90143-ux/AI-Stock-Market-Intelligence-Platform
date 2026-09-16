import numpy as np


def percentage_change(current, previous):

    try:

        if previous == 0:
            return None

        return (
            (current - previous)
            / previous
        ) * 100

    except Exception:
        return None


def calculate_return(data):

    if data.empty or "Close" not in data.columns:
        return None

    first = data["Close"].iloc[0]

    last = data["Close"].iloc[-1]

    if first == 0:
        return None

    return (
        (last - first)
        / first
    ) * 100


def calculate_average_volume(data):

    if data.empty or "Volume" not in data.columns:
        return None

    return data["Volume"].mean()


def calculate_high_low(data):

    if data.empty or "High" not in data.columns:
        return None, None

    return (
        data["High"].max(),
        data["Low"].min()
    )


def calculate_rsi(data, period=14):

    if data.empty or "Close" not in data.columns:
        return None

    delta = data["Close"].diff()

    gain = delta.clip(lower=0)

    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(period).mean()

    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss.replace(0, np.nan)

    rsi = 100 - (
        100 / (1 + rs)
    )

    return rsi


def calculate_drawdown(data):

    if data.empty or "Close" not in data.columns:
        return None

    prices = data["Close"]

    peak = prices.cummax()

    drawdown = (
        prices - peak
    ) / peak

    return drawdown.min()
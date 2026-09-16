import re


def validate_ticker(ticker):

    if not ticker:
        return False

    ticker = ticker.strip().upper()

    pattern = r"^[A-Z0-9.\-]{1,15}$"

    return bool(
        re.match(pattern, ticker)
    )


def validate_question(question):

    if not question:
        return False

    return len(question.strip()) >= 3


def validate_period(period):

    allowed = [
        "1d",
        "5d",
        "1mo",
        "3mo",
        "6mo",
        "1y",
        "2y",
        "5y",
        "10y",
        "max"
    ]

    return period in allowed
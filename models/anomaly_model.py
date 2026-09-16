import pandas as pd
from sklearn.ensemble import IsolationForest


def detect_price_anomalies(data):
    """
    Identifies anomalous trading days based on percentage returns and volume changes
    using an Isolation Forest model.
    """
    if data.empty or "Close" not in data.columns:
        return pd.DataFrame()

    df = data.copy()

    df["Returns"] = (
        df["Close"]
        .pct_change()
        .fillna(0)
    )

    if "Volume" in df.columns:
        df["VolumeChange"] = (
            df["Volume"]
            .pct_change()
            .replace([float("inf"), float("-inf")], 0)
            .fillna(0)
        )
    else:
        df["VolumeChange"] = 0.0

    features = df[["Returns", "VolumeChange"]].replace(
        [float("inf"), float("-inf")],
        0
    )

    if len(features) < 10:
        df["Anomaly"] = 1
        return df

    try:
        model = IsolationForest(
            contamination=0.05,
            random_state=42
        )
        df["Anomaly"] = model.fit_predict(features)
    except Exception:
        df["Anomaly"] = 1

    return df


def get_anomalies(data):
    """
    Returns only rows detected as anomalies (Anomaly == -1).
    """
    result = detect_price_anomalies(data)

    if result.empty or "Anomaly" not in result.columns:
        return pd.DataFrame()

    return result[result["Anomaly"] == -1]
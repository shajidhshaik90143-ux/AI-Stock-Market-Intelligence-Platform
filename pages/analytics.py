import streamlit as st
import plotly.graph_objects as go

from services.market_service import get_history

from models.trend_model import (
    calculate_trend,
    add_moving_averages
)

from models.anomaly_model import (
    detect_price_anomalies,
    get_anomalies
)

from models.risk_model import (
    calculate_risk_metrics,
    risk_label
)


def show():

    st.title("🧠 ML Market Analytics")

    ticker = st.text_input(
        "Stock ticker",
        "AAPL"
    ).strip().upper()

    period = st.selectbox(
        "Period",
        [
            "3mo",
            "6mo",
            "1y",
            "2y",
            "5y"
        ],
        index=2
    )

    if not ticker:
        return

    data = get_history(
        ticker,
        period=period
    )

    if data.empty:

        st.error(
            "Unable to retrieve data."
        )

        return

    trend = calculate_trend(data)

    risk = calculate_risk_metrics(data)

    anomaly_data = detect_price_anomalies(
        data
    )

    anomalies = get_anomalies(
        data
    )

    st.subheader(
        "📈 Trend Analysis"
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Observed Trend",
            trend["trend"]
        )

    with c2:
        st.metric(
            "Regression Slope",
            f"{trend['slope']:.4f}"
            if trend["slope"] is not None
            else "N/A"
        )

    with c3:
        st.metric(
            "Model R²",
            f"{trend['confidence']:.2f}"
            if trend["confidence"] is not None
            else "N/A"
        )

    st.subheader(
        "⚠️ Historical Risk"
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "Volatility",
            f"{risk['volatility'] * 100:.2f}%"
            if risk["volatility"] is not None
            else "N/A"
        )

    with c2:

        st.metric(
            "Maximum Drawdown",
            f"{risk['max_drawdown'] * 100:.2f}%"
            if risk["max_drawdown"] is not None
            else "N/A"
        )

    with c3:

        st.metric(
            "Historical Risk",
            risk_label(
                risk["volatility"]
            )
        )

    st.subheader(
        "🚨 Anomaly Detection"
    )

    st.write(
        f"Detected {len(anomalies)} "
        "potential historical anomalies."
    )

    if not anomalies.empty:

        st.dataframe(
            anomalies[
                [
                    "Date",
                    "Close",
                    "Returns",
                    "VolumeChange"
                ]
            ],
            use_container_width=True
        )

    st.subheader(
        "📊 Price + Moving Averages"
    )

    chart_data = add_moving_averages(
        data
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=chart_data["Date"],
            y=chart_data["Close"],
            name="Close",
            mode="lines"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=chart_data["Date"],
            y=chart_data["MA20"],
            name="MA20",
            mode="lines"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=chart_data["Date"],
            y=chart_data["MA50"],
            name="MA50",
            mode="lines"
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
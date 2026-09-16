import streamlit as st
import plotly.graph_objects as go

from services.market_service import (
    get_history,
    get_quote
)

from models.trend_model import (
    add_moving_averages,
    calculate_trend
)

from models.risk_model import (
    calculate_risk_metrics,
    risk_label
)

from utils.formatters import (
    format_currency,
    format_percent
)


def show():

    st.title("📊 Stock Analysis")

    ticker = st.text_input(
        "Stock ticker",
        "AAPL"
    ).strip().upper()

    period = st.selectbox(
        "Analysis period",
        [
            "1mo",
            "3mo",
            "6mo",
            "1y",
            "2y",
            "5y"
        ],
        index=3
    )

    if not ticker:
        return

    data = get_history(
        ticker,
        period=period
    )

    quote = get_quote(ticker)

    if data.empty:

        st.error(
            "Unable to retrieve stock data."
        )

        return

    data = add_moving_averages(data)

    trend = calculate_trend(data)

    risk = calculate_risk_metrics(data)

    st.subheader(
        f"{quote.get('name', ticker)} ({ticker})"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Price",
            format_currency(
                quote.get("price")
            )
        )

    with col2:
        st.metric(
            "Daily Change",
            format_percent(
                quote.get("change_percent")
            )
        )

    with col3:
        st.metric(
            "Trend",
            trend["trend"]
        )

    with col4:
        st.metric(
            "Risk Profile",
            risk_label(
                risk["volatility"]
            )
        )

    st.subheader("📈 Technical Overview")

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=data["Date"],
            y=data["Close"],
            mode="lines",
            name="Close"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=data["Date"],
            y=data["MA20"],
            mode="lines",
            name="MA20"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=data["Date"],
            y=data["MA50"],
            mode="lines",
            name="MA50"
        )
    )

    fig.update_layout(
        hovermode="x unified"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("📋 Historical Risk Metrics")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Annualized Volatility",
            format_percent(
                risk["volatility"] * 100
                if risk["volatility"] is not None
                else None
            )
        )

    with c2:
        st.metric(
            "Maximum Drawdown",
            format_percent(
                risk["max_drawdown"] * 100
                if risk["max_drawdown"] is not None
                else None
            )
        )

    with c3:
        st.metric(
            "Sharpe-like Ratio",
            f"{risk['sharpe_like']:.2f}"
            if risk["sharpe_like"] is not None
            else "N/A"
        )

    st.subheader("🧾 Recent Market Data")

    st.dataframe(
        data.tail(20),
        use_container_width=True
    )
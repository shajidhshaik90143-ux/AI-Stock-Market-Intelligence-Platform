import streamlit as st
import plotly.graph_objects as go

from services.market_service import (
    get_history,
    get_quote
)

from utils.formatters import (
    format_currency,
    format_percent
)


def show():

    st.title("🏠 Market Dashboard")

    st.write(
        "Interactive market overview and historical price analysis."
    )

    ticker = st.text_input(
        "Enter stock ticker",
        value="AAPL"
    ).strip().upper()

    period = st.selectbox(
        "Historical period",
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

    quote = get_quote(ticker)

    data = get_history(
        ticker,
        period=period
    )

    if data.empty:

        st.error(
            "No market data found. "
            "Check the ticker symbol."
        )

        return

    price = quote.get("price")

    change_percent = quote.get(
        "change_percent"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Current Price",
            format_currency(price)
        )

    with col2:
        st.metric(
            "Daily Change",
            format_percent(change_percent)
        )

    with col3:
        st.metric(
            "Period High",
            format_currency(
                data["High"].max()
            )
        )

    with col4:
        st.metric(
            "Period Low",
            format_currency(
                data["Low"].min()
            )
        )

    st.subheader(
        f"📈 {ticker} Price History"
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=data["Date"],
            y=data["Close"],
            mode="lines",
            name="Close"
        )
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Price",
        hovermode="x unified"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("📊 Volume")

    volume_fig = go.Figure()

    volume_fig.add_trace(
        go.Bar(
            x=data["Date"],
            y=data["Volume"],
            name="Volume"
        )
    )

    volume_fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Volume"
    )

    st.plotly_chart(
        volume_fig,
        use_container_width=True
    )
import streamlit as st

from database.queries import (
    add_to_watchlist,
    remove_from_watchlist,
    get_watchlist
)

from services.market_service import get_quote

from utils.formatters import (
    format_currency,
    format_percent
)


def show():

    st.title("⭐ Watchlist")

    st.write(
        "Track stocks that you want to research."
    )

    with st.form("add_stock"):

        ticker = st.text_input(
            "Add ticker",
            placeholder="AAPL"
        ).strip().upper()

        submitted = st.form_submit_button(
            "➕ Add Stock"
        )

        if submitted:

            if ticker:

                add_to_watchlist(ticker)

                st.success(
                    f"{ticker} added to watchlist."
                )

                st.rerun()

    stocks = get_watchlist()

    if not stocks:

        st.info(
            "Your watchlist is empty."
        )

        return

    for ticker in stocks:

        quote = get_quote(ticker)

        col1, col2, col3, col4 = st.columns(
            [2, 2, 2, 1]
        )

        with col1:

            st.write(
                f"**{ticker}**"
            )

        with col2:

            st.write(
                format_currency(
                    quote.get("price")
                )
            )

        with col3:

            st.write(
                format_percent(
                    quote.get("change_percent")
                )
            )

        with col4:

            if st.button(
                "🗑️",
                key=f"remove_{ticker}"
            ):

                remove_from_watchlist(
                    ticker
                )

                st.rerun()
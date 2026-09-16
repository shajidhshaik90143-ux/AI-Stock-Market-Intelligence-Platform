import streamlit as st

from services.company_service import (
    get_company_profile,
    get_key_metrics,
    get_income_statement,
    get_balance_sheet,
    get_cashflow
)

from utils.formatters import (
    format_currency,
    format_percent
)


def show():

    st.title("🏢 Company Analysis")

    ticker = st.text_input(
        "Company ticker",
        "AAPL"
    ).strip().upper()

    if not ticker:
        return

    profile = get_company_profile(ticker)

    metrics = get_key_metrics(ticker)

    if not profile:

        st.error(
            "Company information unavailable."
        )

        return

    st.header(
        f"{profile.get('name', ticker)}"
    )

    st.write(
        profile.get(
            "description",
            "No description available."
        )
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.write(
            "**Sector:**",
            profile.get("sector")
        )

        st.write(
            "**Industry:**",
            profile.get("industry")
        )

    with col2:

        st.write(
            "**Country:**",
            profile.get("country")
        )

    with col3:

        st.write(
            "**Employees:**",
            profile.get("employees", "N/A")
        )

    st.subheader(
        "📊 Key Financial Metrics"
    )

    columns = st.columns(4)

    metric_items = list(
        metrics.items()
    )

    for index, (label, value) in enumerate(
        metric_items
    ):

        with columns[index % 4]:

            if label in [
                "Market Cap",
                "Enterprise Value",
                "Revenue",
                "Profit"
            ]:

                display = format_currency(value)

            elif label in [
                "Return on Equity",
                "Profit Margin",
                "Operating Margin",
                "Dividend Yield"
            ]:

                display = format_percent(
                    value * 100
                    if value is not None
                    else None
                )

            else:

                display = (
                    f"{value:.2f}"
                    if isinstance(
                        value,
                        (int, float)
                    )
                    else "N/A"
                )

            st.metric(
                label,
                display
            )

    st.subheader(
        "📑 Financial Statements"
    )

    tab1, tab2, tab3 = st.tabs(
        [
            "Income Statement",
            "Balance Sheet",
            "Cash Flow"
        ]
    )

    with tab1:

        data = get_income_statement(ticker)

        if not data.empty:
            st.dataframe(
                data,
                use_container_width=True
            )
        else:
            st.info("No data available.")

    with tab2:

        data = get_balance_sheet(ticker)

        if not data.empty:
            st.dataframe(
                data,
                use_container_width=True
            )
        else:
            st.info("No data available.")

    with tab3:

        data = get_cashflow(ticker)

        if not data.empty:
            st.dataframe(
                data,
                use_container_width=True
            )
        else:
            st.info("No data available.")
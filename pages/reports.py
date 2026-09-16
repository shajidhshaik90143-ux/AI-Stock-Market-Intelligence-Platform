import os
import streamlit as st

from services.market_service import (
    get_quote,
    get_history
)

from services.company_service import (
    get_company_profile,
    get_key_metrics
)

from services.news_service import (
    get_news,
    format_news_for_ai
)

from services.ai_service import (
    analyze_stock
)

from services.report_service import (
    generate_pdf_report
)


def show():

    st.title("📄 Market Research Reports")

    ticker = st.text_input(
        "Stock ticker",
        "AAPL"
    ).strip().upper()

    if st.button(
        "📑 Generate AI Research Report"
    ):

        if not ticker:

            st.warning(
                "Enter a stock ticker."
            )

            return

        with st.spinner(
            "Collecting market data..."
        ):

            quote = get_quote(ticker)

            history = get_history(
                ticker,
                period="1y"
            )

            profile = get_company_profile(
                ticker
            )

            metrics = get_key_metrics(
                ticker
            )

            news = get_news(
                ticker,
                limit=10
            )

        if history.empty:

            st.error(
                "Unable to retrieve market data."
            )

            return

        context_news = format_news_for_ai(
            news
        )

        with st.spinner(
            "AI is generating the report..."
        ):

            report = analyze_stock(
                ticker=ticker,
                quote=quote,
                metrics=metrics,
                news=context_news
            )

        st.subheader(
            "🤖 AI Research Report"
        )

        st.write(report)

        try:

            pdf_path = generate_pdf_report(
                ticker=ticker,
                title=(
                    f"{ticker} AI Market "
                    "Research Report"
                ),
                content=report
            )

            with open(
                pdf_path,
                "rb"
            ) as file:

                st.download_button(
                    label="⬇️ Download PDF Report",
                    data=file.read(),
                    file_name=os.path.basename(
                        pdf_path
                    ),
                    mime="application/pdf"
                )

        except Exception as e:

            st.error(
                f"PDF generation failed: {e}"
            )
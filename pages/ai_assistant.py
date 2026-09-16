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
    answer_question
)


def show():

    st.title("🤖 AI Market Research Assistant")

    st.write(
        "Ask questions about market data, companies, "
        "financial metrics and recent news."
    )

    ticker = st.text_input(
        "Optional stock ticker",
        "AAPL"
    ).strip().upper()

    question = st.text_area(
        "Ask your question",
        placeholder=(
            "Example: Explain the recent market "
            "performance and important risks."
        )
    )

    if st.button(
        "🤖 Ask AI"
    ):

        if not question.strip():

            st.warning(
                "Please enter a question."
            )

            return

        with st.spinner(
            "Collecting market information..."
        ):

            quote = get_quote(ticker)

            profile = get_company_profile(
                ticker
            )

            metrics = get_key_metrics(
                ticker
            )

            news = get_news(
                ticker,
                limit=8
            )

        context = f"""
Ticker:
{ticker}

Current Quote:
{quote}

Company Profile:
{profile}

Financial Metrics:
{metrics}

Recent News:
{format_news_for_ai(news)}
"""

        with st.spinner(
            "AI is preparing the analysis..."
        ):

            answer = answer_question(
                question,
                context
            )

        st.subheader(
            "🤖 AI Response"
        )

        st.write(answer)

        st.caption(
            "AI-generated analysis may contain errors. "
            "Verify important financial information "
            "using primary sources."
        )
import streamlit as st
from services.news_service import get_news, search_news, format_news_for_ai
from services.ai_service import summarize_news


def show():
    st.title("📰 News Intelligence")
    st.write(
        "Real-time financial news headlines, company coverage, "
        "and AI-powered market sentiment analysis."
    )

    search_mode = st.radio(
        "News Source",
        ["Stock Ticker", "Market Topic / Keyword"],
        horizontal=True
    )

    col1, col2 = st.columns([3, 1])

    if search_mode == "Stock Ticker":
        with col1:
            query = st.text_input(
                "Enter Stock Ticker",
                value="AAPL"
            ).strip().upper()
        with col2:
            st.write("")
            st.write("")
            limit = st.slider("Articles", 5, 25, 10)
    else:
        with col1:
            query = st.text_input(
                "Enter Market Keyword / Search Query",
                value="Artificial Intelligence Stocks"
            ).strip()
        with col2:
            st.write("")
            st.write("")
            limit = st.slider("Articles", 5, 25, 10)

    if not query:
        st.info("Please enter a ticker symbol or market topic above.")
        return

    with st.spinner(f"Fetching latest news for '{query}'..."):
        if search_mode == "Stock Ticker":
            articles = get_news(query, limit=limit)
        else:
            articles = search_news(query, limit=limit)

    if not articles:
        st.warning(f"No news articles found for '{query}'. Please try another search term.")
        return

    # AI Sentiment Analysis Action
    st.subheader("🤖 AI Sentiment & Intelligence Summary")
    if st.button("✨ Generate AI News Intelligence Summary"):
        with st.spinner("AI is analyzing recent headlines and market sentiment..."):
            formatted_news = format_news_for_ai(articles)
            ai_summary = summarize_news(formatted_news, ticker=query)
        st.markdown(ai_summary)
        st.divider()

    st.subheader(f"📋 Top Headlines for {query} ({len(articles)} articles)")

    for idx, article in enumerate(articles, 1):
        with st.container():
            title = article.get("title", "No Title")
            link = article.get("link", "#")
            published = article.get("published", "Recent")
            summary = article.get("summary", "")

            # Render clean card
            st.markdown(f"#### {idx}. [{title}]({link})")
            st.caption(f"🕒 Published: {published}")
            if summary and summary != title:
                # Truncate summary if too long for neat output
                clean_summary = summary.replace("<p>", "").replace("</p>", "").strip()
                if len(clean_summary) > 300:
                    clean_summary = clean_summary[:300] + "..."
                st.write(clean_summary)

            st.markdown(f"[Read full coverage ↗]({link})")
            st.divider()
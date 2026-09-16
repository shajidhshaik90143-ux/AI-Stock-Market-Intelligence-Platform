import streamlit as st

from pages.dashboard import show as dashboard_show
from pages.stock_analysis import show as stock_analysis_show
from pages.watchlist import show as watchlist_show
from pages.news import show as news_show
from pages.company_analysis import show as company_analysis_show
from pages.ai_assistant import show as ai_assistant_show
from pages.analytics import show as analytics_show
from pages.reports import show as reports_show

from database.db import init_database


st.set_page_config(
    page_title="AI Stock & Market Intelligence",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)


def apply_css():
    st.markdown(
        """
        <style>

        .main {
            padding-top: 1rem;
        }

        .block-container {
            max-width: 1400px;
            padding-top: 2rem;
        }

        .metric-card {
            padding: 18px;
            border-radius: 12px;
            border: 1px solid rgba(128,128,128,0.25);
            margin-bottom: 10px;
        }

        .section-title {
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 15px;
        }

        .small-text {
            font-size: 13px;
            opacity: 0.7;
        }

        </style>
        """,
        unsafe_allow_html=True
    )


def main():
    init_database()
    apply_css()

    if "watchlist" not in st.session_state:
        st.session_state.watchlist = [
            "AAPL",
            "MSFT",
            "NVDA",
            "GOOGL",
            "AMZN"
        ]

    st.sidebar.title("📈 AI Market Intelligence")

    st.sidebar.caption(
        "Market research, analytics and AI-powered insights"
    )

    pages = {
        "🏠 Dashboard": dashboard_show,
        "📊 Stock Analysis": stock_analysis_show,
        "⭐ Watchlist": watchlist_show,
        "📰 News Intelligence": news_show,
        "🏢 Company Analysis": company_analysis_show,
        "🤖 AI Assistant": ai_assistant_show,
        "🧠 ML Analytics": analytics_show,
        "📄 Reports": reports_show
    }

    selected_page = st.sidebar.radio(
        "Navigation",
        list(pages.keys())
    )

    st.sidebar.divider()

    st.sidebar.info(
        "⚠️ This application provides market information "
        "and analytical insights. AI/ML outputs are not "
        "guaranteed predictions."
    )

    pages[selected_page]()


if __name__ == "__main__":
    main()
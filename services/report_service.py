import os
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch


EXPORT_DIR = "data/exports"

os.makedirs(EXPORT_DIR, exist_ok=True)


def clean_text(text):
    if text is None:
        return ""

    return str(text).replace("&", "&amp;").replace(
        "<", "&lt;"
    ).replace(">", "&gt;")


def generate_pdf_report(
    ticker,
    title,
    content
):

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    filename = (
        f"{ticker.upper()}_market_report_"
        f"{timestamp}.pdf"
    )

    path = os.path.join(
        EXPORT_DIR,
        filename
    )

    document = SimpleDocTemplate(
        path,
        pagesize=A4,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            clean_text(title),
            styles["Title"]
        )
    )

    story.append(Spacer(1, 0.25 * inch))

    story.append(
        Paragraph(
            f"Ticker: {clean_text(ticker.upper())}",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 0.3 * inch))

    for paragraph in str(content).split("\n"):

        paragraph = paragraph.strip()

        if not paragraph:
            story.append(Spacer(1, 8))
            continue

        story.append(
            Paragraph(
                clean_text(paragraph),
                styles["BodyText"]
            )
        )

        story.append(Spacer(1, 6))

    story.append(Spacer(1, 0.3 * inch))

    story.append(
        Paragraph(
            "Disclaimer: This report is for informational "
            "and research purposes only and does not "
            "constitute personalized investment advice.",
            styles["Italic"]
        )
    )

    document.build(story)

    return path
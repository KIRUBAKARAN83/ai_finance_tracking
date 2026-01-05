from django.http import HttpResponse
from datetime import date

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors

from insights.services import monthly_summary


def monthly_pdf(request):
    today = date.today()
    data = monthly_summary(request.user, today.month, today.year)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        f'attachment; filename="Finance_Report_{today.month}_{today.year}.pdf"'
    )

    # ---------------- DOCUMENT ----------------
    doc = SimpleDocTemplate(
        response,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=50,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()
    story = []

    # ---------------- TITLE ----------------
    title_style = ParagraphStyle(
        name="TitleStyle",
        fontSize=20,
        alignment=TA_CENTER,
        spaceAfter=20,
        textColor=colors.HexColor("#2563eb"),
    )

    story.append(Paragraph("AI Finance Tracker", title_style))
    story.append(Paragraph(
        f"Monthly Financial Report – {today.strftime('%B %Y')}",
        ParagraphStyle(
            name="SubTitle",
            alignment=TA_CENTER,
            fontSize=11,
            textColor=colors.grey,
            spaceAfter=30,
        )
    ))

    # ---------------- SUMMARY TABLE ----------------
    table_data = [
        ["Metric", "Amount (₹)"],
        ["Total Income", f"₹ {data['income']:,}"],
        ["Total Expense", f"₹ {data['expense']:,}"],
        ["Savings", f"₹ {data['savings']:,}"],
    ]

    summary_table = Table(table_data, colWidths=[250, 200])
    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f2937")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
        ("FONT", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONT", (0, 1), (-1, -1), "Helvetica"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
        ("TOPPADDING", (0, 0), (-1, 0), 10),
    ]))

    story.append(summary_table)
    story.append(Spacer(1, 25))

    # ---------------- AI INSIGHTS ----------------
    story.append(Paragraph(
        "AI Insights",
        ParagraphStyle(
            name="SectionHeader",
            fontSize=14,
            spaceAfter=12,
            textColor=colors.HexColor("#16a085"),
        )
    ))

    if data.get("insights"):
        for insight in data["insights"]:
            story.append(Paragraph(
                f"• {insight}",
                styles["Normal"]
            ))
            story.append(Spacer(1, 6))
    else:
        story.append(Paragraph(
            "No insights available for this month.",
            styles["Normal"]
        ))

    story.append(Spacer(1, 30))

    # ---------------- FOOTER ----------------
    story.append(Paragraph(
        "Generated automatically by AI Finance Tracker",
        ParagraphStyle(
            name="Footer",
            alignment=TA_CENTER,
            fontSize=9,
            textColor=colors.grey,
        )
    ))

    # ---------------- BUILD PDF ----------------
    doc.build(story)

    return response

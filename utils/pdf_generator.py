from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak
)

from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)

from reportlab.lib.pagesizes import letter

from reportlab.platypus.flowables import HRFlowable

from reportlab.lib import colors

from reportlab.lib.enums import (
    TA_CENTER,
    TA_JUSTIFY,
    TA_LEFT
)

from reportlab.pdfbase import pdfmetrics

from reportlab.pdfbase.ttfonts import TTFont

from reportlab.pdfgen import canvas

from reportlab.platypus.tables import Table, TableStyle

from datetime import datetime



# -------------------------------------------------
# PAGE NUMBERING
# -------------------------------------------------

def add_page_number(canvas, doc):

    page_num = canvas.getPageNumber()

    text = f"{page_num}"

    canvas.setFont(
        "Times-Roman",
        10
    )

    canvas.drawRightString(
        580,
        20,
        text
    )



# -------------------------------------------------
# SECTION TITLE
# -------------------------------------------------

def add_section_title(

    story,
    title,
    styles
):

    heading = Paragraph(

        f"""
        <b>{title}</b>
        """,

        styles["SectionHeading"]
    )

    story.append(heading)

    line = HRFlowable(
        width="100%",
        thickness=0.8,
        color=colors.black
    )

    story.append(line)

    story.append(
        Spacer(1, 10)
    )



# -------------------------------------------------
# PARAGRAPH
# -------------------------------------------------

def add_paragraph(

    story,
    text,
    styles
):

    if not text:

        text = "No information available."

    paragraph = Paragraph(
        text,
        styles["ResearchBody"]
    )

    story.append(paragraph)

    story.append(
        Spacer(1, 12)
    )



# -------------------------------------------------
# BULLETS
# -------------------------------------------------

def add_bullets(

    story,
    items,
    styles
):

    if not items:

        items = [
            "No information available."
        ]

    for item in items:

        bullet = Paragraph(

            f"• {item}",

            styles["BulletStyle"]
        )

        story.append(bullet)

        story.append(
            Spacer(1, 5)
        )



# -------------------------------------------------
# REFERENCES
# -------------------------------------------------

def add_references(

    story,
    references,
    styles
):

    if not references:

        references = [
            "No references available."
        ]

    for index, ref in enumerate(references, start=1):

        reference = Paragraph(

            f"""
            [{index}] {ref}
            """,

            styles["ReferenceStyle"]
        )

        story.append(reference)

        story.append(
            Spacer(1, 6)
        )



# -------------------------------------------------
# MAIN PDF FUNCTION
# -------------------------------------------------

def generate_pdf_report(

    report,

    filename="research_paper.pdf"
):

    doc = SimpleDocTemplate(

        filename,

        pagesize=letter,

        rightMargin=55,
        leftMargin=55,

        topMargin=50,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()



    # -------------------------------------------------
    # CUSTOM STYLES
    # -------------------------------------------------

    styles.add(
        ParagraphStyle(

            name="PaperTitle",

            fontName="Times-Bold",

            fontSize=22,

            leading=28,

            alignment=TA_CENTER,

            spaceAfter=20
        )
    )

    styles.add(
        ParagraphStyle(

            name="AuthorStyle",

            fontName="Times-Roman",

            fontSize=12,

            alignment=TA_CENTER,

            spaceAfter=25
        )
    )

    styles.add(
        ParagraphStyle(

            name="AbstractHeading",

            fontName="Times-Bold",

            fontSize=14,

            leading=18,

            spaceAfter=10
        )
    )

    styles.add(
        ParagraphStyle(

            name="SectionHeading",

            fontName="Times-Bold",

            fontSize=15,

            leading=20,

            textColor=colors.black,

            spaceBefore=10,

            spaceAfter=10
        )
    )

    styles.add(
        ParagraphStyle(

            name="ResearchBody",

            fontName="Times-Roman",

            fontSize=11,

            leading=20,

            alignment=TA_JUSTIFY,

            firstLineIndent=20,

            spaceAfter=12
        )
    )

    styles.add(
        ParagraphStyle(

            name="BulletStyle",

            fontName="Times-Roman",

            fontSize=11,

            leading=18,

            leftIndent=18,

            alignment=TA_JUSTIFY
        )
    )

    styles.add(
        ParagraphStyle(

            name="ReferenceStyle",

            fontName="Times-Roman",

            fontSize=10,

            leading=16,

            leftIndent=15
        )
    )



    story = []



    # -------------------------------------------------
    # TITLE
    # -------------------------------------------------

    title = Paragraph(

        report.get(
            "title",
            "Research Paper"
        ),

        styles["PaperTitle"]
    )

    story.append(title)



    # -------------------------------------------------
    # AUTHOR + DATE
    # -------------------------------------------------

    author_block = Paragraph(

    """
    Autonomous Multi-Agent Research System
    """,

    styles["AuthorStyle"]
    )

    story.append(author_block)



    # -------------------------------------------------
    # ABSTRACT
    # -------------------------------------------------

    abstract_heading = Paragraph(
        "Abstract",
        styles["AbstractHeading"]
    )

    story.append(abstract_heading)

    story.append(
        Spacer(1, 4)
    )

    add_paragraph(

        story,

        report.get(
            "abstract",
            ""
        ),

        styles
    )
    # -------------------------------------------------
    # KEYWORDS
    # -------------------------------------------------

    keywords = ", ".join(

        report.get(
            "keywords",
            []
        )
    )

    keyword_para = Paragraph(

        f"""
        <b>Keywords:</b>
        {keywords}
        """,

        styles["ResearchBody"]
    )

    story.append(keyword_para)

    story.append(
        Spacer(1, 18)
    )


    print(report)
    # -------------------------------------------------
    # INTRODUCTION
    # -------------------------------------------------

    add_section_title(
        story,
        "1. Introduction",
        styles
    )

    add_paragraph(

        story,

        report.get(
            "introduction",
            ""
        ),

        styles
    )

    # -------------------------------------------------
    # METHODOLOGY
    # -------------------------------------------------

    add_section_title(
        story,
        "2. Methodology",
        styles
    )

    add_paragraph(

        story,

        report.get(
            "methodology",
            ""
        ),

        styles
    )

    # -------------------------------------------------
    # DYNAMIC SECTIONS
    # -------------------------------------------------

    section_number = 3

    for section in report.get(
        "dynamic_sections",
        []
    ):

        add_section_title(

            story,

            f"{section_number}. {section.get('heading', '')}",

            styles
        )

        add_paragraph(

            story,

            section.get(
                "content",
                ""
            ),

            styles
        )

        section_number += 1

    
    # -------------------------------------------------
    # CONCLUSION
    # -------------------------------------------------

    add_section_title(
        story,
        f"{section_number}. Conclusion",
        styles
    )

    add_paragraph(

        story,

        report.get(
            "conclusion",
            ""
        ),

        styles
    )



    add_section_title(
        story,
        "References",
        styles
    )

    add_references(

        story,

        report.get(
            "references",
            []
        ),

        styles
    )



    # -------------------------------------------------
    # BUILD
    # -------------------------------------------------

    doc.build(

        story,

        onFirstPage=add_page_number,

        onLaterPages=add_page_number
    )

    return filename
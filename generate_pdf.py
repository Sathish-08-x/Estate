import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, 
    PageBreak, Preformatted, Image as RLImage, KeepTogether
)
from reportlab.pdfgen import canvas
from PIL import Image as PILImage

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#555555"))
        self.setStrokeColor(colors.HexColor("#dddddd"))
        self.setLineWidth(0.5)
        self.line(40, 40, letter[0] - 40, 40)
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 40, 25, page_text)
        self.drawString(40, 25, "CSE326 - CA1 Project Source Code & Assets | EstateFlow")
        self.restoreState()

def get_scaled_image(path, max_width=480, max_height=320):
    if not os.path.exists(path):
        return None
    try:
        with PILImage.open(path) as img:
            w, h = img.size
            ratio = min(max_width / w, max_height / h, 1.0)
            return RLImage(path, width=w * ratio, height=h * ratio)
    except Exception:
        return None

def build_pdf():
    pdf_filename = "CSE326_CA1_EstateFlow_Project_Code_And_Images.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=45,
        bottomMargin=55
    )

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=colors.HexColor("#0d47a1"),
        alignment=1,
        spaceAfter=10
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#333333"),
        alignment=1,
        spaceAfter=20
    )

    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#0d47a1"),
        spaceBefore=14,
        spaceAfter=8
    )

    image_caption_style = ParagraphStyle(
        'ImageCaption',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#1565c0"),
        alignment=1,
        spaceBefore=5,
        spaceAfter=15
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        fontName='Courier',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#1b1f23")
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#333333"),
        spaceAfter=8
    )

    story = []

    logo_path = os.path.join("assets", "logo.png")
    if os.path.exists(logo_path):
        logo_img = get_scaled_image(logo_path, max_width=100, max_height=100)
        if logo_img:
            story.append(Table([[logo_img]], colWidths=[letter[0] - 80], style=[
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10)
            ]))

    story.append(Paragraph("Lovely Professional University", title_style))
    story.append(Paragraph("School of Computer Science and Engineering", subtitle_style))

    story.append(Paragraph("<b>Course Code:</b> CSE326 - Web Development", body_style))
    story.append(Paragraph("<b>Assessment:</b> CA1 Project-Based Assessment (30 Marks)", body_style))
    story.append(Paragraph("<b>Project Title:</b> EstateFlow - Property Lead Management System", body_style))
    story.append(Paragraph("<b>Submission Scope:</b> Complete Source Code, Graphical Assets, UI Screenshots & Project Rubrics", body_style))
    story.append(Spacer(1, 10))

    overview_text = (
        "<b>Project Executive Summary:</b><br/>"
        "EstateFlow is a specialized Real Estate Lead Management Web Application built using pure HTML5, CSS3, "
        "and Vanilla JavaScript. It delivers four core interconnected modules: an interactive KPI Dashboard, a complete "
        "Leads Registry with inline stage editing and state sync, a Kanban-style Sales Pipeline categorized by deal stages, "
        "and a Follow-up Schedule with priority indicators. Data persistence is engineered client-side using browser LocalStorage "
        "for zero-backend continuous state retention."
    )
    story.append(Paragraph(overview_text, body_style))
    story.append(Spacer(1, 10))

    story.append(PageBreak())
    story.append(Paragraph("Section 1: Application Visual Assets & Screenshots", section_heading))
    story.append(Paragraph("This section contains all project screenshots, system graphics, and the official assessment rubrics.", body_style))
    story.append(Spacer(1, 10))

    images_to_embed = [
        ("assets/logo.png", "Figure 1: EstateFlow Official Application Logo", 120, 120),
        ("assets/ui_dashboard_metrics.png", "Figure 2: Real-time Metric Cards on the Dashboard (index.html)", 500, 160),
        ("assets/ui_add_lead_form.png", "Figure 3: New Property Lead Submission Form (index.html)", 480, 280),
        ("assets/ui_pipeline_board_1.png", "Figure 4: Sales Pipeline Kanban Board - New Leads Column (sales.html)", 500, 220),
        ("assets/ui_pipeline_board_2.png", "Figure 5: Sales Pipeline - Contacted, Negotiation & Closed Columns (sales.html)", 500, 220),
        ("assets/rubric_guidelines_p1.jpg", "Figure 6: Assessment Rubric - Marks Distribution & Viva Scope", 420, 360),
        ("assets/rubric_guidelines_p2.jpg", "Figure 7: Assessment Rubric - Video Presentation Guidelines", 420, 360),
        ("assets/rubric_guidelines_p3.jpg", "Figure 8: Assessment Rubric - Excel Submission Template Structure", 420, 360),
        ("assets/rubric_guidelines_p4.jpg", "Figure 9: Assessment Rubric - Final Submission & Evaluation Guidelines", 420, 360)
    ]

    for img_path, caption, mw, mh in images_to_embed:
        img_obj = get_scaled_image(img_path, max_width=mw, max_height=mh)
        if img_obj:
            story.append(KeepTogether([
                Table([[img_obj]], colWidths=[letter[0] - 80], style=[
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8f9fa")),
                    ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#dddddd")),
                    ('PADDING', (0, 0), (-1, -1), 8)
                ]),
                Paragraph(caption, image_caption_style),
                Spacer(1, 10)
            ]))

    files_to_include = [
        ("index.html", "Dashboard & New Lead Registration Interface"),
        ("allleads.html", "All Leads Registry & Inline Stage Management"),
        ("sales.html", "Interactive Sales Pipeline Kanban Board"),
        ("followup.html", "Follow-up Schedule & Priority Task Tracker"),
        ("style.css", "Application Stylesheet & Visual Components"),
        ("script.js", "Application Logic & LocalStorage State Synchronization")
    ]

    story.append(PageBreak())
    story.append(Paragraph("Section 2: Complete Project Source Code", section_heading))
    story.append(Paragraph("This section contains the full, verbatim source code for all modules of EstateFlow.", body_style))
    story.append(Spacer(1, 10))

    for fname, desc in files_to_include:
        story.append(PageBreak())
        story.append(Paragraph(f"Source Code: {fname}", section_heading))
        story.append(Paragraph(f"<i>Component: {desc}</i>", body_style))
        story.append(Spacer(1, 8))

        if os.path.exists(fname):
            with open(fname, 'r', encoding='utf-8') as f:
                content = f.read()
            
            lines = content.split('\n')
            chunk_size = 65
            for i in range(0, len(lines), chunk_size):
                chunk_lines = lines[i:i + chunk_size]
                chunk_text = "\n".join(chunk_lines)
                formatted_block = Preformatted(chunk_text, code_style)
                block_table = Table([[formatted_block]], colWidths=[letter[0] - 80])
                block_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8f9fa")),
                    ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#e0e0e0")),
                    ('PADDING', (0, 0), (-1, -1), 6),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ]))
                story.append(block_table)
                story.append(Spacer(1, 6))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated {pdf_filename}")

if __name__ == '__main__':
    build_pdf()

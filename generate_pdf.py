import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Preformatted
from reportlab.pdfgen import canvas

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
        self.drawString(40, 25, "CSE326 - CA1 Project Source Code | EstateFlow")
        self.restoreState()

def build_pdf():
    pdf_filename = "CSE326_CA1_EstateFlow_Project_Code.pdf"
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
        spaceAfter=25
    )

    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#0d47a1"),
        spaceBefore=15,
        spaceAfter=8
    )

    file_header_style = ParagraphStyle(
        'FileHeader',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#1565c0"),
        spaceBefore=12,
        spaceAfter=6
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
        textColor=colors.HexColor("#333333")
    )

    story = []

    story.append(Paragraph("Lovely Professional University", title_style))
    story.append(Paragraph("School of Computer Science and Engineering", subtitle_style))
    story.append(Spacer(1, 15))

    story.append(Paragraph("<b>Course Code:</b> CSE326 - Web Development", body_style))
    story.append(Paragraph("<b>Assessment:</b> CA1 Project-Based Assessment", body_style))
    story.append(Paragraph("<b>Project Title:</b> EstateFlow - Property Lead Management System", body_style))
    story.append(Spacer(1, 15))

    overview_text = (
        "<b>Project Overview:</b><br/>"
        "EstateFlow is a specialized Real Estate Lead Management Web Application built using HTML5, CSS3, "
        "and JavaScript. The application enables property consultants and agencies to systematically capture, "
        "track, and progress real estate leads across multiple stages of the sales pipeline. Features include an "
        "interactive dashboard with real-time analytics, all leads registry with inline stage updates, dynamic sales pipeline "
        "board categorized by deal stages, and an integrated follow-up schedule. All data is persisted locally via the browser's "
        "LocalStorage API ensuring continuous state retention across sessions."
    )
    story.append(Paragraph(overview_text, body_style))
    story.append(Spacer(1, 20))

    files_to_include = [
        ("index.html", "Dashboard & New Lead Registration Interface"),
        ("allleads.html", "All Leads Registry & Inline Stage Management"),
        ("sales.html", "Interactive Sales Pipeline Kanban Board"),
        ("followup.html", "Follow-up Schedule & Priority Task Tracker"),
        ("style.css", "Application Stylesheet & Visual Components"),
        ("script.js", "Application Logic & LocalStorage State Synchronization")
    ]

    for fname, desc in files_to_include:
        story.append(PageBreak())
        story.append(Paragraph(f"Source Code: {fname}", section_heading))
        story.append(Paragraph(f"<i>Component: {desc}</i>", body_style))
        story.append(Spacer(1, 10))

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

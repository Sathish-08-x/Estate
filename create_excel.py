import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "CA1 Submission"

ws.views.sheetView[0].showGridLines = True

headers = [
    "Project Name & Title",
    "Team Name",
    "Course Code",
    "Registration Number(s)",
    "GitHub Link",
    "Deployed Link",
    "Video Presentation Link"
]

header_fill = PatternFill(start_color="1F497D", end_color="1F497D", fill_type="solid")
header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
center_align = Alignment(horizontal="center", vertical="center", wrap_text=True)
left_align = Alignment(horizontal="left", vertical="center", wrap_text=True)

thin_border = Border(
    left=Side(style='thin', color='D9D9D9'),
    right=Side(style='thin', color='D9D9D9'),
    top=Side(style='thin', color='D9D9D9'),
    bottom=Side(style='thin', color='D9D9D9')
)

for col_num, header in enumerate(headers, 1):
    cell = ws.cell(row=1, column=col_num)
    cell.value = header
    cell.fill = header_fill
    cell.font = header_font
    cell.alignment = center_align
    cell.border = thin_border

sample_data = [
    "EstateFlow - Property Lead Management System",
    "Team EstateFlow",
    "CSE326",
    "Reg. No. 1",
    "https://github.com/<your-username>/CSE326-CA1",
    "https://<your-username>.github.io/CSE326-CA1/",
    "https://youtu.be/<your-video-link>"
]

data_font = Font(name="Calibri", size=10)
for col_num, val in enumerate(sample_data, 1):
    cell = ws.cell(row=2, column=col_num)
    cell.value = val
    cell.font = data_font
    cell.alignment = left_align
    cell.border = thin_border

col_widths = [35, 18, 14, 25, 42, 42, 38]
for i, width in enumerate(col_widths, 1):
    ws.column_dimensions[get_column_letter(i)].width = width

ws.row_dimensions[1].height = 28
ws.row_dimensions[2].height = 24

excel_filename = "CA1_Project_Submission_CSE326.xlsx"
wb.save(excel_filename)
print(f"Successfully created {excel_filename}")

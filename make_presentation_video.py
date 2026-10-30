import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import imageio.v3 as iio

WIDTH = 1920
HEIGHT = 1080
FPS = 15
TOTAL_SECONDS = 240
NUM_SLIDES = 12
SECONDS_PER_SLIDE = TOTAL_SECONDS // NUM_SLIDES
FRAMES_PER_SLIDE = FPS * SECONDS_PER_SLIDE
TOTAL_FRAMES = NUM_SLIDES * FRAMES_PER_SLIDE

SLIDES = [
    {
        "tag": "CSE326 - CA1 PROJECT-BASED ASSESSMENT",
        "title": "EstateFlow",
        "subtitle": "Real Estate Lead Management System",
        "image": "assets/logo.png",
        "img_box": (1320, 260, 1800, 740),
        "points": [
            "Course: CSE326 - Web Development",
            "Project Type: Problem Statement-Based CA1 Assessment (30 Marks)",
            "Evaluation: Functionality (15M) | Viva (10M) | Video Presentation (5M)",
            "Technologies Used: Semantic HTML5, Custom CSS3, Vanilla JavaScript (ES6+)",
            "Data Architecture: Client-Side CRM with LocalStorage State Synchronization"
        ],
        "accent": "#0d47a1"
    },
    {
        "tag": "1. PROBLEM IDENTIFICATION & MOTIVATION",
        "title": "The Real Estate Challenge",
        "subtitle": "Why Traditional Lead Tracking Fails",
        "image": None,
        "points": [
            "Brokers lose valuable client inquiries due to disorganized notebooks and messaging apps",
            "Lack of pipeline visibility: Inability to track leads across New, Site Visit, Negotiation, and Closed Won",
            "Missed follow-up dates directly lead to competitor poaching and lost property commissions",
            "Existing CRM software is overly bloated, complex, expensive, and requires server backends",
            "Motivation: Build a responsive, fast, zero-dependency web application for daily consultant workflow"
        ],
        "accent": "#c62828"
    },
    {
        "tag": "2. PROPOSED SOLUTION & ARCHITECTURE",
        "title": "The EstateFlow Architecture",
        "subtitle": "Four Core Integrated Modules",
        "image": None,
        "points": [
            "Interactive Dashboard: Live KPI cards summarizing active leads, visits, negotiations, and closed deals",
            "Lead Ingestion Form: Standardized capture of Name, Buyer/Seller type, Property Interest, Budget, & Dates",
            "All Leads Registry: Comprehensive searchable table with inline stage dropdowns and Save buttons",
            "Kanban Sales Pipeline: Visual board distributing inquiries across progressive stages with priority badges",
            "Follow-up Scheduler: Priority-ranked timeline ensuring timely client contact and appointment tracking"
        ],
        "accent": "#1565c0"
    },
    {
        "tag": "3. FEATURE DEMO: ANALYTICS DASHBOARD",
        "title": "Real-time KPI Dashboard",
        "subtitle": "High-Level Sales Funnel Visibility",
        "image": "assets/ui_dashboard_metrics.png",
        "img_box": (1180, 320, 1820, 680),
        "points": [
            "Four responsive KPI cards: Total Active Leads, Site Visits, In Negotiation, Closed Won",
            "CSS3 hover-lift transitions and pulse animations for modern interactivity",
            "Counters automatically recalculate from the LocalStorage stage engine",
            "Provides consultants with an instant overview of monthly deal progress"
        ],
        "accent": "#2e7d32"
    },
    {
        "tag": "4. FEATURE DEMO: LEAD INGESTION",
        "title": "New Lead Registration Form",
        "subtitle": "Structured Data Capture & Validation",
        "image": "assets/ui_add_lead_form.png",
        "img_box": (1220, 240, 1820, 840),
        "points": [
            "Captures: Client Name, Buyer/Seller radio toggle, Property Interest, Budget, Stage, Priority, & Date",
            "Form validation ensures no empty records are ingested",
            "On submission, the lead is stored in LocalStorage, incrementing the dashboard counts",
            "Newly submitted leads automatically appear in the All Leads table and Follow-up Schedule"
        ],
        "accent": "#ef6c00"
    },
    {
        "tag": "5. FEATURE DEMO: ALL LEADS REGISTRY",
        "title": "Comprehensive Leads Table",
        "subtitle": "Inline Editing & Stage State Synchronization",
        "image": None,
        "points": [
            "Full table listing: Client Name, Type, Interest, Budget, Stage, Priority, Follow-up Date, & Phone",
            "Inline Stage Dropdown: Change client status between New, Site Visit, In Negotiation, and Closed Won",
            "Save Button: Immediately updates the Stage text cell and writes changes to LocalStorage",
            "Preserves user selections across page reloads and synchronizes with the Sales Pipeline board",
            "Custom leads added from the dashboard dynamically append as fully interactive table rows"
        ],
        "accent": "#00838f"
    },
    {
        "tag": "6. FEATURE DEMO: SALES PIPELINE (KANBAN)",
        "title": "Visual Workflow Board - Part 1",
        "subtitle": "New Inquiries & Initial Stage Sorting",
        "image": "assets/ui_pipeline_board_1.png",
        "img_box": (1180, 280, 1820, 760),
        "points": [
            "Kanban-style multi-column layout built with CSS Flexbox",
            "New Leads Column: Displays incoming prospect cards with budget and property icons",
            "Priority Color Indicators: Red left border for High Priority, Yellow for Medium, Green for Low",
            "Clean visual hierarchy highlighting client budget (Cr) and housing preference (Apartment/House/Condo)"
        ],
        "accent": "#6a1b9a"
    },
    {
        "tag": "7. FEATURE DEMO: SALES PIPELINE (ADVANCED)",
        "title": "Visual Workflow Board - Part 2",
        "subtitle": "Negotiation & Closed Won Deal Progression",
        "image": "assets/ui_pipeline_board_2.png",
        "img_box": (1180, 280, 1820, 760),
        "points": [
            "Contacted, In Negotiation, and Closed Won workflow columns",
            "Moving a lead's stage in the table instantly moves the corresponding card on this pipeline board",
            "Empty state handling: Displays 'No deals closed yet' placeholder when a stage is empty",
            "Smooth hover scale and drop-shadow effects for tactile feedback"
        ],
        "accent": "#4a148c"
    },
    {
        "tag": "8. FEATURE DEMO: FOLLOW-UP SCHEDULE",
        "title": "Integrated Follow-up Schedule",
        "subtitle": "Systematic Appointment & Call Tracking",
        "image": None,
        "points": [
            "Follow-up calendar table displaying client deadlines, contact numbers, and lead stages",
            "Summary metrics: Total Scheduled Follow-ups, High Priority Calls, Site Visits, and Won Deals",
            "Status column tracks progression from Pending to Scheduled, Active, and Won",
            "Cross-linked sidebar enables seamless navigation across all 4 system views"
        ],
        "accent": "#00695c"
    },
    {
        "tag": "9. TECHNICAL IMPLEMENTATION",
        "title": "Pure Web Standards Implementation",
        "subtitle": "Semantic HTML5, Modular CSS3 & Vanilla JavaScript",
        "image": None,
        "points": [
            "HTML5: Semantic document structure (<header>, <nav>, <main>, <form>, <table>)",
            "CSS3: Responsive Flexbox design, CSS variables, keyframe animations, card hover transitions",
            "JavaScript (ES6+): Event delegation, dynamic DOM construction, JSON data serialization",
            "LocalStorage API: Client-side storage engine enabling zero-backend persistence across browser tabs"
        ],
        "accent": "#283593"
    },
    {
        "tag": "10. ACADEMIC RUBRICS & ASSESSMENT ALIGNMENT",
        "title": "CA1 Evaluation Compliance",
        "subtitle": "Meeting Every University Instruction & Benchmark",
        "image": "assets/rubric_guidelines_p1.jpg",
        "img_box": (1240, 240, 1800, 840),
        "points": [
            "Functionality & UI (15 Marks): Complete problem statement implementation and bug-free UI",
            "Viva Preparation (10 Marks): Clear architectural understanding, code explanations, and technical depth",
            "Video Presentation (5 Marks): 4-minute demonstration covering problem, solution, features, and code",
            "UMS Submission: Complete Excel sheet (.xlsx) and PDF documentation generated"
        ],
        "accent": "#37474f"
    },
    {
        "tag": "11. PROJECT CONCLUSION & SUBMISSION",
        "title": "Conclusion & Team Contributions",
        "subtitle": "EstateFlow CA1 Assessment Deliverables",
        "image": "assets/logo.png",
        "img_box": (1320, 280, 1780, 740),
        "points": [
            "Git Repository: Structured commit history on branch 'main' with clean, comment-preserved code",
            "Live Cloud Deployment: Hosted on GitHub Pages with instant online accessibility",
            "Documentation: Comprehensive 31-page code & asset PDF (CSE326_CA1_EstateFlow_Project_Code_And_Images.pdf)",
            "UMS Submission File: CA1_Project_Submission_CSE326.xlsx pre-filled with all project links",
            "Final Status: Fully compliant with all CSE326 evaluation criteria"
        ],
        "accent": "#1b5e20"
    }
]

def get_font(size, bold=False):
    font_names = [
        "C:\\Windows\\Fonts\\segoeuib.ttf" if bold else "C:\\Windows\\Fonts\\segoeui.ttf",
        "C:\\Windows\\Fonts\\arialbd.ttf" if bold else "C:\\Windows\\Fonts\\arial.ttf",
        "C:\\Windows\\Fonts\\calibrib.ttf" if bold else "C:\\Windows\\Fonts\\calibri.ttf"
    ]
    for path in font_names:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()

loaded_images = {}
for slide in SLIDES:
    p = slide.get("image")
    if p and os.path.exists(p) and p not in loaded_images:
        try:
            loaded_images[p] = Image.open(p).convert("RGBA")
        except Exception:
            pass

def render_slide(slide_idx, slide_progress, total_seconds_elapsed):
    slide = SLIDES[slide_idx]
    img = Image.new("RGB", (WIDTH, HEIGHT), "#f8f9fa")
    draw = ImageDraw.Draw(img)

    accent_color = slide["accent"]
    draw.rectangle([0, 0, WIDTH, 16], fill=accent_color)
    draw.rectangle([0, 0, 18, HEIGHT], fill=accent_color)

    font_tag = get_font(22, bold=True)
    font_title = get_font(50, bold=True)
    font_subtitle = get_font(26, bold=False)
    font_bullet = get_font(24, bold=False)
    font_footer = get_font(18, bold=False)
    font_timer = get_font(20, bold=True)

    draw.text((90, 55), slide["tag"], fill=accent_color, font=font_tag)
    draw.text((90, 95), slide["title"], fill="#020e21", font=font_title)
    draw.text((90, 168), slide["subtitle"], fill="#555555", font=font_subtitle)

    draw.line([(90, 218), (WIDTH - 90, 218)], fill="#e0e0e0", width=2)

    has_image = bool(slide.get("image") and slide["image"] in loaded_images)
    card_w = 1040 if has_image else (WIDTH - 180)
    card_y = 250
    card_h = 710
    draw.rectangle([90, card_y, 90 + card_w, card_y + card_h], fill="#ffffff", outline="#e0e0e0", width=2)
    draw.rectangle([90, card_y, 102, card_y + card_h], fill=accent_color)

    y = card_y + 45
    for pt in slide["points"]:
        draw.ellipse([130, y + 6, 144, y + 20], fill=accent_color)
        
        words = pt.split()
        lines = []
        cur_line = []
        max_chars = 62 if has_image else 95
        for w in words:
            if len(" ".join(cur_line + [w])) <= max_chars:
                cur_line.append(w)
            else:
                lines.append(" ".join(cur_line))
                cur_line = [w]
        if cur_line:
            lines.append(" ".join(cur_line))

        for line_text in lines:
            draw.text((165, y), line_text, fill="#1f2937", font=font_bullet)
            y += 34
        y += 24

    if has_image:
        box = slide["img_box"]
        target_w = box[2] - box[0]
        target_h = box[3] - box[1]
        raw_img = loaded_images[slide["image"]]
        
        draw.rectangle([box[0] - 10, box[1] - 10, box[2] + 10, box[3] + 10], fill="#ffffff", outline="#dddddd", width=2)
        
        iw, ih = raw_img.size
        ratio = min(target_w / iw, target_h / ih)
        scaled_w = int(iw * ratio)
        scaled_h = int(ih * ratio)
        resized_img = raw_img.resize((scaled_w, scaled_h), Image.Resampling.LANCZOS)
        
        offset_x = box[0] + (target_w - scaled_w) // 2
        offset_y = box[1] + (target_h - scaled_h) // 2
        
        if resized_img.mode == 'RGBA':
            img.paste(resized_img, (offset_x, offset_y), resized_img)
        else:
            img.paste(resized_img, (offset_x, offset_y))

    mins = int(total_seconds_elapsed // 60)
    secs = int(total_seconds_elapsed % 60)
    timer_str = f"{mins:02d}:{secs:02d} / 04:00"
    
    footer_text = f"Slide {slide_idx + 1} of {len(SLIDES)} | EstateFlow CA1 Presentation | CSE326"
    draw.text((90, HEIGHT - 55), footer_text, fill="#888888", font=font_footer)
    draw.text((WIDTH - 240, HEIGHT - 58), timer_str, fill=accent_color, font=font_timer)

    total_progress = total_seconds_elapsed / TOTAL_SECONDS
    bar_width = int(WIDTH * total_progress)
    draw.rectangle([0, HEIGHT - 10, bar_width, HEIGHT], fill=accent_color)

    return np.array(img)

def generate_video():
    output_filename = "EstateFlow_4Min_Presentation_Video.mp4"
    print(f"Generating 4-minute presentation video: {output_filename}...")
    print(f"Total Duration: {TOTAL_SECONDS}s (4 mins), FPS: {FPS}, Total Frames: {TOTAL_FRAMES}")

    writer = iio.imopen(output_filename, "w", plugin="pyav")
    writer.init_video_stream("libx264", fps=FPS, pixel_format="yuv420p")

    frame_count = 0
    for s_idx in range(NUM_SLIDES):
        slide_title = SLIDES[s_idx]["title"]
        print(f"Rendering Slide {s_idx + 1}/{NUM_SLIDES}: {slide_title} ({SECONDS_PER_SLIDE}s)...")
        for f in range(FRAMES_PER_SLIDE):
            prog = f / FRAMES_PER_SLIDE
            elapsed_sec = (s_idx * SECONDS_PER_SLIDE) + (prog * SECONDS_PER_SLIDE)
            frame = render_slide(s_idx, prog, elapsed_sec)
            writer.write_frame(frame)
            frame_count += 1

    writer.close()
    file_size_mb = os.path.getsize(output_filename) / (1024 * 1024)
    print(f"SUCCESS: Generated {output_filename} ({file_size_mb:.2f} MB, {frame_count} frames, {TOTAL_SECONDS}s / exactly 4:00 mins)!")

if __name__ == '__main__':
    generate_video()

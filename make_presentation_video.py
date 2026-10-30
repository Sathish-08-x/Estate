import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import imageio.v3 as iio

WIDTH = 1920
HEIGHT = 1080
FPS = 30
SECONDS_PER_SLIDE = 5
FRAMES_PER_SLIDE = FPS * SECONDS_PER_SLIDE

SLIDES = [
    {
        "tag": "CSE326 - CA1 PROJECT PRESENTATION",
        "title": "EstateFlow",
        "subtitle": "Property Lead Management System",
        "points": [
            "Course: CSE326 - Web Development",
            "Project Type: Problem Statement-Based CA1 Assessment",
            "Technologies: HTML5, CSS3, Modern JavaScript (ES6+)",
            "Key Architecture: Client-Side CRM with LocalStorage State Engine"
        ],
        "accent": "#0d47a1"
    },
    {
        "tag": "1. PROBLEM IDENTIFICATION & MOTIVATION",
        "title": "The Real Estate Challenge",
        "subtitle": "Why Property Lead Management Matters",
        "points": [
            "Brokers & agencies lose prospective buyers due to fragmented tracking across chats & notebooks",
            "Lack of visibility into lead stages: New, Site Visit, In Negotiation, Closed Won",
            "Missed follow-up dates directly result in dropped real estate deals",
            "Need for an intuitive, zero-dependency, lightweight web dashboard for real-time tracking"
        ],
        "accent": "#c62828"
    },
    {
        "tag": "2. PROPOSED SOLUTION & ARCHITECTURE",
        "title": "EstateFlow Solution",
        "subtitle": "Comprehensive Lead Lifecycle Management",
        "points": [
            "Unified Single-Page Experience with four interconnected modules",
            "Live Analytics Dashboard: Instant counts of active, scheduled, and won deals",
            "Interactive Lead Registry: Inline stage updating with immediate table reflection",
            "Kanban Sales Pipeline: Visual categorization of property inquiries by progress stage",
            "Follow-up Scheduler: Priority-coded reminders ensuring timely client engagement"
        ],
        "accent": "#1565c0"
    },
    {
        "tag": "3. SYSTEM MODULE DEMO - DASHBOARD",
        "title": "Interactive Dashboard & Lead Capture",
        "subtitle": "Real-time Metrics & Ingestion",
        "points": [
            "Four responsive KPI cards: Total Active Leads, Site Visits, In Negotiation, Closed Won",
            "CSS hover-lift & pulse animations for enhanced user engagement",
            "New Lead Form: Captures Client Name, Buyer/Seller Type, Property Interest, Budget, & Dates",
            "Automatic validation and real-time dashboard counter increments on submission"
        ],
        "accent": "#2e7d32"
    },
    {
        "tag": "4. SYSTEM MODULE DEMO - ALL LEADS",
        "title": "All Registered Leads Registry",
        "subtitle": "Dynamic Table with Inline Stage Updates",
        "points": [
            "Tabular display of clients with Budget, Phone, Priority, and Follow-up Dates",
            "Inline Stage Dropdown: Change stage to Site Visit, In Negotiation, or Closed Won",
            "Save Button: Immediately updates the Stage column text and syncs across all pages",
            "Bi-directional state persistence: Newly registered leads automatically append to the table"
        ],
        "accent": "#ef6c00"
    },
    {
        "tag": "5. SYSTEM MODULE DEMO - SALES PIPELINE",
        "title": "Kanban Sales Pipeline Board",
        "subtitle": "Visual Workflow Categorization",
        "points": [
            "Four dedicated workflow columns: New Leads, Contacted, In Negotiation, and Closed Won",
            "Priority-coded left border badges: High (Red), Medium (Orange), Low (Green)",
            "Dynamic card population from LocalStorage data engine",
            "Fallback empty states: Informative messages when columns have no active deals"
        ],
        "accent": "#6a1b9a"
    },
    {
        "tag": "6. SYSTEM MODULE DEMO - FOLLOW-UP SCHEDULE",
        "title": "Integrated Follow-up Schedule",
        "subtitle": "Priority Reminders & Client Status",
        "points": [
            "Centralized timeline tracking client follow-up dates and contact information",
            "Summary statistics: Total scheduled, High Priority count, Site Visits, and Won Deals",
            "Status progression indicators: Pending, Scheduled, Active, and Won",
            "Cross-linked sidebar navigation for rapid module switching"
        ],
        "accent": "#00838f"
    },
    {
        "tag": "7. TECHNICAL IMPLEMENTATION",
        "title": "Modern Web Technologies",
        "subtitle": "Pure HTML5, CSS3, & JavaScript Architecture",
        "points": [
            "HTML5: Semantic layout (<header>, <nav>, <main>, <form>, <table>)",
            "CSS3: Custom Flexbox layout, keyframe entrance animations, interactive hover states",
            "JavaScript: Event delegation, DOM manipulation, JSON serialization",
            "LocalStorage API: Zero-backend persistence ensuring all data survives page refreshes"
        ],
        "accent": "#283593"
    },
    {
        "tag": "8. EVALUATION & OUTCOMES",
        "title": "Outcomes & Team Contributions",
        "subtitle": "Key Highlights for CA1 Submission",
        "points": [
            "Fully functional, bug-free web application ready for live deployment",
            "Source code maintained in Git version control with clean commit history",
            "Complete code PDF generated for official academic verification",
            "Submission Excel sheet prepared matching all UMS evaluation guidelines"
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

def render_slide(slide_idx, progress):
    slide = SLIDES[slide_idx]
    img = Image.new("RGB", (WIDTH, HEIGHT), "#f8f9fa")
    draw = ImageDraw.Draw(img)

    accent_color = slide["accent"]
    draw.rectangle([0, 0, WIDTH, 16], fill=accent_color)
    draw.rectangle([0, 0, 18, HEIGHT], fill=accent_color)

    font_tag = get_font(22, bold=True)
    font_title = get_font(52, bold=True)
    font_subtitle = get_font(28, bold=False)
    font_bullet = get_font(26, bold=False)
    font_footer = get_font(18, bold=False)

    draw.text((100, 60), slide["tag"], fill=accent_color, font=font_tag)
    draw.text((100, 100), slide["title"], fill="#020e21", font=font_title)
    draw.text((100, 175), slide["subtitle"], fill="#555555", font=font_subtitle)

    draw.line([(100, 225), (WIDTH - 100, 225)], fill="#e0e0e0", width=2)

    card_y = 265
    card_h = 680
    draw.rectangle([100, card_y, WIDTH - 100, card_y + card_h], fill="#ffffff", outline="#e0e0e0", width=2)
    draw.rectangle([100, card_y, 112, card_y + card_h], fill=accent_color)

    y = card_y + 60
    for pt in slide["points"]:
        draw.ellipse([145, y + 8, 160, y + 23], fill=accent_color)
        draw.text((185, y), pt, fill="#1f2937", font=font_bullet)
        y += 110

    footer_text = f"Slide {slide_idx + 1} of {len(SLIDES)} | EstateFlow Project Presentation | CSE326"
    draw.text((100, HEIGHT - 55), footer_text, fill="#888888", font=font_footer)

    total_progress = (slide_idx + progress) / len(SLIDES)
    bar_width = int(WIDTH * total_progress)
    draw.rectangle([0, HEIGHT - 8, bar_width, HEIGHT], fill=accent_color)

    return np.array(img)

def generate_video():
    output_filename = "EstateFlow_Project_Presentation.mp4"
    print(f"Generating presentation video: {output_filename}...")

    total_frames = len(SLIDES) * FRAMES_PER_SLIDE
    frames = []

    for s_idx in range(len(SLIDES)):
        for f in range(FRAMES_PER_SLIDE):
            prog = f / FRAMES_PER_SLIDE
            frame = render_slide(s_idx, prog)
            frames.append(frame)

    frames_arr = np.array(frames)
    iio.imwrite(output_filename, frames_arr, fps=FPS, codec="libx264")
    print(f"Successfully generated {output_filename} with {total_frames} frames ({len(SLIDES) * SECONDS_PER_SLIDE} seconds)!")

if __name__ == '__main__':
    generate_video()

# EstateFlow — Property Lead Management System

[![Live Demo](https://img.shields.io/badge/Live-Demo-blue?style=for-the-badge&logo=github)](https://sathish-08-x.github.io/Estate/)
[![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-black?style=for-the-badge&logo=github)](https://github.com/Sathish-08-x/Estate)
[![Course](https://img.shields.io/badge/Course-CSE326-brightgreen?style=for-the-badge)](https://github.com/Sathish-08-x/Estate)

> **CSE326 — Internet Programming | CA1 Project-Based Assessment**  
> **Institution:** Lovely Professional University (LPU)  
> **Team Name:** Boys-QH-T  
> **Team Leader:** Sathish Gudipudi (Reg No: 12613921)  
> **Team Members:** 12613921, 12614592, 12620884  

---

## 📌 Project Overview

**EstateFlow** is a client-side real estate lead management web application designed for property consultants, brokers, and agencies. Built using pure web standards (HTML5, CSS3, and modern JavaScript), EstateFlow streamlines prospect intake, deal progression, and client follow-ups with zero server dependencies by utilizing browser `localStorage` for state retention.

### 🎯 Problem Statement
Real estate agents handle prospective buyers and sellers across multiple channels, but frequently lose track of follow-up dates, budgets, property preferences, and negotiation history.

### 💡 Proposed Solution
A responsive, single-page application that:
- Centralizes lead capture and validation.
- Visualizes sales progression via a 4-stage Kanban pipeline.
- Provides an interactive lead directory with inline stage editing.
- Schedules follow-up calls and site visits ranked by priority.
- Persists all state across browser sessions locally.

---

## 🚀 Key Modules & Features

### 1. 📊 Interactive Dashboard (`index.html`)
- Four real-time metric cards: **Total Active Leads**, **Site Visits Scheduled**, **In Negotiation**, and **Closed Won Deals**.
- CSS hover-lift transitions and pulse animations.
- Dynamic lead intake form capturing: Client Name, Buyer/Seller toggle, Property Type (Apartment, House, Condo), Budget, Stage, Priority, and Follow-up Date.

### 2. 📋 All Leads Registry (`allleads.html`)
- Comprehensive tabular display of all registered property leads with budgets, phone numbers, and dates.
- **Inline Stage Management**: Update any lead's status via dropdown (*New*, *Site Visited Schedule*, *In Negotiation*, *Closed Won*).
- **Save Sync**: Clicking **Save** updates the stage text cell immediately and syncs state across all modules.

### 3. 🏷️ Kanban Sales Pipeline (`sales.html`)
- Multi-column visual board categorized into:
  - **New Leads**
  - **Contacted**
  - **In Negotiation**
  - **Closed Won**
- Priority-coded borders: **High** (Red), **Medium** (Orange), and **Low** (Green).
- Automatic card migration when stages are updated in the directory.
- Informative empty-state placeholders when stages have no active deals.

### 4. 📅 Follow-up Schedule (`followup.html`)
- Systematic task tracker ranking appointments and calls by date and priority.
- Live summary counters for total scheduled, high priority, site visits, and won deals.
- Status indicator tags: *Pending*, *Scheduled*, *Active*, and *Won*.

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| **HTML5** | Semantic structure (`<header>`, `<nav>`, `<main>`, `<form>`, `<table>`) |
| **CSS3** | Responsive Flexbox layout, keyframe entrance animations, interactive hover states |
| **JavaScript (ES6+)** | Dynamic DOM manipulation, event delegation, client-side validation |
| **LocalStorage API** | Persistent client-side data engine retaining lead states across reloads |

---

## 📂 Project Structure

```text
CSE326-CA1/
├── index.html                    # Dashboard & New Lead Ingestion Form
├── allleads.html                 # All Leads Registry & Inline Stage Management
├── sales.html                    # Kanban Sales Pipeline Multi-Stage Board
├── followup.html                 # Follow-up Schedule & Priority Tracker
├── style.css                     # Complete Application Stylesheet
├── script.js                     # Core Application Logic & LocalStorage Engine
├── logo.png                      # Application Brand Logo
├── EstateFlow_Presentation.mp4   # 4-Minute HD Project Presentation Video with Voice
├── README.md                     # Repository Documentation
└── .gitignore                    # Git Ignore Configuration
```

---

## 💻 How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Sathish-08-x/Estate.git
   cd Estate
   ```

2. **Open in any modern web browser:**
   - Double-click `index.html` or open it with Live Server in VS Code.
   - No npm, backend servers, or external database setups required.

---

## 🌐 Live Deployment

The project is hosted live via GitHub Pages:  
👉 **[https://sathish-08-x.github.io/Estate/](https://sathish-08-x.github.io/Estate/)**

---

## 🎥 Video Presentation

A comprehensive 4-minute Full HD walkthrough with natural voice narration covering the problem statement, system architecture, live module demonstrations, and technical implementation:  
👉 **[`EstateFlow_Presentation.mp4`](https://github.com/Sathish-08-x/Estate/blob/main/EstateFlow_Presentation.mp4)**

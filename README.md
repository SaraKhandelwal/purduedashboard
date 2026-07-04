# 🏛️ Purdue University Publishing Intelligence Dashboard

> **Executive-grade analytics dashboard for Purdue University's academic publishing portfolio.**
> Built to support data-driven decisions by university leadership, library administrators, and research strategy teams.

---

## 📌 Overview

This dashboard delivers an analytical experience for exploring Purdue University's publishing landscape — from a university-wide view down to the Agriculture sub-portfolio. It combines Scopus and OpenAlex data sources to provide cross-validated insights into publisher concentration, citation impact, and portfolio composition.

**The tool answers questions like:**
- Which publishers dominate Purdue's research output?
- What share does Agriculture contribute to the total portfolio?
- How concentrated is Purdue's publishing dependency on top commercial publishers?
- Which publications generate the highest citation impact?
- How do Scopus and OpenAlex differ in their coverage of Purdue research?

---

## 🎯 Features

### 1. Executive Summary
- High-level KPI cards: total publications, Ag share, peak citation impact, database coverage gap
- Strategic insight narratives generated from data
- Overview charts suitable for C-suite briefings

### 2. Purdue Publishers Overview
- Ranked bar charts for top N publishers (adjustable via sidebar)
- Cumulative concentration curve (Pareto analysis)
- Top cited publications with citation counts
- Source toggle: Scopus, OpenAlex, or Combined

### 3. Agriculture Deep Dive
- Ag-specific publisher rankings
- Portfolio treemap and output-tier segmentation
- Ag-exclusive vs shared publisher analysis
- Capture rate table showing Ag's share within each publisher

### 4. Comparative Analytics
- Side-by-side Purdue vs Agriculture publisher rankings
- Database coverage comparison (Scopus vs OpenAlex)
- Shared publisher overlap chart
- Agriculture capture rate by publisher
- Full summary comparison table

---

## 🛠️ Tech Stack

| Component | Library |
|-----------|---------|
| Framework | Streamlit |
| Data Processing | Pandas, NumPy |
| Visualizations | Plotly (Express + Graph Objects) |
| Data Source | Excel (openpyxl) |

---

## 📁 Repository Structure

```
purdue-dashboard/
├── app.py                    # Main Streamlit application
├── Dashboard.xlsx            # Source data (Purdue University + Agriculture sheets)
├── requirements.txt          # Python dependencies
├── README.md                 # This file
└── .streamlit/
    └── config.toml           # Theme & server configuration
```

---

## 🚀 Deployment Guide

### Option A — Streamlit Community Cloud (Recommended, Free)

#### Step 1: Create a GitHub Repository
1. Go to [github.com](https://github.com) and sign in (or create a free account)
2. Click **"New repository"** (green button, top right)
3. Name it: `purdue-publishing-dashboard`
4. Set visibility to **Public** (required for free Streamlit Cloud)
5. Click **"Create repository"**

#### Step 2: Upload Your Files
**Option A — GitHub Web UI (easiest):**
1. In your new repo, click **"Add file" → "Upload files"**
2. Drag and drop these files:
   - `app.py`
   - `Dashboard.xlsx`
   - `requirements.txt`
   - `README.md`
3. Click **"Commit changes"**
4. For the `.streamlit/config.toml`:
   - Click **"Add file" → "Create new file"**
   - In the filename box, type: `.streamlit/config.toml`
   - Paste the contents of `config.toml`
   - Click **"Commit changes"**

**Option B — Git CLI:**
```bash
git clone https://github.com/YOUR_USERNAME/purdue-publishing-dashboard.git
cd purdue-publishing-dashboard
# Copy all files here
git add .
git commit -m "Initial dashboard deployment"
git push origin main
```

#### Step 3: Deploy on Streamlit Community Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click **"New app"**
4. Fill in:
   - **Repository**: `YOUR_USERNAME/purdue-publishing-dashboard`
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. Click **"Deploy!"**
6. Wait ~2 minutes for the build to complete
7. Your app will be live at: `https://YOUR_USERNAME-purdue-publishing-dashboard-app-XXXXX.streamlit.app`

---

### Option B — Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/purdue-publishing-dashboard.git
cd purdue-publishing-dashboard

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```
Open your browser to `http://localhost:8501`

---

## 🔄 Updating the App

### If data changes:
1. Replace `Dashboard.xlsx` in your repo with the updated file
2. Commit and push:
   ```bash
   git add Dashboard.xlsx
   git commit -m "Update data: [date]"
   git push origin main
   ```
3. Streamlit Cloud will automatically redeploy within ~1 minute

### If code changes:
1. Edit `app.py` locally
2. Push changes:
   ```bash
   git add app.py
   git commit -m "feat: [description of change]"
   git push origin main
   ```

---

## 📊 Data Sources

| Sheet | Description |
|-------|-------------|
| `Purdue University` | Publication counts by publisher (Scopus + OpenAlex), top cited publications |
| `Purdue Agriculture` | Agriculture sub-portfolio publisher counts (Scopus + OpenAlex) |

---

## 👤 Author
Sara Khandelwal
---

## 📄 License

For internal/educational use. Data sourced from Scopus and OpenAlex under institutional access.

# ProtonIQ — Business Intelligence System
### Built by MA TechHub for Proton Bakers (Pvt) Ltd

> *"The Best of The Best" — Since 1961*

---

## 📁 Project Structure

```
protoniq/
├── app.py                    ← Main Dash application (entry point)
├── requirements.txt          ← Python dependencies
├── Procfile                  ← Gunicorn production server config
├── runtime.txt               ← Python version pin (3.11.9)
│
├── data/
│   ├── __init__.py
│   └── datasets.py           ← All simulated data + KPI calculations
│
├── assets/
│   ├── __init__.py
│   ├── custom.css            ← Proton brand dark theme (forest green + gold)
│   └── theme.py              ← Plotly chart brand colours & layout helpers
│
└── modules/
    ├── __init__.py
    ├── executive.py          ← Module 1: CEO Command Centre
    ├── production.py         ← Module 2: Production Output Tracker
    ├── depot.py              ← Module 3: Depot Intelligence
    ├── retailer.py           ← Module 4: Retailer Performance
    ├── sku.py                ← Module 5: SKU Intelligence
    └── fleet.py              ← Module 6: Fleet Performance
```

---

## 🚀 Local Development

### Prerequisites
- Python 3.11+
- pip

### Setup

```bash
# 1. Clone or extract the project
cd protoniq

# 2. Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # macOS / Linux
# venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python app.py
```

Visit: **http://localhost:8050**

---

## 🌐 Deploy to Render (Free Tier)

### Step 1 — Push to GitHub

```bash
# In the protoniq/ folder:
git init
git add .
git commit -m "ProtonIQ MVP — MA TechHub"

# Create a new repo on github.com (e.g. protoniq)
git remote add origin https://github.com/YOUR_USERNAME/protoniq.git
git branch -M main
git push -u origin main
```

### Step 2 — Create Render Web Service

1. Go to **https://render.com** → Sign up / Log in
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub account → Select **protoniq** repo
4. Fill in settings:

| Setting | Value |
|---|---|
| **Name** | `protoniq` |
| **Region** | Frankfurt (EU) or nearest |
| **Branch** | `main` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:server --workers 2 --timeout 120 --bind 0.0.0.0:$PORT` |
| **Plan** | Free |

5. Click **"Create Web Service"**
6. Render will build and deploy automatically (3–5 minutes)
7. Your live URL: `https://protoniq.onrender.com` (or similar)

### Step 3 — Environment Variables (optional)

No environment variables required for the MVP demo.

For production with live data, you would add:
```
DATABASE_URL=your_postgres_url
SECRET_KEY=your_secret_key
```

---

## 📊 Dashboard Modules (MVP — 6 of 17)

| # | Module | Description |
|---|---|---|
| 1 | 🏆 Executive Command Centre | CEO-level KPIs, revenue, gauges, partner breakdown |
| 2 | 🏭 Production Output Tracker | Daily/monthly volumes, treemap, margin by category |
| 3 | 📦 Depot Intelligence | Fill rates, dispatch throughput, waste across 3 depots |
| 4 | 🏪 Retailer Performance | Revenue ranking, OTD scatter, heatmap across 12 partners |
| 5 | 📋 SKU Intelligence | Product matrix, margin bars, top-5 trends |
| 6 | 🚛 Fleet Performance | Vehicle OTD, fuel efficiency, KM trends, maintenance alerts |

### Full 17-Module ProtonIQ Roadmap (Post-Contract)

```
Phase 2 modules (build on contract):
7.  Energy & Water IQ           — 96,000L daily water tracking (74% production)
8.  Raw Materials Intelligence  — Flour, yeast, sugar inventory & cost
9.  Workforce Analytics         — 1,700+ staff shift, output, absenteeism
10. Quality Control IQ          — Batch reject rates, rework, standards
11. Supplier Performance        — Lead times, cost variance, delivery quality
12. Customer Returns Tracker    — SKU-level return root causes
13. Regional Expansion Scout    — Zambia & Mozambique opportunity maps
14. Financial P&L Command       — Revenue, COGS, EBITDA by segment
15. Demand Forecasting          — 30/60/90-day production planning
16. Compliance & Audit Trail    — HACCP, food safety, certifications
17. Marketing Campaign ROI      — Superbrand, EPL Promo, ambassador returns
```

---

## 🎨 Brand & Design

- **Primary colour**: Forest Green `#1A6B35` (Proton brand green)
- **Accent**: Wheat Gold `#D4A017` (warmth of baked goods)
- **Background**: Deep Forest `#0D2818` (dark professional theme)
- **Typography**: DM Sans (body) + DM Serif Display (headings)
- **Charts**: Custom Plotly template with Proton colour sequence

---

## 🔄 Replacing Demo Data with Live Data

All data lives in `data/datasets.py`. Each function returns a `pd.DataFrame`.

To connect to real data:
1. Replace the `get_*` functions with database queries (PostgreSQL, MySQL, etc.)
2. Or connect to Proton's existing ERP/POS/fleet management systems via API
3. Add a caching layer (`diskcache` or Redis) for performance

---

## 📞 Built by MA TechHub

**Anesu Manjengwa** — Founder, MA TechHub  
Data Analytics & Dashboard Consultancy  
📧 Contact via LinkedIn / GitHub  
🌐 Portfolio: anesu-manjengwa.vercel.app

---

*ProtonIQ is a pitch demonstration system built with simulated data for the purposes of client acquisition. All production figures, revenue values, and operational metrics are realistic estimates based on publicly available Proton Bakers information.*

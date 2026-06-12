# 🛒 RetailIQ — AI-Powered E-commerce Intelligence System

![Power BI](https://img.shields.io/badge/Power%20BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-4479A1?style=for-the-badge&logo=sqlite&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)

> A full end-to-end Business Intelligence project analyzing 800K+ e-commerce transactions using Python, SQL, and Power BI to deliver £870K+ in actionable revenue recovery insights.

---

## 📊 Project Overview

RetailIQ is an AI-powered e-commerce intelligence system built on the **Online Retail II dataset (UCI)** — a real UK-based online retail store with transactions across 41 countries from December 2009 to December 2011.

### What makes this different from a basic dashboard?
- ✅ **RFM Customer Segmentation** — classified 5,878 customers into 6 business segments
- ✅ **Anomaly Detection** — IQR-based system flagging 29 unusual trading days automatically
- ✅ **AI-Generated Executive Report** — business recommendations, not just charts
- ✅ **Full Stack** — Python → SQL → Power BI → Word Report

---

## 🔍 Key Findings

| Metric | Value |
|--------|-------|
| Total Revenue | £17,743,429 |
| Total Orders | 36,969 |
| Unique Customers | 5,878 |
| Unique Products | 4,631 |
| Countries | 41 |
| Avg Order Value | £479.95 |
| Anomaly Days Detected | 29 |

### 🏆 The 13% Rule
> 774 Champion customers (just 13% of the base) generate **£9.8M — 55% of total revenue**

### 💰 Revenue Recovery Opportunity
> **£870,000+** addressable through targeted retention of At Risk and Lost customers

---

## 👥 Customer Segments (RFM Analysis)

| Segment | Customers | Avg Spend | Total Revenue |
|---------|-----------|-----------|---------------|
| 🏆 Champion | 774 | £12,686 | £9,818,881 |
| 💛 Loyal | 1,285 | £2,955 | £3,797,587 |
| ⚠️ At Risk | 1,466 | £1,576 | £2,310,503 |
| 🌱 Potential Loyalist | 894 | £861 | £769,953 |
| 😴 Cant Lose Them | 226 | £2,011 | £454,415 |
| ❌ Lost | 1,233 | £480 | £592,091 |

---

## 📁 Project Structure

```
RetailIQ/
├── Data/
│   ├── Raw/                          ← Original dataset
│   └── Cleaned/                      ← Processed CSV files
│       ├── retail_cleaned.csv        ← Main cleaned dataset
│       ├── rfm_segments.csv          ← RFM customer segments
│       ├── pbi_monthly.csv           ← Monthly revenue data
│       ├── pbi_top_products.csv      ← Top products
│       ├── pbi_by_country.csv        ← Country revenue
│       ├── pbi_rfm.csv               ← RFM for Power BI
│       ├── pbi_daily_anomaly.csv     ← Anomaly detection data
│       └── pbi_kpis.csv              ← KPI summary
├── notebooks/
│   ├── day1_clean_data.py            ← Data cleaning & feature engineering
│   ├── day2_rfm_analysis.py          ← RFM segmentation + SQL analysis
│   ├── day3_anomaly_visuals.py       ← Anomaly detection + charts
│   └── day4_prepare_powerbi.py       ← Power BI data preparation
├── sql/
│   └── analysis_queries.sql          ← 8 SQL business queries
├── visuals/
│   ├── 01_monthly_revenue.png        ← Revenue trend chart
│   ├── 02_customer_segments.png      ← Segmentation donut
│   ├── 03_top_products.png           ← Top products bar chart
│   ├── 04_revenue_by_country.png     ← Country revenue
│   ├── 05_anomaly_detection.png      ← Anomaly detection chart
│   └── 06_revenue_by_segment.png     ← Revenue by segment
├── powerbi/
│   └── RetailIQ_Dashboard.pbix       ← 3-page Power BI dashboard
└── reports/
    └── RetailIQ_Executive_Report.docx ← AI-generated business report
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python (pandas) | Data cleaning, feature engineering |
| Python (matplotlib, seaborn) | Data visualization |
| SQL (SQLite) | Business queries & analysis |
| Power BI | Interactive 3-page dashboard |
| IQR Method | Anomaly detection |
| RFM Analysis | Customer segmentation |

---

## 🚀 How to Run

### Step 1 — Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/RetailIQ.git
cd RetailIQ
```

### Step 2 — Install dependencies
```bash
pip install pandas openpyxl matplotlib seaborn scikit-learn
```

### Step 3 — Download dataset
- Go to: https://www.kaggle.com/datasets/mashlyn/online-retail-ii-uci
- Download `online_retail_II.csv`
- Place in `Data/Raw/`

### Step 4 — Run scripts in order
```bash
python notebooks/day1_clean_data.py
python notebooks/day2_rfm_analysis.py
python notebooks/day3_anomaly_visuals.py
python notebooks/day4_prepare_powerbi.py
```

### Step 5 — Open Power BI dashboard
- Open `powerbi/RetailIQ_Dashboard.pbix` in Power BI Desktop

---

## 📈 Dashboard Pages

| Page | Description |
|------|-------------|
| Executive Overview | KPI cards, monthly trend, top products, revenue by country |
| Customer Segmentation | RFM donut chart, segment revenue, customer table |
| Anomaly & Products | Daily revenue anomaly detection, product performance |

---

## 💡 Business Recommendations

1. **Protect Champions** — Launch VIP programme for 774 Champion customers driving 55% revenue
2. **Win back At Risk** — Immediate re-engagement campaign for 1,466 at-risk customers (£693K opportunity)
3. **Expand internationally** — Germany & France show high revenue per customer
4. **Q4 planning** — Revenue peaks 94% in Nov — plan inventory and marketing ahead

---

## 👤 Author

**Sri Sai Samarth Sistla**
- 🎓 BBA Graduate
- 📍 New Delhi, India
- 🔗 [LinkedIn](https://www.linkedin.com/in/sri-sai-samarth-sistla-532657258)

---

*Built as a Business Analyst portfolio project using Python, SQL, and Power BI.*

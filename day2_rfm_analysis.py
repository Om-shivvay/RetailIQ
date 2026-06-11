"""
RetailIQ — Day 2: RFM Customer Segmentation + SQL Analysis
"""

import pandas as pd
import numpy as np
import sqlite3
import os

# ── Paths ─────────────────────────────────────────────────────────────────────
CLEANED_PATH = "Data/Cleaned/retail_cleaned.csv"
RFM_PATH     = "Data/Cleaned/rfm_segments.csv"
SQL_DB       = "Data/Cleaned/retailiq.db"

# ── 1. Load cleaned data ──────────────────────────────────────────────────────
print("📦 Loading cleaned data...")
df = pd.read_csv(CLEANED_PATH)
df["invoice_date"] = pd.to_datetime(df["invoice_date"])
print(f"   Loaded {len(df):,} rows")

# ── 2. Load into SQLite for SQL analysis ──────────────────────────────────────
print("\n🗄️  Loading data into SQL database...")
conn = sqlite3.connect(SQL_DB)
df.to_sql("retail", conn, if_exists="replace", index=False)
print("   Done! Running SQL queries...\n")

# ── SQL Query 1: Monthly Revenue ──────────────────────────────────────────────
q1 = """
    SELECT 
        strftime('%Y-%m', invoice_date) AS month,
        ROUND(SUM(revenue), 2)          AS total_revenue,
        COUNT(DISTINCT invoice_id)      AS total_orders,
        COUNT(DISTINCT customer_id)     AS unique_customers
    FROM retail
    GROUP BY month
    ORDER BY month
"""
monthly = pd.read_sql(q1, conn)
print("📅 Monthly Revenue (last 6 months):")
print(monthly.tail(6).to_string(index=False))

# ── SQL Query 2: Top 10 Products ──────────────────────────────────────────────
q2 = """
    SELECT 
        product_name,
        SUM(quantity)          AS total_units_sold,
        ROUND(SUM(revenue), 2) AS total_revenue
    FROM retail
    GROUP BY product_name
    ORDER BY total_revenue DESC
    LIMIT 10
"""
top_products = pd.read_sql(q2, conn)
print("\n🏆 Top 10 Products by Revenue:")
print(top_products.to_string(index=False))

# ── SQL Query 3: Revenue by Country ───────────────────────────────────────────
q3 = """
    SELECT 
        country,
        ROUND(SUM(revenue), 2)     AS total_revenue,
        COUNT(DISTINCT customer_id) AS customers
    FROM retail
    GROUP BY country
    ORDER BY total_revenue DESC
    LIMIT 10
"""
by_country = pd.read_sql(q3, conn)
print("\n🌍 Top 10 Countries by Revenue:")
print(by_country.to_string(index=False))

# ── 3. RFM Analysis ───────────────────────────────────────────────────────────
print("\n👥 Calculating RFM scores...")

# Reference date = 1 day after last invoice
reference_date = df["invoice_date"].max() + pd.Timedelta(days=1)

rfm = df.groupby("customer_id").agg(
    recency   = ("invoice_date", lambda x: (reference_date - x.max()).days),
    frequency = ("invoice_id",   "nunique"),
    monetary  = ("revenue",      "sum")
).reset_index()

# Score each metric 1-4 (4 = best)
rfm["r_score"] = pd.qcut(rfm["recency"],   4, labels=[4, 3, 2, 1])
rfm["f_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 4, labels=[1, 2, 3, 4])
rfm["m_score"] = pd.qcut(rfm["monetary"],  4, labels=[1, 2, 3, 4])

rfm["rfm_score"] = (
    rfm["r_score"].astype(int) +
    rfm["f_score"].astype(int) +
    rfm["m_score"].astype(int)
)

# ── 4. Segment customers ──────────────────────────────────────────────────────
def segment(row):
    r, f, m = int(row["r_score"]), int(row["f_score"]), int(row["m_score"])
    if r >= 4 and f >= 4:
        return "🏆 Champion"
    elif r >= 3 and f >= 3:
        return "💛 Loyal"
    elif r >= 3 and f <= 2:
        return "🌱 Potential Loyalist"
    elif r == 2:
        return "⚠️ At Risk"
    elif r == 1 and f >= 3:
        return "😴 Cant Lose Them"
    else:
        return "❌ Lost"

rfm["segment"] = rfm.apply(segment, axis=1)

# ── 5. Segment summary ────────────────────────────────────────────────────────
print("\n📊 Customer Segment Summary:")
summary = rfm.groupby("segment").agg(
    customers       = ("customer_id", "count"),
    avg_recency     = ("recency",     "mean"),
    avg_frequency   = ("frequency",   "mean"),
    avg_monetary    = ("monetary",    "mean"),
    total_revenue   = ("monetary",    "sum")
).round(2).reset_index()
summary = summary.sort_values("total_revenue", ascending=False)
print(summary.to_string(index=False))

# ── 6. Save RFM results ───────────────────────────────────────────────────────
rfm.to_csv(RFM_PATH, index=False)
rfm.to_sql("rfm_segments", conn, if_exists="replace", index=False)
conn.close()

print(f"\n💾 RFM segments saved → {RFM_PATH}")
print("\n🎉 Day 2 complete! Your customer segments are ready.")
print("   Next: Run day3_anomaly_visuals.py")

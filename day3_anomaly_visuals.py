"""
RetailIQ — Day 3: Anomaly Detection + Python Visualizations
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import os

# ── Setup ─────────────────────────────────────────────────────────────────────
CLEANED_PATH = "Data/Cleaned/retail_cleaned.csv"
RFM_PATH     = "Data/Cleaned/rfm_segments.csv"
VISUALS_DIR  = "visuals"
os.makedirs(VISUALS_DIR, exist_ok=True)

plt.style.use("seaborn-v0_8-whitegrid")
COLORS = ["#2D6A4F", "#40916C", "#52B788", "#74C69D", "#95D5B2", "#B7E4C7"]

print("📦 Loading data...")
df  = pd.read_csv(CLEANED_PATH)
rfm = pd.read_csv(RFM_PATH)
df["invoice_date"] = pd.to_datetime(df["invoice_date"])
print(f"   Loaded {len(df):,} rows\n")

# ── Chart 1: Monthly Revenue Trend ───────────────────────────────────────────
print("📊 Chart 1: Monthly Revenue Trend...")
monthly = df.groupby(df["invoice_date"].dt.to_period("M"))["revenue"].sum().reset_index()
monthly["invoice_date"] = monthly["invoice_date"].astype(str)

fig, ax = plt.subplots(figsize=(14, 5))
ax.fill_between(monthly["invoice_date"], monthly["revenue"], alpha=0.3, color="#40916C")
ax.plot(monthly["invoice_date"], monthly["revenue"], color="#2D6A4F", linewidth=2.5, marker="o", markersize=4)
ax.set_title("Monthly Revenue Trend — RetailIQ", fontsize=16, fontweight="bold", pad=15)
ax.set_xlabel("Month", fontsize=12)
ax.set_ylabel("Revenue (£)", fontsize=12)
plt.xticks(rotation=45, ha="right", fontsize=9)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"£{x:,.0f}"))
plt.tight_layout()
plt.savefig(f"{VISUALS_DIR}/01_monthly_revenue.png", dpi=150)
plt.close()
print("   Saved 01_monthly_revenue.png")

# ── Chart 2: Customer Segments Donut ─────────────────────────────────────────
print("📊 Chart 2: Customer Segments...")
seg_counts = rfm["segment"].value_counts()
seg_colors = ["#2D6A4F","#40916C","#52B788","#F4A261","#E76F51","#264653"]

fig, ax = plt.subplots(figsize=(9, 7))
wedges, texts, autotexts = ax.pie(
    seg_counts, labels=seg_counts.index, autopct="%1.1f%%",
    colors=seg_colors[:len(seg_counts)], startangle=140,
    wedgeprops=dict(width=0.55), pctdistance=0.75
)
for t in texts:     t.set_fontsize(11)
for t in autotexts: t.set_fontsize(9); t.set_fontweight("bold")
ax.set_title("Customer Segmentation — RFM Analysis", fontsize=15, fontweight="bold", pad=20)
plt.tight_layout()
plt.savefig(f"{VISUALS_DIR}/02_customer_segments.png", dpi=150)
plt.close()
print("   Saved 02_customer_segments.png")

# ── Chart 3: Top 10 Products ──────────────────────────────────────────────────
print("📊 Chart 3: Top 10 Products...")
top_products = (
    df.groupby("product_name")["revenue"]
    .sum().sort_values(ascending=False).head(10)
)

fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.barh(top_products.index[::-1], top_products.values[::-1], color=COLORS * 2)
ax.set_title("Top 10 Products by Revenue", fontsize=15, fontweight="bold", pad=15)
ax.set_xlabel("Revenue (£)", fontsize=12)
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"£{x:,.0f}"))
for bar, val in zip(bars, top_products.values[::-1]):
    ax.text(bar.get_width() + 1000, bar.get_y() + bar.get_height()/2,
            f"£{val:,.0f}", va="center", fontsize=9)
plt.tight_layout()
plt.savefig(f"{VISUALS_DIR}/03_top_products.png", dpi=150)
plt.close()
print("   Saved 03_top_products.png")

# ── Chart 4: Revenue by Country ───────────────────────────────────────────────
print("📊 Chart 4: Revenue by Country...")
by_country = (
    df.groupby("country")["revenue"]
    .sum().sort_values(ascending=False).head(10)
)

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(by_country.index, by_country.values, color=COLORS * 2)
ax.set_title("Top 10 Countries by Revenue", fontsize=15, fontweight="bold", pad=15)
ax.set_ylabel("Revenue (£)", fontsize=12)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"£{x:,.0f}"))
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig(f"{VISUALS_DIR}/04_revenue_by_country.png", dpi=150)
plt.close()
print("   Saved 04_revenue_by_country.png")

# ── Chart 5: Anomaly Detection ────────────────────────────────────────────────
print("📊 Chart 5: Anomaly Detection...")
daily = df.groupby(df["invoice_date"].dt.date)["revenue"].sum().reset_index()
daily.columns = ["date", "revenue"]

Q1, Q3 = daily["revenue"].quantile(0.25), daily["revenue"].quantile(0.75)
IQR     = Q3 - Q1
upper   = Q3 + 1.5 * IQR
lower   = Q1 - 1.5 * IQR

daily["anomaly"] = (daily["revenue"] > upper) | (daily["revenue"] < lower)
anomalies = daily[daily["anomaly"]]
print(f"   🚨 Detected {len(anomalies)} anomaly days!")

fig, ax = plt.subplots(figsize=(14, 5))
ax.plot(daily["date"], daily["revenue"], color="#40916C", linewidth=1.2, alpha=0.8, label="Daily Revenue")
ax.axhline(upper, color="#E76F51", linestyle="--", linewidth=1.5, label=f"Upper bound £{upper:,.0f}")
ax.axhline(lower, color="#457B9D", linestyle="--", linewidth=1.5, label=f"Lower bound £{lower:,.0f}")
ax.scatter(anomalies["date"], anomalies["revenue"], color="#E63946", s=60, zorder=5, label=f"Anomalies ({len(anomalies)})")
ax.set_title("Daily Revenue — Anomaly Detection (IQR Method)", fontsize=15, fontweight="bold", pad=15)
ax.set_xlabel("Date", fontsize=12)
ax.set_ylabel("Revenue (£)", fontsize=12)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"£{x:,.0f}"))
ax.legend(fontsize=10)
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig(f"{VISUALS_DIR}/05_anomaly_detection.png", dpi=150)
plt.close()
print("   Saved 05_anomaly_detection.png")

# ── Chart 6: RFM Segment Revenue ─────────────────────────────────────────────
print("📊 Chart 6: Revenue by Segment...")
seg_rev = rfm.groupby("segment")["monetary"].sum().sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.bar(seg_rev.index, seg_rev.values, color=seg_colors[:len(seg_rev)])
ax.set_title("Total Revenue by Customer Segment", fontsize=15, fontweight="bold", pad=15)
ax.set_ylabel("Revenue (£)", fontsize=12)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"£{x:,.0f}"))
for bar, val in zip(bars, seg_rev.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50000,
            f"£{val:,.0f}", ha="center", fontsize=9, fontweight="bold")
plt.xticks(rotation=20, ha="right")
plt.tight_layout()
plt.savefig(f"{VISUALS_DIR}/06_revenue_by_segment.png", dpi=150)
plt.close()
print("   Saved 06_revenue_by_segment.png")

print("\n✅ All 6 charts saved to visuals/ folder!")
print(f"   Anomaly days detected: {len(anomalies)}")
print("\n🎉 Day 3 complete! Open your visuals/ folder to see the charts.")
print("   Next: Build your Power BI dashboard (Days 4-5)")

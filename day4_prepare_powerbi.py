"""
RetailIQ — Day 4: Prepare all data files for Power BI
"""

import pandas as pd
import numpy as np
import os

CLEANED_PATH = "Data/Cleaned/retail_cleaned.csv"
RFM_PATH     = "Data/Cleaned/rfm_segments.csv"
OUT          = "Data/Cleaned"

print("📦 Loading data...")
df  = pd.read_csv(CLEANED_PATH)
rfm = pd.read_csv(RFM_PATH)
df["invoice_date"] = pd.to_datetime(df["invoice_date"])

# ── 1. Monthly Summary ────────────────────────────────────────────────────────
monthly = df.groupby(df["invoice_date"].dt.to_period("M")).agg(
    total_revenue    = ("revenue",     "sum"),
    total_orders     = ("invoice_id",  "nunique"),
    unique_customers = ("customer_id", "nunique"),
    total_items      = ("quantity",    "sum")
).reset_index()
monthly["invoice_date"] = monthly["invoice_date"].astype(str)
monthly.to_csv(f"{OUT}/pbi_monthly.csv", index=False)
print("✅ Saved pbi_monthly.csv")

# ── 2. Top Products ───────────────────────────────────────────────────────────
top_products = df.groupby("product_name").agg(
    total_revenue    = ("revenue",  "sum"),
    total_units_sold = ("quantity", "sum"),
    total_orders     = ("invoice_id","nunique")
).reset_index().sort_values("total_revenue", ascending=False).head(20)
top_products.to_csv(f"{OUT}/pbi_top_products.csv", index=False)
print("✅ Saved pbi_top_products.csv")

# ── 3. Country Summary ────────────────────────────────────────────────────────
by_country = df.groupby("country").agg(
    total_revenue    = ("revenue",     "sum"),
    total_orders     = ("invoice_id",  "nunique"),
    unique_customers = ("customer_id", "nunique")
).reset_index().sort_values("total_revenue", ascending=False)
by_country.to_csv(f"{OUT}/pbi_by_country.csv", index=False)
print("✅ Saved pbi_by_country.csv")

# ── 4. RFM Segments clean ────────────────────────────────────────────────────
rfm_clean = rfm[["customer_id","recency","frequency","monetary","segment"]].copy()
rfm_clean["segment"] = rfm_clean["segment"].str.replace(r"[^\w\s]","",regex=True).str.strip()
rfm_clean.to_csv(f"{OUT}/pbi_rfm.csv", index=False)
print("✅ Saved pbi_rfm.csv")

# ── 5. Daily Revenue (for anomaly chart) ─────────────────────────────────────
daily = df.groupby(df["invoice_date"].dt.date)["revenue"].sum().reset_index()
daily.columns = ["date","revenue"]
Q1, Q3 = daily["revenue"].quantile(0.25), daily["revenue"].quantile(0.75)
IQR    = Q3 - Q1
daily["is_anomaly"]   = ((daily["revenue"] > Q3 + 1.5*IQR) | (daily["revenue"] < Q1 - 1.5*IQR)).astype(int)
daily["upper_bound"]  = round(Q3 + 1.5*IQR, 2)
daily["lower_bound"]  = max(round(Q1 - 1.5*IQR, 2), 0)
daily.to_csv(f"{OUT}/pbi_daily_anomaly.csv", index=False)
print("✅ Saved pbi_daily_anomaly.csv")

# ── 6. KPI Summary ───────────────────────────────────────────────────────────
kpis = {
    "total_revenue":     round(df["revenue"].sum(), 2),
    "total_orders":      df["invoice_id"].nunique(),
    "total_customers":   df["customer_id"].nunique(),
    "total_products":    df["stock_code"].nunique(),
    "total_countries":   df["country"].nunique(),
    "avg_order_value":   round(df.groupby("invoice_id")["revenue"].sum().mean(), 2),
    "champion_customers":len(rfm[rfm["segment"].str.contains("Champion")]),
    "at_risk_customers": len(rfm[rfm["segment"].str.contains("At Risk")]),
    "anomaly_days":      int(daily["is_anomaly"].sum()),
}
pd.DataFrame([kpis]).to_csv(f"{OUT}/pbi_kpis.csv", index=False)
print("✅ Saved pbi_kpis.csv")

print("\n📊 KPI Summary:")
for k, v in kpis.items():
    print(f"   {k:25s}: {v:,}")

print("\n🎉 All Power BI data files ready in Data/Cleaned/")
print("   Files to import into Power BI:")
print("   • pbi_monthly.csv")
print("   • pbi_top_products.csv")
print("   • pbi_by_country.csv")
print("   • pbi_rfm.csv")
print("   • pbi_daily_anomaly.csv")
print("   • pbi_kpis.csv")

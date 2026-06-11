"""
RetailIQ — Day 1: Data Cleaning & Feature Engineering
Dataset: Online Retail II (UCI / Kaggle)
"""

import pandas as pd
import numpy as np 
import os

# ── Paths ────────────────────────────────────────────────────────────────────
RAW_PATH     = "Data/Raw/online_retail_II.csv"
CLEANED_PATH = "Data/Cleaned/retail_cleaned.csv"

# ── 1. Load ───────────────────────────────────────────────────────────────────
print("📦 Loading dataset...")
df = pd.read_csv(RAW_PATH, encoding="utf-8", low_memory=False)
print(f"   Raw shape: {df.shape[0]:,} rows × {df.shape[1]} columns")

# ── 2. Column standardisation ─────────────────────────────────────────────────
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

print(f"\n📋 Columns found: {list(df.columns)}")

# Rename to clean names (handles both xlsx and csv column name variants)
df = df.rename(columns={
    "invoice":      "invoice_id",
    "invoiceno":    "invoice_id",
    "stockcode":    "stock_code",
    "description":  "product_name",
    "quantity":     "quantity",
    "invoicedate":  "invoice_date",
    "price":        "unit_price",
    "unitprice":    "unit_price",
    "customer_id":  "customer_id",
    "customerid":   "customer_id",
    "country":      "country",
})

# ── 3. Drop nulls ─────────────────────────────────────────────────────────────
print(f"\n🔍 Nulls before cleaning:\n{df.isnull().sum()}")
before = len(df)
df = df.dropna(subset=["customer_id"])
df["product_name"] = df["product_name"].fillna("Unknown")
print(f"   Dropped {before - len(df):,} rows with no customer_id")

# ── 4. Remove returns & bad rows ──────────────────────────────────────────────
df = df[~df["invoice_id"].astype(str).str.startswith("C")]
df = df[df["quantity"]   > 0]
df = df[df["unit_price"] > 0]
print(f"   After removing returns/negatives: {len(df):,} rows")

# ── 5. Fix data types ─────────────────────────────────────────────────────────
df["invoice_date"] = pd.to_datetime(df["invoice_date"])
df["customer_id"]  = df["customer_id"].astype(float).astype(int).astype(str)
df["stock_code"]   = df["stock_code"].astype(str).str.strip()

# ── 6. Feature engineering ────────────────────────────────────────────────────
df["revenue"]       = df["quantity"] * df["unit_price"]
df["invoice_month"] = df["invoice_date"].dt.to_period("M")
df["invoice_year"]  = df["invoice_date"].dt.year
df["day_of_week"]   = df["invoice_date"].dt.day_name()
df["hour"]          = df["invoice_date"].dt.hour

print(f"\n✅ Feature engineering done!")

# ── 7. Quick summary ──────────────────────────────────────────────────────────
print("\n📊 Clean dataset summary:")
print(f"   Total transactions : {len(df):,}")
print(f"   Unique customers   : {df['customer_id'].nunique():,}")
print(f"   Unique products    : {df['stock_code'].nunique():,}")
print(f"   Countries          : {df['country'].nunique()}")
print(f"   Date range         : {df['invoice_date'].min().date()} → {df['invoice_date'].max().date()}")
print(f"   Total revenue      : £{df['revenue'].sum():,.2f}")
print(f"\n   Top 5 countries by revenue:")
print(df.groupby("country")["revenue"].sum().sort_values(ascending=False).head())

# ── 8. Save ───────────────────────────────────────────────────────────────────
os.makedirs("Data/Cleaned", exist_ok=True)
df.to_csv(CLEANED_PATH, index=False)
print(f"\n💾 Saved cleaned data → {CLEANED_PATH}")
print("   Day 1 complete! Run day2_rfm_analysis.py next. 🎉")

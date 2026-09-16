from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import pandas as pd

app = FastAPI(title="Business Sales Analytics API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "sales_data.csv"

def load_data():
    df = pd.read_csv(DATA).drop_duplicates().copy()
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
    for col in ["Product", "Category", "Region"]:
        df[col] = df[col].astype("string").str.strip().fillna("Unknown")
    for col in ["Quantity", "Unit Price", "Revenue", "Cost", "Profit"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["Quantity"] = df["Quantity"].fillna(0)
    df["Revenue"] = df["Revenue"].fillna(df["Quantity"] * df["Unit Price"])
    df["Cost"] = df["Cost"].fillna(df["Revenue"] - df["Profit"])
    df["Profit"] = df["Profit"].fillna(df["Revenue"] - df["Cost"])
    df["Month"] = df["Order Date"].dt.to_period("M").astype(str)
    return df

@app.get("/", response_class=HTMLResponse)
def home():
    return (ROOT / "index.html").read_text(encoding="utf-8")

@app.get("/api/filters")
def filters():
    df = load_data()
    return {
        "regions": sorted(df["Region"].unique().tolist()),
        "categories": sorted(df["Category"].unique().tolist()),
        "min_date": df["Order Date"].min().strftime("%Y-%m-%d"),
        "max_date": df["Order Date"].max().strftime("%Y-%m-%d")
    }

@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.get("/api/dashboard")
def dashboard(region: str = "", category: str = "", start_date: str = "", end_date: str = ""):
    df = load_data()
    if region:
        df = df[df["Region"] == region]
    if category:
        df = df[df["Category"] == category]
    if start_date:
        df = df[df["Order Date"] >= pd.to_datetime(start_date)]
    if end_date:
        df = df[df["Order Date"] <= pd.to_datetime(end_date)]

    transactions = df["Order ID"].nunique()
    revenue = df["Revenue"].sum()
    monthly = df.groupby("Month", as_index=False)[["Revenue", "Profit"]].sum()
    products = df.groupby("Product", as_index=False)[["Revenue", "Profit"]].sum().sort_values("Revenue", ascending=False).head(10)
    regions = df.groupby("Region", as_index=False)["Revenue"].sum().sort_values("Revenue", ascending=False)
    return {
        "kpis": {
            "revenue": round(revenue, 2),
            "profit": round(df["Profit"].sum(), 2),
            "transactions": int(transactions),
            "quantity": int(df["Quantity"].sum()),
            "aov": round(revenue / transactions, 2) if transactions else 0
        },
        "monthly": monthly.to_dict("records"),
        "products": products.to_dict("records"),
        "regions": regions.to_dict("records")
    }

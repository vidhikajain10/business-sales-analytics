from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI(title="Business Sales Analytics API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

DATA = "data/sales_data.csv"

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

@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.get("/api/dashboard")
def dashboard():
    df = load_data()
    monthly = df.groupby("Month", as_index=False)[["Revenue", "Profit"]].sum()
    products = df.groupby("Product", as_index=False)[["Revenue", "Profit"]].sum().sort_values("Revenue", ascending=False).head(10)
    regions = df.groupby("Region", as_index=False)["Revenue"].sum().sort_values("Revenue", ascending=False)
    transactions = df["Order ID"].nunique()
    revenue = df["Revenue"].sum()
    return {
        "kpis": {"revenue": round(revenue, 2), "profit": round(df["Profit"].sum(), 2), "transactions": int(transactions), "aov": round(revenue / transactions, 2)},
        "monthly": monthly.to_dict("records"),
        "products": products.to_dict("records"),
        "regions": regions.to_dict("records"),
    }

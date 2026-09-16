from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import pandas as pd

app = FastAPI(title="Business Sales Analytics API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "sales_data.csv"

ALIASES = {
    "order id":"Order ID", "order_id":"Order ID", "id":"Order ID",
    "order date":"Order Date", "date":"Order Date", "order_date":"Order Date",
    "product":"Product", "item":"Product", "product name":"Product",
    "category":"Category", "type":"Category", "region":"Region", "area":"Region",
    "quantity":"Quantity", "qty":"Quantity", "units":"Quantity",
    "unit price":"Unit Price", "price":"Unit Price", "unit_price":"Unit Price",
    "revenue":"Revenue", "sales":"Revenue", "sales amount":"Revenue",
    "cost":"Cost", "profit":"Profit", "profit amount":"Profit"
}


def clean_data(df):
    raw_rows = len(df)
    renamed = df.rename(columns=lambda x: ALIASES.get(str(x).strip().lower(), str(x).strip())).copy()
    before_duplicates = len(renamed)
    df = renamed.drop_duplicates().copy()
    duplicates_removed = before_duplicates - len(df)
    required = ["Order ID", "Order Date", "Product", "Quantity"]
    missing = [x for x in required if x not in df.columns]
    if missing:
        raise HTTPException(400, "Missing required columns: " + ", ".join(missing))
    for col in ["Product", "Category", "Region"]:
        if col not in df.columns:
            df[col] = "Unknown"
        df[col] = df[col].astype("string").str.strip().fillna("Unknown")
    for col in ["Quantity", "Unit Price", "Revenue", "Cost", "Profit"]:
        if col not in df.columns:
            df[col] = pd.NA
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
    invalid_dates = int(df["Order Date"].isna().sum())
    df = df.dropna(subset=["Order Date"])
    df["Quantity"] = df["Quantity"].fillna(0)
    df["Revenue"] = df["Revenue"].fillna(df["Quantity"] * df["Unit Price"])
    df["Cost"] = df["Cost"].fillna(df["Revenue"] - df["Profit"])
    df["Profit"] = df["Profit"].fillna(df["Revenue"] - df["Cost"])
    df[["Revenue", "Cost", "Profit"]] = df[["Revenue", "Cost", "Profit"]].fillna(0)
    df["Month"] = df["Order Date"].dt.to_period("M").astype(str)
    df.attrs["raw_rows"] = raw_rows
    df.attrs["duplicates_removed"] = duplicates_removed
    df.attrs["invalid_dates_removed"] = invalid_dates
    return df


def load_data():
    return clean_data(pd.read_csv(DATA))


def make_dashboard(df, region="", category="", start_date="", end_date=""):
    available_regions = sorted(df["Region"].unique().tolist())
    available_categories = sorted(df["Category"].unique().tolist())
    min_date = df["Order Date"].min().strftime("%Y-%m-%d") if len(df) else ""
    max_date = df["Order Date"].max().strftime("%Y-%m-%d") if len(df) else ""
    raw_rows = int(df.attrs.get("raw_rows", len(df)))
    duplicates_removed = int(df.attrs.get("duplicates_removed", 0))
    invalid_dates_removed = int(df.attrs.get("invalid_dates_removed", 0))
    if region: df = df[df["Region"] == region]
    if category: df = df[df["Category"] == category]
    if start_date: df = df[df["Order Date"] >= pd.to_datetime(start_date)]
    if end_date: df = df[df["Order Date"] <= pd.to_datetime(end_date)]
    transactions = df["Order ID"].nunique()
    revenue = df["Revenue"].sum()
    monthly = df.groupby("Month", as_index=False)[["Revenue", "Profit"]].sum()
    products = df.groupby("Product", as_index=False)[["Revenue", "Profit"]].sum().sort_values("Revenue", ascending=False).head(10)
    regions = df.groupby("Region", as_index=False)["Revenue"].sum().sort_values("Revenue", ascending=False)
    margin = df["Profit"].sum() / revenue * 100 if revenue else 0
    return {"kpis":{"revenue":round(revenue,2),"profit":round(df["Profit"].sum(),2),"transactions":int(transactions),"quantity":int(df["Quantity"].sum()),"aov":round(revenue/transactions,2) if transactions else 0,"margin":round(margin,1)},"monthly":monthly.to_dict("records"),"products":products.to_dict("records"),"regions":regions.to_dict("records"),"rows":len(df),"top_product":products.iloc[0]["Product"] if len(products) else "—","data_quality":{"raw_rows":raw_rows,"cleaned_rows":len(df),"duplicates_removed":duplicates_removed,"invalid_dates_removed":invalid_dates_removed},"filters":{"regions":available_regions,"categories":available_categories,"min_date":min_date,"max_date":max_date}}


@app.get("/", response_class=HTMLResponse)
def home():
    return (ROOT / "index.html").read_text(encoding="utf-8")

@app.get("/api/filters")
def filters():
    d = load_data()
    return {"regions":sorted(d["Region"].unique().tolist()),"categories":sorted(d["Category"].unique().tolist()),"min_date":d["Order Date"].min().strftime("%Y-%m-%d"),"max_date":d["Order Date"].max().strftime("%Y-%m-%d")}

@app.get("/api/health")
def health():
    return {"status":"ok"}

@app.get("/api/dashboard")
def dashboard(region: str="", category: str="", start_date: str="", end_date: str=""):
    return make_dashboard(load_data(), region, category, start_date, end_date)

@app.post("/api/analyze")
async def analyze(file: UploadFile = File(...), region: str="", category: str="", start_date: str="", end_date: str=""):
    name = (file.filename or "").lower()
    if name.endswith(".csv"):
        df = pd.read_csv(file.file)
    elif name.endswith((".xlsx", ".xls")):
        df = pd.read_excel(file.file)
    else:
        raise HTTPException(400, "Please upload a CSV or Excel file.")
    cleaned = clean_data(df)
    result = make_dashboard(cleaned, region, category, start_date, end_date)
    result["source"] = file.filename
    return result

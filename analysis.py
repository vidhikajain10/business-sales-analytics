import pandas as pd

def load_data(path="data/sales_data.csv"):
    df = pd.read_csv(path).drop_duplicates().copy()
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
    df = df.dropna(subset=["Order Date"])
    for col in ["Product", "Category", "Region"]:
        df[col] = df[col].fillna("Unknown").astype(str).str.strip()
    for col in ["Quantity", "Unit Price", "Revenue", "Cost", "Profit"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["Quantity"] = df["Quantity"].fillna(0)
    df["Unit Price"] = df["Unit Price"].fillna(0)
    df["Revenue"] = df["Revenue"].fillna(df["Quantity"] * df["Unit Price"])
    df["Cost"] = df["Cost"].fillna(df["Revenue"] - df["Profit"])
    df["Profit"] = df["Profit"].fillna(df["Revenue"] - df["Cost"])
    df["Month"] = df["Order Date"].dt.to_period("M").astype(str)
    return df

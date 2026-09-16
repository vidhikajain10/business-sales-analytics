import streamlit as st
import plotly.express as px
from analysis import load_data

st.set_page_config(page_title="Business Sales Analytics", page_icon="📊", layout="wide")
st.markdown("""
<style>
.block-container {max-width: 1200px; padding-top: 2rem;}
[data-testid="stMetric"] {border: 1px solid #e5e7eb; border-radius: 10px; padding: 14px;}
</style>
""", unsafe_allow_html=True)

df = load_data()

st.title("Business Sales Analytics")
st.caption("Interactive sales performance and KPI dashboard")

st.sidebar.header("Filters")
start, end = st.sidebar.date_input(
    "Date range", value=(df["Order Date"].min().date(), df["Order Date"].max().date()),
    min_value=df["Order Date"].min().date(), max_value=df["Order Date"].max().date()
)
regions = st.sidebar.multiselect("Region", sorted(df["Region"].unique()), default=sorted(df["Region"].unique()))
categories = st.sidebar.multiselect("Category", sorted(df["Category"].unique()), default=sorted(df["Category"].unique()))

filtered = df[
    (df["Order Date"].dt.date >= start) &
    (df["Order Date"].dt.date <= end) &
    df["Region"].isin(regions) &
    df["Category"].isin(categories)
]

if filtered.empty:
    st.warning("No sales data matches the selected filters.")
    st.stop()

revenue = filtered["Revenue"].sum()
profit = filtered["Profit"].sum()
transactions = filtered["Order ID"].nunique()
quantity = filtered["Quantity"].sum()
aov = revenue / transactions if transactions else 0

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Revenue", f"${revenue:,.0f}")
k2.metric("Total Profit", f"${profit:,.0f}")
k3.metric("Transactions", f"{transactions:,}")
k4.metric("Avg Order Value", f"${aov:,.0f}")

monthly = filtered.groupby("Month", as_index=False)[["Revenue", "Profit"]].sum()
fig_month = px.line(monthly, x="Month", y=["Revenue", "Profit"], markers=True, labels={"value":"Amount", "variable":"Metric"})
fig_month.update_layout(height=380, margin=dict(l=0,r=0,t=30,b=0), legend_title_text="")
st.subheader("Monthly Performance")
st.plotly_chart(fig_month, use_container_width=True)

product = filtered.groupby("Product", as_index=False)[["Revenue", "Profit"]].sum().sort_values("Revenue", ascending=False).head(10)
region = filtered.groupby("Region", as_index=False)["Revenue"].sum().sort_values("Revenue", ascending=False)

c1, c2 = st.columns(2)
with c1:
    st.subheader("Product Performance")
    fig_product = px.bar(product, x="Product", y=["Revenue", "Profit"], barmode="group", labels={"value":"Amount", "variable":"Metric"})
    fig_product.update_layout(height=420, margin=dict(l=0,r=0,t=30,b=0), legend_title_text="")
    st.plotly_chart(fig_product, use_container_width=True)
with c2:
    st.subheader("Regional Performance")
    fig_region = px.bar(region, x="Region", y="Revenue", labels={"Revenue":"Revenue"})
    fig_region.update_layout(height=420, margin=dict(l=0,r=0,t=30,b=0))
    st.plotly_chart(fig_region, use_container_width=True)

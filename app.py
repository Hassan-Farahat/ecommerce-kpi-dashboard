import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Page setup
st.set_page_config(page_title="E-Commerce KPI Dashboard", page_icon="📊", layout="wide")

# Generate synthetic dataset (no external CSV file needed)
@st.cache_data
def load_data():
    np.random.seed(42)
    dates = pd.date_range(start="2024-01-01", periods=180)
    categories = ["Electronics", "Clothing", "Home & Kitchen", "Beauty"]
    regions = ["North America", "Europe", "Asia-Pacific", "LATAM"]
    
    data = []
    for _ in range(1000):
        data.append({
            "Date": np.random.choice(dates),
            "Category": np.random.choice(categories),
            "Region": np.random.choice(regions),
            "Sales": round(np.random.uniform(20, 500), 2),
            "Profit": round(np.random.uniform(5, 150), 2)
        })
    df = pd.DataFrame(data)
    df["Date"] = pd.to_datetime(df["Date"])
    return df

df = load_data()


# Sidebar filters
st.sidebar.header("Filters")
region_filter = st.sidebar.multiselect("Region", df["Region"].unique(), default=df["Region"].unique())
category_filter = st.sidebar.multiselect("Category", df["Category"].unique(), default=df["Category"].unique())

filtered_df = df[(df["Region"].isin(region_filter)) & (df["Category"].isin(category_filter))]
if filtered_df.empty:
    st.warning("⚠️ Please select at least one Region and Category from the sidebar.")
    st.stop()

# Header
st.title("📊 Executive Sales & Revenue Dashboard")
st.markdown("Track sales performance, margins, and market distributions in real time.")



# Top KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", f"${filtered_df['Sales'].sum():,.2f}")
col2.metric("Total Profit", f"${filtered_df['Profit'].sum():,.2f}")
col3.metric("Total Orders", f"{len(filtered_df):,}")
col4.metric("Avg Order Value", f"${filtered_df['Sales'].mean() if len(filtered_df) > 0 else 0:,.2f}")

st.markdown("---")



# Charts
c1, c2 = st.columns(2)

with c1:
    st.subheader("Monthly Revenue Trend")
    monthly = filtered_df.groupby(filtered_df["Date"].dt.to_period("M"))["Sales"].sum().reset_index()
    monthly["Date"] = monthly["Date"].astype(str)
    fig_line = px.line(monthly, x="Date", y="Sales", markers=True, template="plotly_white")
    st.plotly_chart(fig_line, use_container_width=True)

with c2:
    st.subheader("Sales by Category")
    cat_sales = filtered_df.groupby("Category")["Sales"].sum().reset_index()
    fig_bar = px.bar(cat_sales, x="Category", y="Sales", color="Category", template="plotly_white")
    st.plotly_chart(fig_bar, use_container_width=True)



# Donut Chart
st.subheader("Regional Market Share")
reg_sales = filtered_df.groupby("Region")["Sales"].sum().reset_index()
fig_pie = px.pie(reg_sales, values="Sales", names="Region", hole=0.4)
st.plotly_chart(fig_pie, use_container_width=True)
import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Financial Transactions Dashboard",
    layout="wide"
)

# Title
st.title("Financial Transactions Dashboard")

st.write(
    "Interactive dashboard for the analysis of financial transactions performed during 2024."
)

st.header("Time Analysis")

# Load data
fact_transactions = pd.read_csv("Streamlit/fact_transactions.csv")
dim_time = pd.read_csv("Streamlit/dim_time.csv")
dim_symbol = pd.read_csv("Streamlit/dim_symbol.csv")

# Merge with time dimension
data = fact_transactions.merge(
    dim_time,
    on="time_key",
    how="left"
)

data["date"] = pd.to_datetime(data["date"])

# Date filters
col1, col2 = st.columns(2)

with col1:
    start_date = st.date_input(
        "Start Date",
        value=pd.to_datetime("2024-01-01")
    )

with col2:
    end_date = st.date_input(
        "End Date",
        value=pd.to_datetime("2024-12-31")
    )

st.write(
    f"Selected period: {start_date} to {end_date}"
)

# Filter data
filtered_data = data[
    (data["date"] >= pd.to_datetime(start_date))
    &
    (data["date"] <= pd.to_datetime(end_date))
]

# Metrics
col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Total Transactions",
        len(filtered_data)
    )

with col2:
    st.metric(
        "Traded Symbols",
        filtered_data["symbol_key"].nunique()
    )

# Chart 1
st.subheader("Total Transactions Over Time")

transactions_over_time = (
    filtered_data.groupby("date")
    .size()
)

st.line_chart(transactions_over_time)

# Merge symbol information
data_symbols = filtered_data.merge(
    dim_symbol,
    on="symbol_key",
    how="left"
)

# Top symbols
top_symbols = (
    data_symbols.groupby("symbol")
    .size()
    .sort_values(ascending=False)
    .head(3)
)

# Top sectors
top_sectors = (
    data_symbols.groupby("sector")
    .size()
    .sort_values(ascending=False)
    .head(5)
)

# Display in two columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("Top 3 Traded Symbols")
    st.bar_chart(top_symbols)

with col2:
    st.subheader("Top 5 Sectors by Transaction Count")
    st.bar_chart(top_sectors)

# Top industries
st.subheader("Top 5 Industries by Transaction Count")

top_industries = (
    data_symbols.groupby("industry")
    .size()
    .sort_values(ascending=False)
    .head(5)
)

st.bar_chart(top_industries)

# Footer
st.divider()

st.caption(
    "Big Data Analytics - Homework 3 | Financial Transactions Dashboard"
)
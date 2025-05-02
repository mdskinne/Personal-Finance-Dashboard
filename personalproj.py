# Personal Finance & Investment Dashboard
# Core structure using Streamlit, pandas, and yfinance integration placeholders

import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px
from datetime import datetime

# ---------------------------------
# Sidebar - Navigation
# ---------------------------------
st.sidebar.title("Finance Dashboard")
page = st.sidebar.radio("Navigate", ["Expenses & Budget", "Investment Portfolio", "Net Worth Overview"])

# ---------------------------------
# Data Loaders and Helpers
# ---------------------------------
def load_transactions(file):
    df = pd.read_csv(file)
    df["Date"] = pd.to_datetime(df["Date"])
    return df

def fetch_stock_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    data = data[["Open", "High", "Low", "Close", "Volume"]]
    data["Ticker"] = ticker
    return data.reset_index()

# ---------------------------------
# Expenses & Budget Tab
# ---------------------------------
if page == "Expenses & Budget":
    st.title("💸 Expenses & Budget Overview")
    uploaded_file = st.file_uploader("Upload your transactions (CSV)", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)

        # Parse date and create month column
        df["Date"] = pd.to_datetime(df["Date"])
        df["Month"] = df["Date"].dt.to_period("M").astype(str)

        st.subheader("📋 Preview of Transactions")
        st.dataframe(df.head())

        # -------------------------------
        # 📊 Category Summary (all-time)
        # -------------------------------
        category_summary = df.groupby("Category")["Amount"].sum().sort_values()
        st.subheader("📊 Total by Category")
        fig1 = px.bar(category_summary.reset_index(), x="Category", y="Amount", title="Spending by Category")
        st.plotly_chart(fig1)

        # -------------------------------
        # 📆 Monthly Net Cash Flow
        # -------------------------------
        monthly_summary = df.groupby("Month")["Amount"].sum().reset_index()
        st.subheader("📅 Monthly Income vs Expenses")
        fig2 = px.bar(monthly_summary, x="Month", y="Amount", title="Net Cash Flow Over Time")
        st.plotly_chart(fig2)

        # -------------------------------
        # 🧾 Category Budgets & Alerts
        # -------------------------------
        st.subheader("💼 Monthly Budget Settings")
        categories = df["Category"].unique()
        budget_inputs = {}

        for cat in categories:
            budget_inputs[cat] = st.number_input(f"Set budget for {cat}", value=500.0, step=50.0)

        st.subheader("🚨 Budget Alerts")
        for cat in categories:
            spent = df[df["Category"] == cat]["Amount"].sum()
            budget = budget_inputs[cat]
            if -spent > budget:
                st.warning(f"⚠️ You exceeded your budget for **{cat}**! (Spent: ${-spent:.2f}, Budget: ${budget:.2f})")

        # -------------------------------
        # 🥧 Monthly Pie Chart Selector
        # -------------------------------
        expense_df = df[df["Amount"] < 0]
        available_months = expense_df["Month"].unique()
        selected_month = st.selectbox("🗓️ Select Month for Spending Breakdown", sorted(available_months))

        filtered_df = expense_df[expense_df["Month"] == selected_month]
        month_category_summary = filtered_df.groupby("Category")["Amount"].sum().abs().reset_index()

        st.subheader(f"🥧 Spending Breakdown for {selected_month}")
        fig3 = px.pie(
            month_category_summary,
            names="Category",
            values="Amount",
            title=f"Spending by Category - {selected_month}"
        )
        st.plotly_chart(fig3)
       

      

# ---------------------------------
# Investment Portfolio Tab
# ---------------------------------
elif page == "Investment Portfolio":
    st.title("📈 Investment Portfolio")
    tickers = st.text_input("Enter tickers (comma separated):", "AAPL,MSFT,GOOGL")
    start_date = st.date_input("Start Date", datetime(2022, 1, 1))
    end_date = st.date_input("End Date", datetime.today())

    if st.button("Fetch Portfolio Data"):
        tickers_list = [t.strip() for t in tickers.split(",")]
        price_data = {}

        for ticker in tickers_list:
            df = yf.download(ticker, start=start_date, end=end_date)[["Close"]]
            df.columns = [ticker]  # Rename 'Close' column to ticker name
            price_data[ticker] = df

        # Combine all close price columns
        combined_df = pd.concat(price_data.values(), axis=1)
        combined_df.reset_index(inplace=True)

        # ---- Cumulative Return Calculation ----
        returns_df = combined_df.copy()
        returns_df.set_index("Date", inplace=True)
        returns_df = returns_df.pct_change().dropna()

        cumulative_returns = (1 + returns_df).cumprod().reset_index()

        # Melt for Plotly
        melted_returns = cumulative_returns.melt(id_vars=["Date"], var_name="Ticker", value_name="Cumulative Return")

        # Plot
        st.subheader("Portfolio Cumulative Returns")
        fig = px.line(melted_returns, x="Date", y="Cumulative Return", color="Ticker", title="Cumulative Returns Over Time")
        st.plotly_chart(fig)

# ---------------------------------
# Net Worth Tab
# ---------------------------------
elif page == "Net Worth Overview":
    st.title("💼 Net Worth Overview")
    st.write("Add your assets and liabilities manually.")

    assets = st.number_input("Total Assets ($)", min_value=0.0, value=50000.0)
    liabilities = st.number_input("Total Liabilities ($)", min_value=0.0, value=15000.0)

    net_worth = assets - liabilities
    st.metric("Net Worth", f"${net_worth:,.2f}")

    # Pie chart
    net_df = pd.DataFrame({
        "Type": ["Assets", "Liabilities"],
        "Value": [assets, liabilities]
    })
    fig = px.pie(net_df, names="Type", values="Value", title="Assets vs. Liabilities")
    st.plotly_chart(fig)

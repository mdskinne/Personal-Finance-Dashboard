# 💼 Personal Finance & Investment Dashboard

An interactive web-based dashboard built using **Streamlit** for tracking your personal finances, budgeting, investments, and net worth—all in one place. Upload your transaction data, analyze your spending, visualize investment performance, and track your net worth with ease.

---

## 🚀 Features

### 📊 Expenses & Budget
- Upload your CSV transactions file
- Automatic categorization and monthly breakdown
- Budget input for each category with over-budget alerts
- Visualizations:
  - Total spend by category
  - Monthly net cash flow
  - Monthly spending pie charts

### 📈 Investment Portfolio
- Enter stock tickers (e.g., `AAPL, MSFT, GOOGL`)
- Fetch historical price data from Yahoo Finance
- Plot cumulative returns over time
- Compare performance across multiple tickers

### 💼 Net Worth Overview
- Manually input total assets and liabilities
- Auto-calculates net worth
- Visualizes asset vs. liability breakdown via pie chart

---

## 🛠️ Tech Stack

- [Streamlit](https://streamlit.io/) — Frontend web framework
- [pandas](https://pandas.pydata.org/) — Data manipulation
- [yfinance](https://pypi.org/project/yfinance/) — Stock price data
- [plotly](https://plotly.com/python/) — Interactive charts

---

## 📄 Sample CSV Format (for transactions)

Make sure your CSV has at least the following columns:

| Date       | Description     | Category       | Amount |
|------------|------------------|----------------|--------|
| 2024-04-01 | Starbucks Coffee | Food & Dining  | -5.75  |
| 2024-04-03 | Paycheck         | Income         | 2500   |

- **Amount**: Expenses should be negative, income positive.
- **Category**: Used for budgeting and breakdowns.

---

## ▶️ How to Run

1. **Clone the repository**
2. **Install Packages**
3. **Run streamlit run personalproj.py**

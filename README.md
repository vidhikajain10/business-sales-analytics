# Business Sales Analytics & KPI Reporting

A practical business analytics project that cleans sales data, calculates KPIs, and serves an interactive web dashboard through a FastAPI backend.

## Features

- Sales data cleaning with Pandas
- Revenue, profit, transactions, quantity, and average order value KPIs
- Monthly revenue and profit trends
- Product and regional performance
- FastAPI backend endpoints
- Responsive browser dashboard
- SQL analysis queries
- Streamlit version included for local analytics

## Tech Stack

**Python | Pandas | SQL | FastAPI | Streamlit | Chart.js | Git/GitHub**

## Flow

**Raw Sales Data → Cleaning → KPI Calculation → FastAPI Backend → Interactive Dashboard**

The included CSV is a synthetic dataset created for project demonstration.

## Run Locally

### Web dashboard

```bash
pip install -r requirements.txt
uvicorn api.index:app --reload
```

Open `http://127.0.0.1:8000` after serving the frontend with your preferred static server.

### Streamlit version

```bash
pip install pandas streamlit plotly
streamlit run app.py
```

## API

- `GET /api/health` — backend health check
- `GET /api/dashboard` — KPI and chart data

## KPIs

- **Total Revenue:** Sum of sales revenue
- **Total Profit:** Revenue minus cost
- **Total Transactions:** Unique orders
- **Average Order Value:** Revenue divided by unique transactions

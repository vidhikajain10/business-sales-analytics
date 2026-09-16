# Business Sales Analytics & KPI Reporting

A manager-friendly sales analytics tool that cleans business data, calculates KPIs, and turns CSV or Excel files into an interactive dashboard.

## How It Works

**Upload Data → Clean & Validate → Calculate KPIs → Filter → Analyze → Make Decisions**

1. **Upload** — Upload a CSV or Excel sales file, or use the included sample data.
2. **Clean** — The app removes duplicate records, converts dates and numbers, standardizes text fields, and fills calculable missing values.
3. **Analyze** — Pandas calculates revenue, profit, transactions, quantity, average order value, and profit margin.
4. **Filter** — Managers can filter results by region, category, and date range.
5. **Visualize** — Interactive charts show monthly trends, regional performance, and top products.
6. **Review** — KPI cards and performance insights provide a quick view for business reviews and decision-making.

## Manager Use Cases

- Monitor revenue and profit performance
- Identify high-performing products and regions
- Compare monthly sales trends
- Check average order value and sales volume
- Spot profitability changes using profit margin
- Analyze a new sales file without changing the application code
- Export a KPI summary for reporting

## Features

- CSV and Excel upload
- Automatic data cleaning and validation
- Revenue, profit, profit margin, transactions, quantity, and AOV KPIs
- Monthly revenue and profit trends
- Product and regional performance
- Interactive Region, Category, and Date filters
- Manager-focused performance insights
- KPI summary download
- Responsive business dashboard
- FastAPI backend with Pandas analytics
- SQL analysis queries
- Included sample sales dataset

## Expected Data

The tool works best with columns such as:

`Order ID`, `Order Date`, `Product`, `Category`, `Region`, `Quantity`, `Unit Price`, `Revenue`, `Cost`, `Profit`

Common column-name variations can be handled during upload where possible. Revenue and profit can also be calculated when enough source fields are available.

## Tech Stack

**Python | Pandas | SQL | FastAPI | Chart.js | HTML/CSS/JavaScript | Git/GitHub**

## Project Flow

```text
CSV / Excel
    ↓
Data Cleaning & Validation
    ↓
KPI Calculation with Pandas
    ↓
FastAPI Backend
    ↓
Interactive Dashboard
    ↓
Manager Insights & Reporting
```

## Run Locally

```bash
pip install -r requirements.txt
uvicorn api.index:app --reload
```

Open `http://127.0.0.1:8000`.

## API

- `GET /api/health` — backend health check
- `GET /api/filters` — available dashboard filters
- `GET /api/dashboard` — KPI and chart data
- `POST /api/analyze` — analyze an uploaded CSV or Excel file

## KPIs

- **Total Revenue** — total sales revenue
- **Total Profit** — revenue minus cost
- **Profit Margin** — profit as a percentage of revenue
- **Transactions** — unique orders
- **Quantity Sold** — total units sold
- **Average Order Value** — revenue divided by transactions

The included CSV is a synthetic dataset created for project demonstration.

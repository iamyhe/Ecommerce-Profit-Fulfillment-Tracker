<p align="center">
  <h1 align="center">📊 E-Commerce Profit & Fulfillment</h1>
  <p align="center">
    An end-to-end data analytics project — from raw data cleaning to a production-ready interactive dashboard — built to surface actionable E-commerce and Supply Chain insights.
  </p>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Pandas-2.0+-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas"/>
  <img src="https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit"/>
  <img src="https://img.shields.io/badge/Plotly-5.18+-3F4F75?style=for-the-badge&logo=plotly&logoColor=white" alt="Plotly"/>
</p>

---

## 🧩 Business Problem

Retail and E-commerce businesses generate massive volumes of transactional data daily, yet most of it sits in raw CSVs — disconnected from decision-makers. This project bridges that gap by transforming **9,800 raw Superstore sales records** into a clean, interactive dashboard that answers critical business questions:

- **Where is revenue concentrated** — and which product lines underperform?
- **How does sales volume shift** across months and seasons?
- **Are shipping SLAs being met** across different fulfilment modes?
- **What is the average order value** — and how does it change by region?

The result is a tool that lets analysts and leadership explore the data in real time through filters, KPIs, and interactive charts — no SQL or Python required.

---

## 🔬 Data Cleaning Methodology

Raw data rarely arrives analysis-ready. The [`data_quality_report.py`](data_quality_report.py) script first profiled the dataset and identified three issues, which [`data_cleaning.py`](data_cleaning.py) then resolved:

| Issue Found | Cleaning Action |
|---|---|
| **11 missing values** in `Postal Code` | Filled with the placeholder `"Unknown"` to preserve all rows, then cast the column from `float64` → `string` to eliminate trailing `.0` decimals |
| **Date columns stored as strings** | Converted `Order Date` and `Ship Date` from `object` → `datetime64` using `pd.to_datetime()` with explicit `DD/MM/YYYY` format parsing |
| **No fulfilment speed metric** | Engineered a new feature — `Shipping_Time_Days` — calculated as `(Ship Date − Order Date).dt.days` to quantify delivery performance |

Additionally, the `Row ID` column was dropped as it carries no analytical value.

The cleaned output is saved as [`cleaned_superstore.csv`](cleaned_superstore.csv) — a ready-to-query dataset with **0 nulls, 18 columns, and 9,800 rows**.

---

## ✨ Key Features & Insights

### Interactive Filters (Sidebar)
- **Date Range Picker** — Slice the data to any time window within the dataset.
- **Region Multi-Select** — Compare performance across South, West, East, and Central regions, individually or combined.

### KPI Metrics (Top Row)
| Metric | Business Question It Answers |
|---|---|
| **Total Sales** | What is the overall revenue in the selected period/region? |
| **Total Orders** | How many unique orders were placed? |
| **Avg Order Value (AOV)** | How much does a typical order generate? |
| **Avg Shipping Time** | How fast are we fulfilling orders on average? |

### Interactive Charts
| Chart | Type | Insight |
|---|---|---|
| **Monthly Sales Trend** | Area chart | Reveals seasonality, growth momentum, and demand peaks for inventory & marketing planning |
| **Sales by Sub-Category** | Horizontal bar | Ranks all 17 product sub-categories by revenue — highlights top performers and candidates for promotion or discontinuation |
| **Shipping Time by Ship Mode** | Box plot | Compares median delivery speed, spread, and outliers across Same Day, First Class, Second Class, and Standard Class fulfilment |

All charts are fully interactive — hover for tooltips, zoom, pan, and export to PNG.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Data Processing** | Python 3.10+, Pandas |
| **Visualization** | Plotly Express |
| **Web Framework** | Streamlit |
| **Styling** | Custom CSS (dark theme, glassmorphism KPI cards) |

---

## 🚀 How to Run Locally

### Prerequisites
- Python 3.10 or higher installed on your system.

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/iamyhe/Ecommerce-Profit-Fulfillment-Tracker.git
   cd interactive-sales-supply-chain-dashboard
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate        # macOS / Linux
   venv\Scripts\activate           # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the data cleaning pipeline** (generates `cleaned_superstore.csv`)
   ```bash
   python data_cleaning.py
   ```

5. **Launch the dashboard**
   ```bash
   streamlit run dashboard.py
   ```

6. **Open your browser** at [http://localhost:8501](http://localhost:8501) and explore!

---

## 📁 Project Structure

```
├── train.csv                  # Raw Superstore sales data (9,800 rows)
├── data_quality_report.py     # Step 1 — Data profiling & quality audit
├── data_cleaning.py           # Step 2 — Cleaning, type conversion & feature engineering
├── cleaned_superstore.csv     # Step 3 — Analysis-ready output
├── dashboard.py               # Step 4 — Interactive Streamlit dashboard
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation (this file)
```

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).

---

<p align="center">
  <sub>Built with ❤️ using Python, Pandas, Streamlit & Plotly</sub>
</p>

# 🛒 Myntra Sales Analysis — Interactive Streamlit App

An end-to-end sales analytics web app built with **Python, pandas, Plotly and Streamlit**. Upload a raw Myntra sales CSV, clean it in one click, download the cleaned data, and explore revenue, order, customer and product insights through interactive dashboards — or write your **own Python analysis** in a built-in code box.

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.55-FF4B4B?logo=streamlit&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-3.0-150458?logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-6.6-3F4F75?logo=plotly&logoColor=white)

---

## 📑 Table of Contents

1. [Overview](#-overview)
2. [Key Features](#-key-features)
3. [Screenshots](#-screenshots)
4. [Dataset](#-dataset)
5. [Data Cleaning Pipeline](#-data-cleaning-pipeline)
6. [Business Questions Answered](#-business-questions-answered)
7. [Custom Python Analysis](#-custom-python-analysis)
8. [Project Structure](#-project-structure)
9. [Getting Started](#-getting-started)
10. [How to Use the App](#-how-to-use-the-app)
11. [Design Decisions](#-design-decisions)
12. [Limitations & Future Work](#-limitations--future-work)
13. [Author](#-author)

---

## 🎯 Overview

Most analytics projects live in notebooks that only the author can run. This project turns a full analysis workflow into a **self-service web app** that anyone can use without writing code:

```
Raw CSV  ──►  Clean & validate  ──►  Download clean CSV  ──►  Explore dashboards  ──►  Custom Python analysis
```

The data is a **Myntra e-commerce orders dataset** (8,000 orders, 2023–2025). The app answers practical business questions: *Which categories and brands earn the most? Which payment mode has the highest order value? Where are orders cancelled or returned?*

---

## ✨ Key Features

| Page | What it does |
|------|--------------|
| 🧹 **Data Cleaning** | Upload raw CSV → standardise column names, drop PII, fill missing ratings, strip whitespace → full cleaning report → download `clean_dataset.csv` |
| 📊 **Exploratory Data Analysis** | KPI cards (revenue, orders, AOV), statistical summary, correlation heatmap, outlier box plots |
| 📈 **Sales** | Revenue by category, brand, state, year and order channel |
| 💰 **Average Order Value** | AOV by category, brand, payment mode, order channel and product |
| 🛍️ **Order Analysis** | Orders by city, channel, order status, gender and age group |
| 👥 **Customer Analysis** | Unique customers by payment mode, membership tier and order channel |
| 📦 **Product Analysis** | Product-level orders, revenue, quantity, average discount and delivery days |
| 🧪 **Custom Python Analysis** | Type your own pandas / plotly code, run it on the cleaned data, and download the result as CSV |

**Highlights**
- 🔗 **One continuous flow** — cleaned data is shared between pages automatically (no re-uploading), with a fallback to upload any clean CSV.
- 🎨 **Custom styling** — KPI cards, sidebar navigation and file-uploader theming via `style.css`.
- 🧩 **Modular code** — every page is one `render_*()` function; adding a new page takes 3 lines in `app.py`.

---

## 📸 Screenshots

### 1. Data Cleaning — upload, clean, and review the report
![Data Cleaning](screenshots/screenshots/data_clean.pdf)

### 2. Exploratory Data Analysis — summary statistics and correlation heatmap
![EDA](screenshots/EDA.pdf)

### 3. Sales Analysis — revenue breakdowns with interactive charts
![Sales Analysis](screenshots/sales_analysis.pdf)

<details>
<summary><b>More pages (click to expand)</b></summary>

#### Average Order Value
![AOV](screenshots/AOV.pdf)

#### Order Analysis
![Order Analysis](screenshots/order_analysis.pdf)

#### Customer Analysis
![Customer Analysis](screenshots/customer_analysis.pdf)

#### Product Analysis
![Product Analysis](screenshots/product_analysis.pdf)

</details>

### 4. Custom Python Analysis — write your own code, get a table + CSV download
![Custom Analysis](screenshots/custom_analysis.pdf)

---

## 📂 Dataset

| Property | Value |
|----------|-------|
| Source file | `dataset/Myntra_Sales_Dataset.csv` (raw) · `dataset/clean_dataset.csv` (cleaned) |
| Rows | 8,000 orders |
| Columns | 29 raw → 28 after cleaning |
| Period | 1 Jan 2023 – 31 Dec 2025 |
| Coverage | 35 brands · 6 categories · 15 states · 20 cities · ~2,500 customers |

<details>
<summary><b>Column dictionary</b></summary>

| Group | Columns |
|-------|---------|
| **Order** | `order_id`, `order_date`, `order_month`, `order_quarter`, `order_year`, `order_status`, `order_channel`, `payment_mode`, `delivery_days` |
| **Customer** | `customer_id`, `gender`, `age`, `city`, `state`, `membership_tier` |
| **Product** | `product_id`, `product_name`, `category`, `sub_category`, `brand`, `color`, `size` |
| **Pricing** | `mrp`, `discount_percent`, `selling_price`, `quantity`, `total_amount` |
| **Feedback** | `rating` |

`customer_name` exists in the raw file and is **dropped during cleaning** (personal data is not needed for analysis).

</details>

---

## 🧹 Data Cleaning Pipeline

Implemented in `streamlit_/data_clean/data_clean.py`. Each step is a small, testable function.

| # | Step | Detail |
|---|------|--------|
| 1 | Standardise columns | Replace the text `"NaN"` with real nulls; make names `snake_case` (`Order_ID` → `order_id`) |
| 2 | Drop PII | Remove `customer_name` |
| 3 | Quality check | Null counts, duplicate count, shape |
| 4 | Handle missing values | `rating` had **2,142 nulls (~27%)** → filled with the **median** (robust to the skewed 1–5 scale) |
| 5 | Profile categories | Unique values per text column + `category × size` crosstab to spot inconsistent labels |
| 6 | Strip whitespace | Trim leading/trailing spaces in all text columns, then verify none remain |

The page shows a live **Cleaning Report** (metrics + 6 expandable checks) and a **Download Clean Data (CSV)** button.

---

## 💡 Business Questions Answered

<details>
<summary><b>Sales</b></summary>

- Which categories, brands and states generate the most revenue?
- How does revenue trend year over year?
- Which order channel (Website / Mobile App / Mobile Web) earns the most?
</details>

<details>
<summary><b>Average Order Value (AOV)</b></summary>

- Which category and brand have the highest AOV?
- Which payment modes are associated with higher order values?
- Which order channel and which product drive the highest AOV?
</details>

<details>
<summary><b>Orders</b></summary>

- Which cities place the most orders?
- How do orders split by channel, status (Delivered / Returned / Cancelled / Pending), gender and age group?
</details>

<details>
<summary><b>Customers & Products</b></summary>

- How many unique customers use each payment mode, membership tier and channel?
- Which products lead in revenue, quantity sold, discount level and delivery time?
</details>

### Sample findings from this dataset

- **Total revenue ≈ ₹2.13 Cr** from 8,000 orders, with an average order value of about **₹2,658**.
- **Women (₹71.0 L)** and **Men (₹66.9 L)** are the top two categories; together they bring in over 60% of revenue.
- **H&M, Roadster and Puma** are the top three brands by revenue.
- About **73% of orders are delivered**, while **~12% are returned** and **~9.5% are cancelled** — a clear area for operational improvement.

---

## 🧪 Custom Python Analysis

The last page lets you run **your own Python code** on the cleaned data — like a mini notebook inside the app.

**Rules (kept simple):**

| You want to… | Write… |
|--------------|--------|
| Use the data | it is the variable `df` (a safe copy) |
| Show a table (with CSV download) | `result = ...` |
| Show a chart | `fig = px.bar(...)` or draw with `plt` / `sns` |
| Show text | `print(...)` |
| Use Streamlit directly | `st.dataframe(...)`, `st.write(...)` also work |

`pd`, `np`, `px`, `plt`, `sns` and `st` are pre-imported. The last line of your code is shown automatically, like a notebook cell.

**Example**

```python
def discount_band(val):
    if val <= 10:   return "0-10% (Low)"
    elif val <= 25: return "11-25% (Medium)"
    elif val <= 40: return "26-40% (High)"
    else:           return "41%+ (Very High)"

df["discount_band"] = df["discount_percent"].apply(discount_band)

result = (
    df.groupby("discount_band")
      .agg(orders=("order_id", "count"),
           total_qty=("quantity", "sum"),
           total_revenue=("total_amount", "sum"))
      .round(2)
)
```

**Built-in conveniences**
- 5 ready-made examples in a dropdown
- Expandable list of all columns with data types
- Auto-fix for accidental leading spaces (common when pasting code)
- Clear, readable error messages with the line number

> ⚠️ **Security note:** the page runs user-written code with a basic safety guard (blocks `open`, `eval`, `exec`, `os`/`subprocess` imports and dunder tricks). This is a **seat-belt for accidents, not a sandbox**. It is designed for **local use**. If you deploy the app publicly, remove this page or put it behind authentication.

---

## 🗂️ Project Structure

```
Myntra sales streamlit/
│
├── app.py                        # Entry point: page config, CSS, sidebar navigation, routing
├── requirements.txt              # Python dependencies
├── README.md
│
├── dataset/
│   ├── Myntra_Sales_Dataset.csv  # Raw data (upload this on the Data Cleaning page)
│   └── clean_dataset.csv         # Cleaned data (output of the pipeline)
│
├── 
│   └── screenshots/              # Images used in this README
│
└── streamlit_/
    ├── helper.py                 # Shared utilities: get_clean_df(), kpi_card(), footer()
    ├── style.css                 # Custom styling (KPI cards, sidebar, uploader)
    │
    ├── data_clean/
    │   └── data_clean.py         # Cleaning functions + Data Cleaning page
    │
    └── EDA/
        ├── EDA.py                # Summary stats, correlation heatmap, outliers, KPIs
        ├── sales_analysis.py     # Revenue analysis
        ├── AOV.py                # Average order value analysis
        ├── order_analysis.py     # Order analysis
        ├── customer_analysis.py  # Customer analysis
        ├── product_analysis.py   # Product analysis
        └── custom_analysis.py    # Custom Python analysis (code box)
```

---

## 🚀 Getting Started

### Prerequisites
- Python **3.11 or newer**
- `pip`

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/Ishasavani1402/myntra-sales-analysis-streamlit.git
cd myntra-sales-analysis-streamlit

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

The app opens at **http://localhost:8501**.

### Dependencies

```
streamlit==1.55.0
pandas==3.0.5
numpy==2.4.0
matplotlib==3.10.8
seaborn==0.13.2
plotly==6.6.0
```

---

## 🧭 How to Use the App

1. **Open 🧹 Data Cleaning** and upload `dataset/Myntra_Sales_Dataset.csv`.
2. Click **Clean Data**, review the report, and (optionally) **download the clean CSV**.
3. Move to any analysis page from the sidebar — it automatically uses the data you just cleaned.
   - After a browser refresh, choose **"Upload a clean CSV"** and upload `dataset/clean_dataset.csv`.
4. Finish with **🧪 Custom Python Analysis** to ask your own questions.

---

## 🧠 Design Decisions

| Decision | Why |
|----------|-----|
| **`st.session_state` for sharing data** | Cleaned data is stored once and reused by every page — the user never re-uploads. It works like a shared counter between pages. |
| **`helper.py` for shared code** | `get_clean_df()`, `kpi_card()` and `footer()` live in one place, so pages never import from each other. |
| **One `render_*()` function per page** | Keeps `app.py` short (routing only) and makes new pages a 3-line change. |
| **Median imputation for ratings** | Ratings are ordinal and skewed; the median avoids creating impossible values and resists outliers. |
| **Dropping `customer_name`** | Not needed for analysis; reduces personal-data exposure. |
| **Copy of `df` for custom code** | User code can never modify or damage the cleaned dataset. |

---

## 🔭 Limitations & Future Work

- [ ] Add **true time-series forecasting** (the Sales page currently covers historical revenue breakdowns).
- [ ] Add **sidebar filters** (year, category, state) that apply across all pages.
- [ ] Add **cohort / repeat-customer and RFM segmentation** analysis.
- [ ] **Persist cleaned data** across browser refreshes (e.g., cache to disk).
- [ ] Add **unit tests** for the cleaning functions.
- [ ] **Deploy** on Streamlit Community Cloud (with the Custom Analysis page disabled or password-protected).

---

## 👩‍💻 Author

**Isha** — Aspiring Data Analyst

- GitHub: [@Ishasavani1402](https://github.com/Ishasavani1402)

If you found this project useful, please ⭐ the repository!

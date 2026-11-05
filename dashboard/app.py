
# ============================================================
# SUPPLYCHAIN INSIGHTS
# Delivery & Business Performance Dashboard
#
# Technologies: Python, Pandas, SQLite, Streamlit, Plotly
# Dataset: DataCo Smart Supply Chain
# Database: data/processed/supply_chain.db
# Table: supply_chain
# ============================================================


# ============================================================
# SECTION 1: IMPORT LIBRARIES
# ============================================================

import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import gdown

from pathlib import Path


# ============================================================
# SECTION 2: PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="SupplyChain Insights",
    page_icon="📦",
    layout="wide"
)


# ============================================================
# SECTION 3: CUSTOM CSS
# ============================================================

st.markdown("""
<style>

/* Main dashboard spacing */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Keep KPI numbers on one line */
[data-testid="stMetricValue"] {
    white-space: nowrap !important;
    overflow: visible !important;
    text-overflow: clip !important;
}

/* Adjust KPI number size */
[data-testid="stMetricValue"] div {
    font-size: clamp(1.05rem, 1.45vw, 1.65rem) !important;
    white-space: nowrap !important;
}

/* KPI labels */
[data-testid="stMetricLabel"] {
    font-size: 0.9rem;
}

/* Improve chart spacing */
div[data-testid="stPlotlyChart"] {
    margin-bottom: 1rem;
}

</style>
""", unsafe_allow_html=True)



# ============================================================
# SECTION 4: PROJECT AND DATABASE PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

# Local database path (your computer)
LOCAL_DB_PATH = (
    BASE_DIR / "data" / "processed" / "supply_chain.db"
)

# Cloud database path (Streamlit server)
CLOUD_DB_PATH = Path("/tmp/supply_chain.db")


# ============================================================
# SECTION 5: LOAD DATABASE FROM LOCAL OR GOOGLE DRIVE
# ============================================================

def get_database_path():

    # OPTION 1: Use local database if available
    if LOCAL_DB_PATH.exists():
        return str(LOCAL_DB_PATH)

    # OPTION 2: Use previously downloaded cloud database
    if CLOUD_DB_PATH.exists() and CLOUD_DB_PATH.stat().st_size > 0:
        return str(CLOUD_DB_PATH)

    # OPTION 3: Download database from Google Drive
    try:

        file_id = st.secrets["1Oz1xPlwFdCqiz-XaE6vZV5g4ypJI5-xx"]

        downloaded_file = gdown.download(
            id=file_id,
            output=str(CLOUD_DB_PATH),
            quiet=False
        )

        if (
            downloaded_file is None
            or not CLOUD_DB_PATH.exists()
            or CLOUD_DB_PATH.stat().st_size == 0
        ):
            raise RuntimeError("Google Drive database download failed.")

        return str(CLOUD_DB_PATH)

    except Exception as error:

        if CLOUD_DB_PATH.exists():
            CLOUD_DB_PATH.unlink()

        st.error(f"Database loading failed: {error}")
        st.stop()


@st.cache_data
def load_data(database_path):

    connection = sqlite3.connect(database_path)

    try:

        data = pd.read_sql_query(
            "SELECT * FROM supply_chain",
            connection
        )

    finally:

        connection.close()

    return data


# Load database and data
try:

    DB_PATH = get_database_path()

    df = load_data(DB_PATH)

except Exception as error:

    st.error(f"Unable to load database: {error}")
    st.stop()


# ============================================================
# SECTION 6: DATA PREPROCESSING
# ============================================================

# Convert date columns to datetime
df["order_date_dateorders"] = pd.to_datetime(
    df["order_date_dateorders"],
    errors="coerce"
)

df["shipping_date_dateorders"] = pd.to_datetime(
    df["shipping_date_dateorders"],
    errors="coerce"
)

# Remove unnecessary whitespace from text columns
text_columns = df.select_dtypes(include="object").columns

for column in text_columns:
    df[column] = df[column].str.strip()

# Convert financial and shipping columns to numeric
numeric_columns = [
    "sales",
    "order_item_total",
    "shipping_delay_days",
    "days_for_shipping_real",
    "days_for_shipment_scheduled"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )

# Remove records without valid order dates
df = df.dropna(
    subset=["order_date_dateorders"]
)

if df.empty:
    st.error("No usable records found.")
    st.stop()


# ============================================================
# SECTION 7: DASHBOARD HEADER
# ============================================================

st.title("📦 SupplyChain Insights")

st.header("Delivery & Business Performance Dashboard")

st.write(
    "Explore historical supply-chain performance across "
    "markets, regions, shipping modes, and product categories."
)

st.divider()


# ============================================================
# SECTION 8: SIDEBAR FILTERS
# ============================================================

st.sidebar.title("Dashboard Filters")


# ------------------------------------------------------------
# 8.1 ORDER DATE FILTER
# ------------------------------------------------------------

min_date = df["order_date_dateorders"].min().date()
max_date = df["order_date_dateorders"].max().date()

date_range = st.sidebar.date_input(
    "Select Order Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Handle date range or single date selection
if isinstance(date_range, (tuple, list)):

    if len(date_range) == 2:
        start_date, end_date = date_range
    elif len(date_range) == 1:
        start_date = end_date = date_range[0]
    else:
        start_date, end_date = min_date, max_date

else:
    start_date = end_date = date_range


# ------------------------------------------------------------
# 8.2 MARKET FILTER
# ------------------------------------------------------------

markets = sorted(
    df["market"].dropna().unique().tolist()
)

selected_markets = st.sidebar.multiselect(
    "Select Market",
    options=markets,
    default=markets
)


# ------------------------------------------------------------
# 8.3 SHIPPING MODE FILTER
# ------------------------------------------------------------

shipping_modes = sorted(
    df["shipping_mode"].dropna().unique().tolist()
)

selected_shipping_modes = st.sidebar.multiselect(
    "Select Shipping Mode",
    options=shipping_modes,
    default=shipping_modes
)


# ------------------------------------------------------------
# 8.4 REGION FILTER
# ------------------------------------------------------------

regions = sorted(
    df["order_region"].dropna().unique().tolist()
)

selected_regions = st.sidebar.multiselect(
    "Select Region",
    options=regions,
    default=regions
)


# ------------------------------------------------------------
# 8.5 PRODUCT CATEGORY FILTER
# ------------------------------------------------------------

categories = sorted(
    df["category_name"].dropna().unique().tolist()
)

selected_categories = st.sidebar.multiselect(
    "Select Product Category",
    options=categories,
    default=categories
)


# ============================================================
# SECTION 9: APPLY FILTERS
# ============================================================

filtered_df = df.copy()

# Date filter
filtered_df = filtered_df[
    (filtered_df["order_date_dateorders"].dt.date >= start_date)
    &
    (filtered_df["order_date_dateorders"].dt.date <= end_date)
]

# Market filter
filtered_df = filtered_df[
    filtered_df["market"].isin(selected_markets)
]

# Shipping mode filter
filtered_df = filtered_df[
    filtered_df["shipping_mode"].isin(selected_shipping_modes)
]

# Region filter
filtered_df = filtered_df[
    filtered_df["order_region"].isin(selected_regions)
]

# Category filter
filtered_df = filtered_df[
    filtered_df["category_name"].isin(selected_categories)
]


# ============================================================
# SECTION 10: CHECK FILTER RESULTS
# ============================================================

if filtered_df.empty:

    st.warning(
        "No records match the selected filters. "
        "Please change your selections."
    )

    st.stop()


# ============================================================
# SECTION 11: CALCULATE BUSINESS KPIs
# ============================================================

# Total order-item records
total_order_items = len(filtered_df)

# Unique orders
unique_orders = filtered_df["order_id"].nunique()

# Canceled records
canceled_records = (
    filtered_df["delivery_status"] == "Shipping canceled"
).sum()

# Exclude canceled records for delivery performance
filtered_delivery = filtered_df[
    filtered_df["delivery_status"] != "Shipping canceled"
].copy()

# Late records
late_records = (
    filtered_delivery["delivery_status"] == "Late delivery"
).sum()

# Late delivery percentage
if len(filtered_delivery) > 0:
    late_rate = (
        late_records / len(filtered_delivery)
    ) * 100
else:
    late_rate = 0

# Total sales
total_sales = filtered_df["sales"].sum()


# ============================================================
# SECTION 12: DISPLAY FIVE KPIs IN ONE ROW
# ============================================================

st.subheader("Overall Business Performance")

# IMPORTANT:
# Total Sales receives a wider column than the other KPIs.
# This prevents its long number from being cut off.

kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5 = st.columns(
    [1, 1, 1, 1.8, 1]
)

with kpi_col1:
    st.metric(
        label="Total Order Items",
        value=f"{total_order_items:,}"
    )

with kpi_col2:
    st.metric(
        label="Unique Orders",
        value=f"{unique_orders:,}"
    )

with kpi_col3:
    st.metric(
        label="Late Delivery Rate",
        value=f"{late_rate:.2f}%"
    )

with kpi_col4:
    st.metric(
        label="Total Sales",
        value=f"${total_sales:,.2f}"
    )

with kpi_col5:
    st.metric(
        label="Canceled Records",
        value=f"{canceled_records:,}"
    )

st.divider()


# ============================================================
# SECTION 13: DELIVERY STATUS DISTRIBUTION
# ============================================================

st.header("1. Delivery Status Distribution")

st.write(
    "Understand how order-item records are distributed "
    "across different delivery outcomes."
)

delivery_counts = (
    filtered_df["delivery_status"]
    .value_counts()
    .reset_index()
)

delivery_counts.columns = [
    "Delivery Status",
    "Number of Records"
]

fig_delivery = px.pie(
    delivery_counts,
    names="Delivery Status",
    values="Number of Records",
    title="Distribution of Delivery Status",
    hole=0.4
)

fig_delivery.update_layout(
    template="plotly_dark"
)

st.plotly_chart(
    fig_delivery,
    use_container_width=True
)


# ============================================================
# SECTION 14: SHIPPING MODE PERFORMANCE
# ============================================================

st.header("2. Shipping Mode Performance")

st.write(
    "Compare late delivery rates across different shipping modes. "
    "Canceled records are excluded."
)

if not filtered_delivery.empty:

    shipping_analysis = (
        filtered_delivery
        .groupby("shipping_mode")
        .agg(
            total_records=("delivery_status", "count"),
            late_records=(
                "delivery_status",
                lambda values: (values == "Late delivery").sum()
            ),
            avg_delay=("shipping_delay_days", "mean")
        )
        .reset_index()
    )

    shipping_analysis["late_rate"] = (
        shipping_analysis["late_records"]
        / shipping_analysis["total_records"]
    ) * 100

    shipping_analysis = shipping_analysis.sort_values(
        "late_rate",
        ascending=False
    )

    fig_shipping = px.bar(
        shipping_analysis,
        x="shipping_mode",
        y="late_rate",
        text=shipping_analysis["late_rate"].map(
            lambda value: f"{value:.2f}%"
        ),
        title="Late Delivery Rate by Shipping Mode",
        labels={
            "shipping_mode": "Shipping Mode",
            "late_rate": "Late Delivery Rate (%)"
        }
    )

    fig_shipping.update_traces(
        textposition="outside"
    )

    fig_shipping.update_layout(
        template="plotly_dark",
        yaxis_range=[
            0,
            min(110, max(105, shipping_analysis["late_rate"].max() + 10))
        ]
    )

    st.plotly_chart(
        fig_shipping,
        use_container_width=True
    )

    st.dataframe(
        shipping_analysis,
        use_container_width=True,
        hide_index=True
    )

else:
    st.info("No non-canceled delivery records available.")

st.divider()


# ============================================================
# SECTION 15: REGIONAL DELIVERY PERFORMANCE
# ============================================================

st.header("3. Regional Delivery Performance")

st.write(
    "Identify regions with higher late delivery rates. "
    "Only regions with at least 100 records are included."
)

if not filtered_delivery.empty:

    region_analysis = (
        filtered_delivery
        .groupby("order_region")
        .agg(
            total_records=("delivery_status", "count"),
            late_records=(
                "delivery_status",
                lambda values: (values == "Late delivery").sum()
            )
        )
        .reset_index()
    )

    region_analysis["late_rate"] = (
        region_analysis["late_records"]
        / region_analysis["total_records"]
    ) * 100

    region_analysis = region_analysis[
        region_analysis["total_records"] >= 100
    ]

    region_analysis = region_analysis.sort_values(
        "late_rate",
        ascending=False
    ).head(10)

    fig_region = px.bar(
        region_analysis,
        x="late_rate",
        y="order_region",
        orientation="h",
        text=region_analysis["late_rate"].map(
            lambda value: f"{value:.2f}%"
        ),
        title="Top 10 Regions by Late Delivery Rate",
        labels={
            "order_region": "Region",
            "late_rate": "Late Delivery Rate (%)"
        }
    )

    fig_region.update_traces(
        textposition="outside"
    )

    fig_region.update_layout(
        template="plotly_dark",
        yaxis={"categoryorder": "total ascending"}
    )

    st.plotly_chart(
        fig_region,
        use_container_width=True
    )

else:
    st.info("No regional delivery data available.")

st.divider()


# ============================================================
# SECTION 16: PRODUCT CATEGORY PERFORMANCE
# ============================================================

st.header("4. Product Category Performance")

st.write(
    "Explore product categories with higher late delivery rates. "
    "Categories with fewer than 100 records are excluded."
)

if not filtered_delivery.empty:

    category_analysis = (
        filtered_delivery
        .groupby("category_name")
        .agg(
            total_records=("delivery_status", "count"),
            late_records=(
                "delivery_status",
                lambda values: (values == "Late delivery").sum()
            )
        )
        .reset_index()
    )

    category_analysis["late_rate"] = (
        category_analysis["late_records"]
        / category_analysis["total_records"]
    ) * 100

    category_analysis = category_analysis[
        category_analysis["total_records"] >= 100
    ]

    category_analysis = category_analysis.sort_values(
        "late_rate",
        ascending=False
    ).head(10)

    fig_category = px.bar(
        category_analysis,
        x="late_rate",
        y="category_name",
        orientation="h",
        text=category_analysis["late_rate"].map(
            lambda value: f"{value:.2f}%"
        ),
        title="Top 10 Product Categories by Late Delivery Rate",
        labels={
            "category_name": "Product Category",
            "late_rate": "Late Delivery Rate (%)"
        }
    )

    fig_category.update_traces(
        textposition="outside"
    )

    fig_category.update_layout(
        template="plotly_dark",
        yaxis={"categoryorder": "total ascending"}
    )

    st.plotly_chart(
        fig_category,
        use_container_width=True
    )

else:
    st.info("No product category data available.")

st.divider()


# ============================================================
# SECTION 17: MONTHLY LATE DELIVERY TREND
# ============================================================

st.header("5. Monthly Late Delivery Trend")

st.write(
    "Track changes in late delivery rates over time."
)

if not filtered_delivery.empty:

    monthly_analysis = filtered_delivery.copy()

    monthly_analysis["month"] = (
        monthly_analysis["order_date_dateorders"]
        .dt.to_period("M")
        .astype(str)
    )

    monthly_analysis = (
        monthly_analysis
        .groupby("month")
        .agg(
            total_records=("delivery_status", "count"),
            late_records=(
                "delivery_status",
                lambda values: (values == "Late delivery").sum()
            )
        )
        .reset_index()
    )

    monthly_analysis["late_rate"] = (
        monthly_analysis["late_records"]
        / monthly_analysis["total_records"]
    ) * 100

    fig_monthly = px.line(
        monthly_analysis,
        x="month",
        y="late_rate",
        markers=True,
        title="Monthly Late Delivery Rate",
        labels={
            "month": "Month",
            "late_rate": "Late Delivery Rate (%)"
        }
    )

    fig_monthly.update_layout(
        template="plotly_dark",
        xaxis_tickangle=-45
    )

    st.plotly_chart(
        fig_monthly,
        use_container_width=True
    )

else:
    st.info("No monthly trend data available.")

st.divider()


# ============================================================
# SECTION 18: SALES BY PRODUCT CATEGORY
# ============================================================

st.header("6. Sales Performance by Product Category")

st.write(
    "Identify the product categories contributing "
    "the highest sales value."
)

sales_category = (
    filtered_df
    .groupby("category_name")
    .agg(
        total_sales=("sales", "sum")
    )
    .reset_index()
    .sort_values(
        "total_sales",
        ascending=False
    )
    .head(10)
)

fig_sales_category = px.bar(
    sales_category,
    x="total_sales",
    y="category_name",
    orientation="h",
    text=sales_category["total_sales"].map(
        lambda value: f"${value:,.0f}"
    ),
    title="Top 10 Product Categories by Sales",
    labels={
        "category_name": "Product Category",
        "total_sales": "Total Sales ($)"
    }
)

fig_sales_category.update_traces(
    textposition="outside"
)

fig_sales_category.update_layout(
    template="plotly_dark",
    yaxis={"categoryorder": "total ascending"}
)

st.plotly_chart(
    fig_sales_category,
    use_container_width=True
)

st.divider()


# ============================================================
# SECTION 19: FINANCIAL EXPOSURE FROM LATE DELIVERIES
# ============================================================

st.header("7. Financial Exposure from Late Deliveries")

st.write(
    "Examine sales and order-item value associated "
    "with late delivery records."
)

late_delivery_df = filtered_df[
    filtered_df["delivery_status"] == "Late delivery"
].copy()

late_sales = late_delivery_df["sales"].sum()

late_item_value = late_delivery_df["order_item_total"].sum()

financial_col1, financial_col2 = st.columns(2)

with financial_col1:
    st.metric(
        "Sales Associated with Late Records",
        f"${late_sales:,.2f}"
    )

with financial_col2:
    st.metric(
        "Order Item Value Associated with Late Records",
        f"${late_item_value:,.2f}"
    )

st.caption(
    "These figures represent sales and order-item value associated "
    "with late delivery records. They are not confirmed financial losses."
)

st.divider()


# ============================================================
# SECTION 20: MARKET-WISE DELIVERY PERFORMANCE
# ============================================================

st.header("8. Market-Wise Delivery Performance")

st.write(
    "Compare late delivery rates across different global markets."
)

if not filtered_delivery.empty:

    market_analysis = (
        filtered_delivery
        .groupby("market")
        .agg(
            total_records=("delivery_status", "count"),
            late_records=(
                "delivery_status",
                lambda values: (values == "Late delivery").sum()
            )
        )
        .reset_index()
    )

    market_analysis["late_rate"] = (
        market_analysis["late_records"]
        / market_analysis["total_records"]
    ) * 100

    market_analysis = market_analysis.sort_values(
        "late_rate",
        ascending=False
    )

    fig_market = px.bar(
        market_analysis,
        x="market",
        y="late_rate",
        text=market_analysis["late_rate"].map(
            lambda value: f"{value:.2f}%"
        ),
        title="Late Delivery Rate by Market",
        labels={
            "market": "Market",
            "late_rate": "Late Delivery Rate (%)"
        }
    )

    fig_market.update_traces(
        textposition="outside"
    )

    fig_market.update_layout(
        template="plotly_dark",
        yaxis_range=[
            0,
            min(110, max(105, market_analysis["late_rate"].max() + 10))
        ]
    )

    st.plotly_chart(
        fig_market,
        use_container_width=True
    )

else:
    st.info("No market delivery data available.")

st.divider()


# ============================================================
# SECTION 21: DETAILED ORDER-ITEM DATA
# ============================================================

st.header("9. Detailed Order-Item Records")

st.write(
    "Explore records matching your selected dashboard filters."
)

st.dataframe(
    filtered_df.head(1000),
    use_container_width=True,
    hide_index=True
)

st.caption(
    f"Showing up to 1,000 records out of "
    f"{len(filtered_df):,} matching records."
)


# ============================================================
# SECTION 22: DOWNLOAD FILTERED DATA
# ============================================================

csv_data = filtered_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="📥 Download Filtered Data as CSV",
    data=csv_data,
    file_name="filtered_supply_chain_data.csv",
    mime="text/csv"
)


# ============================================================
# SECTION 23: FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    <div style="text-align: center;">

    **SupplyChain Insights**

    Data Analytics Project | Python | SQL | Streamlit | Plotly

    Data Source: DataCo Smart Supply Chain Dataset

    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
#  Interactive Sales & Supply Chain Dashboard
#  Built with Streamlit + Plotly Express + Pandas
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px

# -- Page Configuration ----------------------------------------
st.set_page_config(
    page_title="Superstore Sales Dashboard",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -- Custom CSS for a polished, premium look --------------------
st.markdown(
    """
    <style>
    /* ── Google Font ────────────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Inter', sans-serif; }

    /* ── Hide default Streamlit chrome ──────────────────── */
    #MainMenu, footer, header { visibility: hidden; }

    /* ── KPI card styling ──────────────────────────────── */
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #1e1e2f 0%, #2b2b40 100%);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 14px;
        padding: 20px 24px;
        box-shadow: 0 4px 24px rgba(0,0,0,0.25);
    }
    div[data-testid="stMetric"] label {
        color: #a0a0c0 !important;
        font-weight: 500;
        font-size: 0.82rem;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #f0f0ff !important;
        font-weight: 700;
        font-size: 1.65rem;
    }

    /* ── Sidebar styling ───────────────────────────────── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #12121f 0%, #1a1a2e 100%);
    }
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: #c0c0e0;
    }

    /* ── Chart container subtle card ───────────────────── */
    div[data-testid="stPlotlyChart"] {
        border-radius: 12px;
        overflow: hidden;
    }

    /* ── Dividers ──────────────────────────────────────── */
    hr { border-color: rgba(255,255,255,0.06) !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# -- Plotly theme defaults -------------------------------------
PLOTLY_LAYOUT = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color="#c0c0e0"),
    margin=dict(l=40, r=20, t=50, b=40),
)
COLOR_SEQUENCE = ["#6C63FF", "#FF6584", "#43E8D8", "#FFD66B", "#A78BFA",
                  "#F87171", "#34D399", "#60A5FA", "#FBBF24", "#C084FC"]


# =============================================================
#  DATA LOADING
# =============================================================
@st.cache_data
def load_data():
    """Load and lightly prepare the cleaned Superstore dataset."""
    df = pd.read_csv("cleaned_superstore.csv", parse_dates=["Order Date", "Ship Date"])
    return df


df_raw = load_data()

# =============================================================
#  SIDEBAR FILTERS
# =============================================================
st.sidebar.markdown("## :mag: Filters")
st.sidebar.markdown("Use the controls below to slice the data by **date range** and **region**.")

# ── Date range ──
min_date = df_raw["Order Date"].min().date()
max_date = df_raw["Order Date"].max().date()

date_range = st.sidebar.date_input(
    "Order Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

# Guard: if user has only picked a start date, wait for end date
if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

# ── Region multiselect ──
all_regions = sorted(df_raw["Region"].unique())
selected_regions = st.sidebar.multiselect(
    "Region",
    options=all_regions,
    default=all_regions,
)

# ── Apply filters ──
mask = (
    (df_raw["Order Date"].dt.date >= start_date)
    & (df_raw["Order Date"].dt.date <= end_date)
    & (df_raw["Region"].isin(selected_regions))
)
df = df_raw.loc[mask].copy()


# =============================================================
#  EMPTY-STATE GUARD
# =============================================================
st.markdown("# :bar_chart: Superstore Sales Dashboard")

if df.empty:
    st.warning("No data matches the current filters. Adjust the sidebar selections to explore the dataset.")
    st.stop()

st.caption(f"Showing **{len(df):,}** of {len(df_raw):,} records  |  "
           f"{start_date.strftime('%b %d, %Y')} - {end_date.strftime('%b %d, %Y')}")

# =============================================================
#  KPI METRICS
# =============================================================
st.markdown(
    "> **Key Performance Indicators** -- These top-level metrics give leadership "
    "a quick pulse-check on revenue volume, order count, average deal size, and "
    "fulfilment speed."
)

total_sales = df["Sales"].sum()
total_orders = df["Order ID"].nunique()
avg_order_value = total_sales / total_orders if total_orders else 0
avg_ship_days = df["Shipping_Time_Days"].mean()

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Sales", f"${total_sales:,.2f}")
k2.metric("Total Orders", f"{total_orders:,}")
k3.metric("Avg Order Value", f"${avg_order_value:,.2f}")
k4.metric("Avg Shipping Time", f"{avg_ship_days:.1f} days")

st.divider()

# =============================================================
#  CHART 1 — Monthly Sales Trend
# =============================================================
st.markdown("### Monthly Sales Trend")
st.markdown(
    "> Tracking revenue over time reveals **seasonality** and **growth momentum**, "
    "helping the business plan inventory and marketing spend around demand peaks."
)

monthly = (
    df.assign(Month=df["Order Date"].dt.to_period("M").dt.to_timestamp())
    .groupby("Month", as_index=False)["Sales"]
    .sum()
)

fig_trend = px.area(
    monthly,
    x="Month",
    y="Sales",
    labels={"Sales": "Revenue ($)", "Month": ""},
    color_discrete_sequence=["#6C63FF"],
)
fig_trend.update_layout(**PLOTLY_LAYOUT, title="")
fig_trend.update_traces(
    line=dict(width=2.5),
    fillcolor="rgba(108,99,255,0.15)",
    hovertemplate="<b>%{x|%b %Y}</b><br>Revenue: $%{y:,.0f}<extra></extra>",
)
st.plotly_chart(fig_trend, use_container_width=True)

st.divider()

# =============================================================
#  CHART 2 & 3 — Side-by-side
# =============================================================
col_left, col_right = st.columns(2)

# ── Chart 2: Sales by Sub-Category ──
with col_left:
    st.markdown("### Sales by Sub-Category")
    st.markdown(
        "> Identifies the **highest-** and **lowest-revenue product lines**. "
        "Sub-categories at the bottom may warrant promotion, bundling, or discontinuation."
    )

    sub_sales = (
        df.groupby("Sub-Category", as_index=False)["Sales"]
        .sum()
        .sort_values("Sales", ascending=True)
    )

    fig_sub = px.bar(
        sub_sales,
        x="Sales",
        y="Sub-Category",
        orientation="h",
        labels={"Sales": "Revenue ($)", "Sub-Category": ""},
        color="Sales",
        color_continuous_scale=["#FF6584", "#FFD66B", "#43E8D8", "#6C63FF"],
    )
    fig_sub.update_layout(**PLOTLY_LAYOUT, title="", coloraxis_showscale=False)
    fig_sub.update_traces(
        hovertemplate="<b>%{y}</b><br>Revenue: $%{x:,.0f}<extra></extra>"
    )
    st.plotly_chart(fig_sub, use_container_width=True)

# ── Chart 3: Shipping Time by Ship Mode ──
with col_right:
    st.markdown("### Shipping Time by Ship Mode")
    st.markdown(
        "> Compares fulfilment speed across carriers. A box-plot reveals the "
        "**median, spread, and outliers** -- useful for SLA monitoring and "
        "identifying modes that consistently underperform."
    )

    fig_ship = px.box(
        df,
        x="Ship Mode",
        y="Shipping_Time_Days",
        color="Ship Mode",
        labels={"Shipping_Time_Days": "Days to Ship", "Ship Mode": ""},
        color_discrete_sequence=COLOR_SEQUENCE,
    )
    fig_ship.update_layout(**PLOTLY_LAYOUT, title="", showlegend=False)
    st.plotly_chart(fig_ship, use_container_width=True)

st.divider()

# =============================================================
#  FOOTER
# =============================================================
st.markdown(
    "<div style='text-align:center; color:#555; font-size:0.78rem; padding:12px 0;'>"
    "Superstore Sales Dashboard &middot; Built with Streamlit &amp; Plotly"
    "</div>",
    unsafe_allow_html=True,
)

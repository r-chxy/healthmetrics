import streamlit as st
import pandas as pd

# ----------------------------------------------------------
# CONFIG
# ----------------------------------------------------------
st.set_page_config(
    page_title="Chexy – Growth & Activation Dashboard",
    layout="wide",
    page_icon="📈"
)

# Your Google Sheet (CSV Export)
CSV_URL = "https://docs.google.com/spreadsheets/d/1V9ymJKvgccVr6z_EvLBx7XBoSVnGgrw8xIVnS_uex5Y/export?format=csv&gid=1997349262"


# ----------------------------------------------------------
# LOAD DATA
# ----------------------------------------------------------
@st.cache_data(ttl=300)
def load_data():
    df = pd.read_csv(CSV_URL)
    return df

df = load_data()

st.title("📈 Chexy – Active Users, New Accounts & Activations Dashboard")
st.caption("Data Source: Google Sheets → BigQuery Connected Query")

# Segment selection
segment = st.sidebar.selectbox("User Segment", df["segment"].unique())
row = df[df["segment"] == segment].iloc[0]


# ----------------------------------------------------------
# KPI FUNCTION
# ----------------------------------------------------------
def metric_card(title, value, abs_change, pct_change):
    delta_text = None
    if pct_change is not None and not pd.isna(pct_change):
        delta_text = f"{abs_change:+} ({pct_change:.1f}%)"
    st.metric(title, value, delta_text)


# ----------------------------------------------------------
# ACTIVE USERS (30 / 60 / 90)
# ----------------------------------------------------------
st.subheader("👥 Active Users (Rolling Windows)")

col1, col2, col3 = st.columns(3)
with col1:
    metric_card(
        "Active Users (30d)",
        row["active_users_30d"],
        row["active_users_30d_abs_change"],
        row["active_users_30d_pct_change"]
    )
with col2:
    metric_card(
        "Active Users (60d)",
        row["active_users_60d"],
        row["active_users_60d_abs_change"],
        row["active_users_60d_pct_change"]
    )
with col3:
    metric_card(
        "Active Users (90d)",
        row["active_users_90d"],
        row["active_users_90d_abs_change"],
        row["active_users_90d_pct_change"]
    )


# ----------------------------------------------------------
# NEW ACCOUNTS
# ----------------------------------------------------------
st.subheader("🆕 New Accounts")

col4, col5, col6 = st.columns(3)
with col4:
    metric_card(
        "New Accounts (Today)",
        row["new_accounts_today"],
        row["new_accounts_today_abs_change"],
        row["new_accounts_today_pct_change"]
    )

with col5:
    metric_card(
        "New Accounts (WTD – 7 Days)",
        row["new_accounts_wtd"],
        row["new_accounts_wtd_abs_change"],
        row["new_accounts_wtd_pct_change"]
    )

with col6:
    metric_card(
        "New Accounts (MTD – 30 Days)",
        row["new_accounts_mtd"],
        row["new_accounts_mtd_abs_change"],
        row["new_accounts_mtd_pct_change"]
    )


# ----------------------------------------------------------
# NEW ACTIVATIONS
# ----------------------------------------------------------
st.subheader("🚀 New Activations")

col7, col8, col9 = st.columns(3)

with col7:
    metric_card(
        "Activations (Today)",
        row["activations_today"],
        row["activations_today_abs_change"],
        row["activations_today_pct_change"]
    )

with col8:
    metric_card(
        "Activations (WTD – 7 Days)",
        row["activations_wtd"],
        row["activations_wtd_abs_change"],
        row["activations_wtd_pct_change"]
    )

with col9:
    metric_card(
        "Activations (MTD – 30 Days)",
        row["activations_mtd"],
        row["activations_mtd_abs_change"],
        row["activations_mtd_pct_change"]
    )


# ----------------------------------------------------------
# RAW TABLE
# ----------------------------------------------------------
st.subheader("📄 Raw KPI Data (Filtered)")
st.dataframe(df[df["segment"] == segment])

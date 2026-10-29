import streamlit as st
import pandas as pd
def kpi_card(col, label, value):
    """Render one KPI card using the classes from style.css."""
    col.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def footer():
    st.caption("🚀 Mytra sales analysis | built by Isha")

def get_clean_df():
    """Use cleaned data from the previous step, or let the user upload a clean CSV."""
    if "clean_df" in st.session_state:
        source = st.radio(
            "Data source",
            ["Use data cleaned in the previous step", "Upload a clean CSV"],
            horizontal=True,
        )
        if source.startswith("Use"):
            return st.session_state["clean_df"]

    uploaded = st.file_uploader("Upload a clean CSV", type=["csv"], key="eda_upload")
    return pd.read_csv(uploaded) if uploaded else None

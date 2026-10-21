import streamlit as st

def kpi_card(column, label, value):
    column.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
        </div>
    """, unsafe_allow_html=True)

def footer():
    st.divider()
    st.caption("🚀 wallmart analysis | Built by Isha")
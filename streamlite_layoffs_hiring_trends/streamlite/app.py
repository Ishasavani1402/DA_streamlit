import pandas as pd
import streamlit as st
from csv_to_mysql import create_connection
# import queries
from pathlib import Path 


# page configuration
st.set_page_config(page_title='Tech Layoff Hiring Trends' , layout='wide' , page_icon='💻')

def load_css(file_name):
    css_path = Path(__file__).parent / file_name
    with open(css_path, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def kpi_card(column, label, value):
    column.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
        </div>
    """, unsafe_allow_html=True)


load_css("style.css")

# # head part
st.markdown("""
<h2 style="margin-bottom:0;">💻 Tech Layoff Hiring Trends</h2>
<p style="color:gray; margin-top:0; margin-bottom:10px;">
</p>
""", unsafe_allow_html=True)

with st.sidebar:
    st.sidebar.title("📌 Navigation")
    menu = st.radio(
        'Select Analysis',
        options=[
            'Overview',
            'medical condition',
            'insurance provider',
            'doctor analysis',
            'hospital analysis',
            'seasonal analysis',
        ],
        index=0
    )

# get connection
conn = create_connection()
import streamlit as st
from pathlib import Path
import pandas as pd
from streamlit_.data_clean.data_clean import render_data_cleaning

# Page configuration
st.set_page_config(
    page_title="Mytra Sales Analysis",
    layout="wide",
    page_icon="🛒"
)

# Load CSS
def load_css(file_name):
    css_path = Path(__file__).parent / file_name

    with open(css_path, encoding="utf-8") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

load_css("streamlit_/style.css")

# Header
st.markdown("""
<h2 style="margin-bottom:0;">🛒 Mytra Sales Analysis</h2>
<p style="color:gray; margin-top:0; margin-bottom:10px;"></p>
""", unsafe_allow_html=True)


icons = {
    "Data Cleaning": "🧹 Data Cleaning",
}

with st.sidebar:
    st.sidebar.title("📌 Navigation")
    menu = st.radio(
        "Select Analysis",
        options=list(icons.keys()),
        format_func=lambda x: icons[x],
        index=0
    )

if menu == 'Data Cleaning':
    render_data_cleaning()
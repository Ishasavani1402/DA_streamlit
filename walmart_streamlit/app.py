import streamlit as st
from pathlib import Path 
# from streamlite import navigation

# page configuration
st.set_page_config(page_title="Wallmart Analysis" , layout="wide" , page_icon="🛒")

def load_css(file_name):
    css_path = Path(__file__).parent / file_name
    with open(css_path, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css("streamlit\\style.css")

# header
st.markdown("""
<h2 style="margin-bottom:0;">🛒 Wallmart Analysis</h2>
<p style="color:gray; margin-top:0; margin-bottom:10px;">
</p>
""", unsafe_allow_html=True)
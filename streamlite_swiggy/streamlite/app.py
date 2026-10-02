import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import navigation
from pathlib import Path

# page configuration
st.set_page_config(page_title='Swiggy analysis' , layout='wide')

# CSS
def load_css(file_name):
    css_path = Path(__file__).parent / file_name
    with open(css_path, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css("style.css")

# head part
st.markdown("""
<h2 style="margin-bottom:0;">📊 Swiggy Analysis System</h2>
<p style="color:gray; margin-top:0; margin-bottom:10px;">
</p>
""", unsafe_allow_html=True)

icons = {
    "Overview": "🔍 Overview",
    "City Analysis": "🏙️ City Analysis",
    "Restuarant Analysis": "🍽 Restuarant Analysis"

}
with st.sidebar:
    uploaded_file = st.file_uploader("Upload Sales CSV File", type=["csv"])
    st.sidebar.title("📌 Navigation")
    menu = st.radio(
        "Select Analysis",
        options=list(icons.keys()),
        format_func=lambda x: icons[x],
        index=0
    )


 
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    if menu == 'Overview':
        navigation.overview(df)
    elif menu == 'City Analysis':
        navigation.city_analysis(df)
    elif menu == 'Restuarant Analysis':
        navigation.restuarant_analysis(df)

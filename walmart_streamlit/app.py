import streamlit as st
from pathlib import Path 
from  streamlite.overview import overview
from streamlite.sales_analysis import sales_analysis
from streamlite.customer_type import custtomer_type
from streamlite.time_series_analysis import monthly_sale
# page configuration
st.set_page_config(page_title="Wallmart Analysis" , layout="wide" , page_icon="🛒")

def load_css(file_name):
    css_path = Path(__file__).parent / file_name
    with open(css_path, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css("streamlite\\style.css")

# header
st.markdown("""
<h2 style="margin-bottom:0;">🛒 Wallmart Analysis</h2>
<p style="color:gray; margin-top:0; margin-bottom:10px;">
</p>
""", unsafe_allow_html=True)



icons = {
    "Overview": "🔍 Overview",
    "sales analysis" : "📊 Sales Analysis",
    "customer type distribuution" : "👥 Customer Type Distribution",
    "time series analysis" : "📈 Time Series Analysis",

}

with st.sidebar:
    st.sidebar.title("📌 Navigation")
    menu = st.radio(
        "Select Analysis",
        options=list(icons.keys()),
        format_func=lambda x: icons[x],
        index=0
    )

if menu == "Overview":
    overview()
elif menu == "sales analysis":
    sales_analysis()
elif menu == "customer type distribuution":
    custtomer_type()
elif menu == 'time series analysis':
    monthly_sale()
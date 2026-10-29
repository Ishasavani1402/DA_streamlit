import streamlit as st
from pathlib import Path
from streamlit_.data_clean.data_clean import render_data_cleaning
from streamlit_.EDA.EDA import render_eda   
from streamlit_.EDA.sales_analysis import render_sales_analysis
from streamlit_.EDA.AOV import render_aov
from streamlit_.EDA.order_analysis import render_orders
from streamlit_.EDA.customer_analysis import render_customer_analysis
from streamlit_.EDA.product_analysis import render_product_analysis
from streamlit_.EDA.custome_analysis import render_custom_analysis
# Page configuration
st.set_page_config(
    page_title="Myntra Sales Analysis",
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
<h2 style="margin-bottom:0;">🛒 Myntra Sales Analysis</h2>
<p style="color:gray; margin-top:0; margin-bottom:10px;"></p>
""", unsafe_allow_html=True)


icons = {
    "Data Cleaning": "🧹 Data Cleaning",
    "EDA": "📊 Exploratory Data Analysis",
    "Sales Forecasting": "📈 Sales Forecasting",
    "AOV" : "💰 Average Order Value",
    "Order Analysis" : "🛍️ Order Analysis",
    "customer Analysis" : "👥 Customer Analysis",
    "product Analysis" : "📦 Product Analysis" , 
    "Custom Analysis" : "🧪 Custom Python Analysis",
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
elif menu == 'EDA':
    render_eda()
elif menu == 'Sales Forecasting':
    render_sales_analysis()
elif menu == 'AOV':
    render_aov()
elif menu == 'Order Analysis':
    render_orders()
elif menu == 'customer Analysis':
    render_customer_analysis()
elif menu == 'product Analysis':
    render_product_analysis()
elif menu == 'Custom Analysis':
    render_custom_analysis()
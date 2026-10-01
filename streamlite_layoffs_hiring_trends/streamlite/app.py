import streamlit as st
from pathlib import Path 
import navigation

# page configuration
st.set_page_config(page_title="Tech Layoff Hiring Trends" , layout="wide" , page_icon="💻")

def load_css(file_name):
    css_path = Path(__file__).parent / file_name
    with open(css_path, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css("style.css")

# # head part
st.markdown("""
<h2 style="margin-bottom:0;">💻 Tech Layoff Hiring Trends</h2>
<p style="color:gray; margin-top:0; margin-bottom:10px;">
</p>
""", unsafe_allow_html=True)

icons = {
    "Overview": "🔍 Overview",
    "Yearly Layoff Trend": "📉 Yearly Layoff Trend",
    "Country Analysis": "🌍 Country Analysis",
    "Company Analysis": "🏢 Company Analysis",
    "Industry Analysis": "🏭 Industry Analysis",
    "Hiring Trend Analysis": "🤝 Hiring Trend Analysis",
    "Hiring Role Analysis": "💻 Hiring Role Analysis" , 
    "Market Condition Analysis": "📊 Market Condition Analysis"

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
    navigation.overview()

elif menu == 'Country Analysis':
    navigation.country_analysis()

elif menu =='Yearly Layoff Trend':
    navigation.yearly_layoff()

elif menu == 'Company Analysis':
    navigation.company_analysis()

elif menu == 'Industry Analysis':
    navigation.industry_analysis()

elif menu == 'Hiring Trend Analysis':
    navigation.hiring_trend_analysis()

elif menu == 'Hiring Role Analysis':
    navigation.hiring_role_analysis()

elif menu =='Market Condition Analysis':
    navigation.market_condition_analysis()

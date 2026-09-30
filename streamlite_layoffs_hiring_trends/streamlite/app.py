import pandas as pd
import streamlit as st
from csv_to_mysql import create_connection
import queries
from pathlib import Path 


# page configuration
st.set_page_config(page_title="Tech Layoff Hiring Trends" , layout="wide" , page_icon="💻")

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

# get connection
conn = create_connection()

if menu == "Overview":
    st.header("📌 Key Business Metrics")

    overall_layoff = pd.read_sql_query(queries.overall_layoff_kpi , conn)
    layoff_pct = pd.read_sql_query(queries.layoff_pct_kpi , conn)
    total_company = pd.read_sql_query(queries.total_company_kpi , conn)
    total_industry = pd.read_sql_query(queries.total_industry_kpi , conn)

    k1,k2,k3 , k4 = st.columns(4)
    kpi_card(k1, "Overall Layoff", f"{int(overall_layoff.iloc[0,0]):,}")
    kpi_card(k2, "Overall Layoff (%)", f"{float(layoff_pct.iloc[0,0]):,} %")
    kpi_card(k3, "total company", f"{int(total_company.iloc[0,0]):,}")
    kpi_card(k4, "total industry", f"{int(total_industry.iloc[0,0]):,}")

    st.divider()
    
    st.subheader('AI adoption vs layoffs')
    df = pd.read_sql_query(queries.ai_adoption_vs_layoff , conn)
    st.dataframe(df)
    st.bar_chart(df , x='ai_adoption_bucket' , y='avg_layoff')

    st.divider()
    st.caption("🚀 Tech Layoff Hiring Trend system | Built by Isha")

elif menu == 'Country Analysis':
    st.subheader('country wise layoff distribution')
    df = pd.read_sql_query(queries.country_layoff , conn)
    st.dataframe(df)
    st.bar_chart(df , x='country' , y='total_layoff')

    st.divider()
    st.caption("🚀 Tech Layoff Hiring Trend system | Built by Isha")

elif menu =='Yearly Layoff Trend':
    st.subheader("1 . yearly layoff distribution"  , text_alignment='left')
    df = pd.read_sql_query(queries.yearly_layoff , conn)
    st.dataframe(df)
    st.line_chart(df , x='year' , y='total_layoff' , use_container_width=True)
    
    st.divider()

    st.subheader("2 . For each year, what percentage of a company's Moderate and Aggressive Hiring activity belongs to that company?"  , text_alignment='left')
    df = pd.read_sql_query(queries.yerly_hiring_pct_for_cmpny , conn)
    st.dataframe(df)

    st.divider()
        
    st.subheader('3 . in each year which company have higest layoff??')
    df = pd.read_sql_query(queries.yearly_company_layoff , conn)
    st.dataframe(df)

    st.divider()
    st.caption("🚀 Tech Layoff Hiring Trend system | Built by Isha")

elif menu == 'Company Analysis':
    st.subheader('1 . company wise layoff') 
    df = pd.read_sql_query(queries.company_layoff , conn)
    st.dataframe(df)
    st.bar_chart(df, x='company_name', y='total_layoff', horizontal=True)

    st.divider()
        
    st.subheader('2 .  in each company which hiring role have higest open role??')
    df = pd.read_sql_query(queries.yearly_company_open_roles , conn)
    st.dataframe(df)

    # Prepare data for chart
    chart_data = df.pivot(
    index='company_name',
    columns='top_hiring_role',
    values='total_open_role'
    ).fillna(0)
    st.bar_chart(chart_data , horizontal=True)

    st.divider()


    st.subheader('3 . company size layoff') 
    df = pd.read_sql_query(queries.company_size_layoff , conn)
    st.dataframe(df)
    st.bar_chart(df, x='company_size', y='total_layoff')
    

    st.divider()
    st.caption("🚀 Tech Layoff Hiring Trend system | Built by Isha")

elif menu == 'Industry Analysis':
    st.subheader('1 . industry layoff')
    df = pd.read_sql_query(queries.industry_layoff , conn)
    st.dataframe(df)
    st.bar_chart(df , x='industry' , y='total_layoff')

    st.divider()

    st.subheader('2 . in each industry which is common reason for layoff ??')
    df = pd.read_sql_query(queries.industry_common_reason_layoff , conn)
    st.dataframe(df)
      # Prepare data for chart
    chart_data = df.pivot(
    index='industry',
    columns='reason_for_layoffs',
    values='layoff_record'
    ).fillna(0)
    st.bar_chart(chart_data, use_container_width=True)

    st.divider()
    st.caption('🚀 Tech Layoff Hiring Trend system | Built by Isha')

elif menu == 'Hiring Trend Analysis':
    st.subheader('1 . hiring trend analysis moderate vs aggresive')
    df = pd.read_sql_query(queries.hiring_trend_analysis , conn)
    st.dataframe(df)
    st.bar_chart(df , x='hiring_trend' , y='avg_open_role')

    st.divider()
    st.caption('🚀 Tech Layoff Hiring Trend system | Built by Isha')

elif menu == 'Hiring Role Analysis':
    st.subheader('1 . hiring role analysis by open roles')
    df = pd.read_sql_query(queries.hiring_role_analysis , conn)
    st.dataframe(df)
    st.bar_chart(df , x='top_hiring_role' , y='total_open_role')

    st.divider()
    st.caption('🚀 Tech Layoff Hiring Trend system | Built by Isha')

elif menu =='Market Condition Analysis':
    st.subheader('1 . market condition wise layoff')
    df = pd.read_sql_query(queries.market_condition_layoff , conn)
    st.dataframe(df)
    st.bar_chart(df , x='market_condition' , y='total_layoff')

    st.divider()
    st.subheader('2 . market condition vs hiring trend analysis')
    df = pd.read_sql_query(queries.market_condition_hiring_trend , conn)
    st.dataframe(df)
   # Prepare data for chart
    chart_data = df.pivot(
    index='market_condition',
    columns='hiring_trend',
    values='total_open_role'
    ).fillna(0)

    st.bar_chart(chart_data, use_container_width=True)

    st.divider()
    st.caption('🚀 Tech Layoff Hiring Trend system | Built by Isha')

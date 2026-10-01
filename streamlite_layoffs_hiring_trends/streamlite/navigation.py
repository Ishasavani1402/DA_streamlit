import streamlit as st
from db import run
import queries
import plotly.express as px

def kpi_card(column, label, value):
    column.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
        </div>
    """, unsafe_allow_html=True)

def footer():
    st.divider()
    st.caption("🚀 Tech Layoff Hiring Trend system | Built by Isha")

def overview():
    st.header("📌 Key Business Metrics")
    
    overall_layoff = run(queries.overall_layoff_kpi)
    layoff_pct = run(queries.layoff_pct_kpi)
    total_company = run(queries.total_company_kpi)
    total_industry = run(queries.total_industry_kpi)

    k1,k2,k3 , k4 = st.columns(4)
    kpi_card(k1, "Overall Layoff", f"{int(overall_layoff.iloc[0,0]):,}")
    kpi_card(k2, "Overall Layoff (%)", f"{float(layoff_pct.iloc[0,0]):,} %")
    kpi_card(k3, "total company", f"{int(total_company.iloc[0,0]):,}")
    kpi_card(k4, "total industry", f"{int(total_industry.iloc[0,0]):,}")

    st.divider()
    
    st.subheader('AI adoption vs layoffs')
    df = run(queries.ai_adoption_vs_layoff)
    st.dataframe(df)
    fig = px.bar(df.sort_values("avg_layoff" , ascending=False), x="ai_adoption_bucket", y="avg_layoff", orientation="v")
    st.plotly_chart(fig, use_container_width=True)

    footer()

def country_analysis():
    st.subheader('country wise layoff distribution')
    df = run(queries.country_layoff )
    st.dataframe(df)
    fig = px.bar(df.sort_values("total_layoff" , ascending=False), x="country", y="total_layoff", orientation="v")
    st.plotly_chart(fig)

    footer()

def yearly_layoff():
    st.subheader("1 . yearly layoff distribution"  , text_alignment='left')
    df = run(queries.yearly_layoff)
    st.dataframe(df)
    st.line_chart(df , x='year' , y='total_layoff')
    
    st.divider()

    st.subheader("2 . For each year, what percentage of a company's Moderate and Aggressive Hiring activity belongs to that company?"  , text_alignment='left')
    df = run(queries.yerly_hiring_pct_for_cmpny , )
    st.dataframe(df)

    st.divider()
        
    st.subheader('3 . in each year which company have higest layoff??')
    df = run(queries.yearly_company_layoff , )
    st.dataframe(df)

    footer()

def company_analysis():
    st.subheader('1 . company wise layoff') 
    df = run(queries.company_layoff)
    st.dataframe(df)
    fig = px.bar(df.sort_values("total_layoff"), x="total_layoff", y="company_name", orientation="h")
    st.plotly_chart(fig)

    st.divider()
        
    st.subheader('2 .  in each company which hiring role have higest open role??')
    df = run(queries.yearly_company_open_roles , )
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
    df = run(queries.company_size_layoff , )
    st.dataframe(df)
    fig = px.bar(df.sort_values("total_layoff" , ascending=False), x="company_size", y="total_layoff", orientation="v")
    st.plotly_chart(fig)
    # st.bar_chart(df, x='company_size', y='total_layoff')
    

    footer()

def industry_analysis():
    st.subheader('1 . industry layoff')
    df = run(queries.industry_layoff , )
    st.dataframe(df)
    fig = px.bar(df.sort_values("total_layoff" , ascending=False), x="industry", y="total_layoff", orientation="v")
    st.plotly_chart(fig)
    st.divider()

    st.subheader('2 . in each industry which is common reason for layoff ??')
    df = run(queries.industry_common_reason_layoff , )
    st.dataframe(df)
        # Prepare data for chart
    chart_data = df.pivot(
    index='industry',
    columns='reason_for_layoffs',
    values='layoff_record'
    ).fillna(0)
    st.bar_chart(chart_data, )

    footer()


def hiring_trend_analysis():
    st.subheader('1 . hiring trend analysis moderate vs aggresive')
    df = run(queries.hiring_trend_analysis , )
    st.dataframe(df)
    st.bar_chart(df , x='hiring_trend' , y='avg_open_role')

    footer()

def hiring_role_analysis():
    st.subheader('1 . hiring role analysis by open roles')
    df = run(queries.hiring_role_analysis , )
    st.dataframe(df)
    fig = px.bar(df.sort_values("total_open_role" , ascending=False), x="top_hiring_role", y="total_open_role", orientation="v")
    st.plotly_chart(fig)

    footer()

def market_condition_analysis():
    st.subheader('1 . market condition wise layoff')
    df = run(queries.market_condition_layoff , )
    st.dataframe(df)
    fig = px.bar(df.sort_values("total_layoff" , ascending=False), x="market_condition", y="total_layoff", orientation="v")
    st.plotly_chart(fig)

    st.divider()

    st.subheader('2 . market condition vs hiring trend analysis')
    df = run(queries.market_condition_hiring_trend , )
    st.dataframe(df)
    # Prepare data for chart
    chart_data = df.pivot(
    index='market_condition',
    columns='hiring_trend',
    values='total_open_role'
    ).fillna(0)

    st.bar_chart(chart_data, )

    footer()
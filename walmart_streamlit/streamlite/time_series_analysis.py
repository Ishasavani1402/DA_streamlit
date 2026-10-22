import streamlit as st
from db import run
from . import queries
from .helpers import footer
from plotly import express as px

def monthly_sale():
    st.subheader("1 . monthly sales analysis")
    monthly_sale = run(queries.monthly_sales)
    st.dataframe(monthly_sale)
    fig = px.line(monthly_sale,
                  x='month_no',
                  y='total_sale',
                  markers=True,
                  title="Monthly Sales Analysis",
                  labels={
                      "month_no": "Month Number",
                      "total_sale": "Total Sales"
                  })
    fig.update_layout(
        xaxis_title="Month Number",
        yaxis_title="Total Sales",
        template="plotly_white"
    )
    st.plotly_chart(fig)

    st.divider()
    st.subheader('2 . time of day wise sales')
    time_of_day = run(queries.time_of_day)
    st.dataframe(time_of_day)
    fig = px.bar(time_of_day,
            x="time_of_day",
            y='total_sale',
            title="time of day wise sale",
            text_auto=True
        )
    st.plotly_chart(fig)

    footer()




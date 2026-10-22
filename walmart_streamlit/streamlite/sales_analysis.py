import streamlit as st
from db import run
from . import queries
from .helpers import footer
from plotly import express as px

def sales_analysis():
    st.subheader("1 . 📊 Category-wise Total Sales")

    category_sale = run(queries.category_sale)

    st.dataframe(category_sale)

    # Pie chart showing percentage of total sales
    fig = px.pie(
        category_sale,
        names="product_category",
        values="total_sale",
        title="Percentage of Total Sales by Category",
        hole=0.4
    )

    fig.update_traces(
        textinfo="label+percent",
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Total Sales: %{value:,.2f}<br>"
            "Share of Sales: %{percent}"
            "<extra></extra>"
        )
    )

    fig.update_layout(
        title_x=0.5,
        legend_title="Product Category"
    )

    st.plotly_chart(fig)

    st.divider()

    st.subheader('2 . product line wise total sale')
    product_line = run(queries.product_line_sale)
    st.dataframe(product_line)
    fig = px.bar(product_line,
                 x='product_line',
                 y='total_sale')
    st.plotly_chart(fig)

    st.divider()
    st.subheader('3 . total sale by products')
    product_sale = run(queries.product_sale)
    st.dataframe(product_sale)
    fig = px.bar(product_sale.sort_values('total_sale'),
                     x='total_sale',
                     y='product_name',
                     orientation='h',
                     barmode='relative')
    st.plotly_chart(fig)

    st.divider()
    st.subheader('4 . total sale by city')
    city_sale = run(queries.city_sale)
    st.dataframe(city_sale)
    fig = px.bar(city_sale,
                        x='city',
                        y='total_sale',
                        barmode='relative')
    st.plotly_chart(fig)

    footer()
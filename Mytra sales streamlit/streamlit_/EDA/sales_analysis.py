import streamlit as st
import plotly.express as px
from streamlit_.helper import footer
from streamlit_.helper import get_clean_df

def category_revenue(df):
    st.subheader("1 . Revenue by Category")

    result = (
        df.groupby("category", as_index=False)
          .agg(total_revenue=("total_amount", "sum"))
          .sort_values(by="total_revenue", ascending=False)
    )
    st.dataframe(result)
    fig = px.bar(
        result,
        x="category",
        y="total_revenue",
        title="Total Revenue by Category",
        labels={"category": "Category", "total_revenue": "Total Revenue"},
        text_auto=True,
    )
    fig.update_layout(xaxis_title="Category", yaxis_title="Total Revenue")
    st.plotly_chart(fig)
    st.divider()

def brand_revenue(df):
    st.subheader("2 . Revenue by Brand")
    
    result = (
        df.groupby("brand", as_index=False)
            .agg(total_revenue=("total_amount", "sum"))
            .sort_values(by="total_revenue", ascending=False)
            .head(10)
    )
    st.dataframe(result)
    fig = px.bar(
        result,
        x="total_revenue",
        y="brand",
        orientation="h",
        title="Top 10 Brands by Revenue",
        labels={"brand": "Brand", "total_revenue": "Total Revenue"},
        text_auto=True,
    )
    fig.update_layout(xaxis_title="Total Revenue", yaxis_title="Brand")
    fig.update_yaxes(autorange="reversed")
    st.plotly_chart(fig)
    st.divider()

def state_revenue(df):
    st.subheader("3 . Revenue by State")
    
    result = (
        df.groupby("state", as_index=False)
            .agg(total_revenue=("total_amount", "sum"))
            .sort_values(by="total_revenue", ascending=False)
            .head(10)
    )
    st.dataframe(result)
    fig = px.bar(
        result,
        x="total_revenue",
        y="state",
        orientation="h",
        title="Top 10 state by Revenue",
        labels={"state": "State", "total_revenue": "Total Revenue"},
        text_auto=True,
    )
    fig.update_layout(xaxis_title="Total Revenue", yaxis_title="State")
    fig.update_yaxes(autorange="reversed")
    st.plotly_chart(fig)
    st.divider()

def yerly_sales(df):
    st.subheader('3 . yearly sales trend')
    result = df.groupby('order_year', as_index=False).agg(yearly_sales=('total_amount', 'sum'))
    st.dataframe(result)
    fig = px.line(
        result,
        x='order_year',
        y='yearly_sales',
        title='Yearly Sales Trend',
        labels={'order_year': 'Year', 'yearly_sales': 'Yearly Sales'},
        markers=True
    )
    fig.update_layout(xaxis_title='Year', yaxis_title='Yearly Sales')
    st.plotly_chart(fig)
    st.divider()

def order_chennal_revenue(df):
    st.subheader('4 . revenue by order chennal')
    result = (
            df.groupby("order_channel", as_index=False)
              .agg(total_revenue=("total_amount", "sum"))
              .sort_values(by="total_revenue", ascending=False)
        )
    st.dataframe(result)
    fig = px.bar(
        result,
        x="order_channel",
        y="total_revenue",
        title="Total Revenue by Order Chenal",
        labels={"order_channel": "Order_chenal", "total_revenue": "Total Revenue"},
        text_auto=True,
    )
    fig.update_layout(xaxis_title="Order_Chenal", yaxis_title="Total Revenue")
    st.plotly_chart(fig)
    st.divider()
    









def render_sales_analysis():
    df = get_clean_df()
    if df is None:
        st.warning("upload an already clean CSV.")
        return

    category_revenue(df)
    brand_revenue(df)
    state_revenue(df)
    yerly_sales(df)
    order_chennal_revenue(df)
    footer()
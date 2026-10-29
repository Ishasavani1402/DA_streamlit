import streamlit as st
import plotly.express as px
from streamlit_.helper import footer
from streamlit_.helper import get_clean_df

def payment_mode_customers(df):
    st.subheader('1 . total customer by use of payment mode')
    result = (
            df.groupby("payment_mode", as_index=False)
                .agg(total_customers=("customer_id", "nunique"))
                .sort_values(by="total_customers", ascending=False)
            )
    st.dataframe(result)

    fig = px.bar(
        result,
        x="payment_mode",
        y="total_customers",
        title="Customers by Payment Mode",
        labels={"payment_mode": "Payment Mode", "total_customers": "Total Customers"},
    )
    st.plotly_chart(fig)
    st.divider()

def membership_tier_customers(df):
    st.subheader('2 . total customer by membership tier')
    result = (
            df.groupby("membership_tier", as_index=False)
                .agg(total_customers=("customer_id", "nunique"))
                .sort_values(by="total_customers", ascending=False)
            )
    st.dataframe(result)

    fig = px.bar(
        result,
        x="membership_tier",
        y="total_customers",
        title="Customers by membership_tier",
        labels={"membership_tier": "Membership Tier", "total_customers": "Total Customers"},
    )
    st.plotly_chart(fig)
    st.divider()

def order_chennel_customers(df):
    st.subheader('2 . total customer by order channel')
    result = (
            df.groupby("order_channel", as_index=False)
                .agg(total_customers=("customer_id", "nunique"))
                .sort_values(by="total_customers", ascending=False)
            )
    st.dataframe(result , height='auto')

    fig = px.bar(
        result,
        x="order_channel",
        y="total_customers",
        title="Customers by order chennel",
        labels={"order_channel": "Order Channel", "total_customers": "Total Customers"},
    )
    st.plotly_chart(fig)
    st.divider()

def render_customer_analysis():
    df = get_clean_df()
    if df is None:
        st.warning("upload an already clean CSV.")
        return
    payment_mode_customers(df)
    membership_tier_customers(df)
    order_chennel_customers(df)
    footer()

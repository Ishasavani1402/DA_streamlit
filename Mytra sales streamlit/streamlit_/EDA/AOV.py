import streamlit as st
import plotly.express as px
from streamlit_.helper import footer
from streamlit_.helper import get_clean_df


def category_aov(df):
    st.subheader("1 . Which Category Generates the Highest AOV?")

    result = (
        df.groupby("category")
          .agg(
              total_sale=("total_amount", "sum"),
              total_order=("order_id", "nunique")
          )
          .reset_index()
    )

    result["aov"] = (
        result["total_sale"] / result["total_order"]
    )

    result = result.sort_values(
        by="aov", ascending=False
    )

    # st.dataframe(result)

    # Display the category with the highest AOV
    top_category = result.iloc[0]

    st.success(
        f"Highest AOV Category: {top_category['category']} "
        f"| AOV: {top_category['aov']:.2f}",
        icon=":material/thumb_up:"
    )

    st.divider()


def brand_aov(df):
    st.subheader("2 . Which Brand Generates the Highest AOV?")

    result = (
        df.groupby("brand")
          .agg(
              total_sale=("total_amount", "sum"),
              total_order=("order_id", "nunique")
          )
          .reset_index()
    )

    result["aov"] = (
        result["total_sale"] / result["total_order"]
    )

    result = result.sort_values(
        by="aov", ascending=False
    )

    # st.dataframe(result)

    # Display the category with the highest AOV
    top_brand = result.iloc[0]

    st.success(
        f"Highest AOV Brand: {top_brand['brand']} "
        f"| AOV: {top_brand['aov']:.2f}",
        icon=":material/thumb_up:"
    )

    st.divider()


def payment_mode_aov(df):
    st.subheader("3 . Which payment modes are associated with higher average order values?")

    result = (
        df.groupby("payment_mode")
          .agg(
              total_sale=("total_amount", "sum"),
              total_order=("order_id", "nunique")
          )
          .reset_index()
    )

    result["aov"] = (
        result["total_sale"] / result["total_order"]
    )

    result = result.sort_values(
        by="aov", ascending=False
    )

    # st.dataframe(result)

    # Display the category with the highest AOV
    top_payment_mode = result.iloc[0]

    st.success(
        f"Highest AOV Payment_Mode: {top_payment_mode['payment_mode']} "
        f"| AOV: {top_payment_mode['aov']:.2f}",
        icon=":material/thumb_up:"
    )

    st.divider()

def order_chenal_aov(df):
    st.subheader('4 . Which order channel (Website, Mobile App, Mobile Web) drives highest average order value?')

    result = (
        df.groupby("order_channel")
            .agg(
                total_sale=("total_amount", "sum"),
                total_order=("order_id", "nunique")
            )
            .reset_index()
    )

    result["aov"] = (
        result["total_sale"] / result["total_order"]
    )

    result = result.sort_values(
        by="aov", ascending=False
    )

    # st.dataframe(result)

    # Display the category with the highest AOV
    top_order_chennal = result.iloc[0]

    st.success(
        f"Highest AOV order channel: {top_order_chennal['order_channel']} "
        f"| AOV: {top_order_chennal['aov']:.2f}",
        icon=":material/thumb_up:"
    )

    st.divider()


def product_aov(df):
    st.subheader('5 . Which product drives highest average order value?')

    result = (
        df.groupby("product_name")
            .agg(
                total_sale=("total_amount", "sum"),
                total_order=("order_id", "nunique")
            )
            .reset_index()
    )

    result["aov"] = (
        result["total_sale"] / result["total_order"]
    )

    result = result.sort_values(
        by="aov", ascending=False
    )

    # st.dataframe(result)

    # Display the category with the highest AOV
    top_product = result.iloc[0]

    st.success(
        f"Highest AOV order channel: {top_product['product_name']} "
        f"| AOV: {top_product['aov']:.2f}",
        icon=":material/thumb_up:"
    )

    st.divider()

def render_aov():
    df = get_clean_df()
    if df is None:
        st.warning("upload an already clean CSV.")
        return
    category_aov(df)
    brand_aov(df)
    payment_mode_aov(df)
    order_chenal_aov(df)
    product_aov(df)
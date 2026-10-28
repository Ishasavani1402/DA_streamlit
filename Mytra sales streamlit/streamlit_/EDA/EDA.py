import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from streamlit_.helper import kpi_card
from streamlit_.helper import footer
from streamlit_.helper import get_clean_df

def render_eda():
    df = get_clean_df()
    if df is None:
        st.warning("upload an already clean CSV.")
        return

    st.caption(f"{df.shape[0]} rows × {df.shape[1]} columns")
    df_preview = st.checkbox("Show clean data preview", value=False)
    if df_preview:
        st.subheader("Clean Data Preview")
        st.dataframe(df)

    st.subheader("Data Summary")
    st.dataframe(df.describe())

    st.divider()

    st.subheader("Correlation Heatmap")
    numeric_cols = df.select_dtypes(np.number)
    plt.figure(figsize=(13,10))
    sns.heatmap(numeric_cols.corr() , annot=True , cmap="coolwarm")
    plt.title("correlation heatmap")
    st.pyplot(plt.gcf())

    st.divider()
    st.subheader("box plot for outliers")
    numerical_cols = df.select_dtypes(include=["float64", "int64"]).columns
    plt.figure(figsize=(15, 10))
    for i, col in enumerate(numerical_cols):
        plt.subplot(4, 4, i + 1) # adjust the number of rows and columns as needed
        sns.boxplot(df[col])
        plt.title(col)
    plt.tight_layout()
    st.pyplot(plt.gcf())

    st.divider()
    kpi(df)  

    footer()



def kpi(df):
    st.subheader("Key Performance Indicators (KPIs)")
    total_sales = df['total_amount'].sum()
    total_orders = df['order_id'].nunique()
    avg_order_value = total_sales / total_orders if total_orders else 0
    total_customers = df['customer_id'].nunique()
    repeated_customers = df[df.duplicated(subset='customer_id', keep=False)]['customer_id'].nunique()
    one_time_customers = total_customers - repeated_customers

    kpi1, kpi2, kpi3  = st.columns(3)
    kpi4 , kpi5 , kpi6 = st.columns(3)
    kpi_card(kpi1, "Total Revenue", f"${total_sales:,.2f}")
    kpi_card(kpi2, "Total Orders", f"{total_orders:,}")
    kpi_card(kpi3, "Average Order Value", f"${avg_order_value:,.2f}")
    kpi_card(kpi4, "Total Customers", f"{total_customers:,}")
    kpi_card(kpi5, "Repeated Customers", f"{repeated_customers:,}")
    kpi_card(kpi6, "One-Time Customers", f"{one_time_customers:,}")


import streamlit as st
import plotly.express as px
from streamlit_.helper import footer
from streamlit_.helper import get_clean_df
import numpy as np

def city_orders(df):
    st.subheader('1 . city wise order')
    result = (
            df.groupby("city", as_index=False)
              .agg(total_orders=("order_id", "count"))
              .sort_values(by="total_orders", ascending=False)
        )
    st.dataframe(result)

    fig = px.bar(
        result.head(10),
        x="total_orders",
        y="city",
        orientation="h",
        title="top 10 City by orders",
        labels={"total_orders": "Total Orders", "city": "City"},
    )
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig)
    st.divider()

def chennal_orders(df):
    st.subheader('2 . order chennal wise order')
    result = (
            df.groupby("order_channel", as_index=False)
              .agg(total_orders=("order_id", "count"))
        )
        # Calculate percentage of total orders
    result["perc_of_total"] = (
        result["total_orders"] / result["total_orders"].sum() * 100
    ).round(2)

    result = result.sort_values(
        by="total_orders",
        ascending=False
    )

    st.dataframe(result)
    # Pie chart
    fig = px.pie(
        result,
        names="order_channel",
        values="total_orders",
        title="Order Chennel Wise Orders",
        hover_data=["perc_of_total"],
        labels={
            "order_channel": "Order Chennel",
            "total_orders": "Total Orders",
            "perc_of_total": "Percentage of Total Orders"
        },
        hole=0.4
    )

    fig.update_traces(
        textinfo="label+percent",
        hovertemplate=(
            "Status: %{label}<br>"
            "Total Orders: %{value}<br>"
            "Percentage: %{customdata[0]:.2f}%"
            "<extra></extra>"
        )
    )

    st.plotly_chart(fig)
    st.divider()


def order_status_orders(df):
    st.subheader('3. Order Status Wise Orders')

    result = (
        df.groupby("order_status", as_index=False)
          .agg(total_orders=("order_id", "count"))
    )

    # Calculate percentage of total orders
    result["perc_of_total"] = (
        result["total_orders"] / result["total_orders"].sum() * 100
    ).round(2)

    result = result.sort_values(
        by="total_orders",
        ascending=False
    )

    # Display table
    st.dataframe(result)

    # Pie chart
    fig = px.pie(
        result,
        names="order_status",
        values="total_orders",
        title="Order Status Wise Orders",
        hover_data=["perc_of_total"],
        labels={
            "order_status": "Order Status",
            "total_orders": "Total Orders",
            "perc_of_total": "Percentage of Total Orders"
        },
        hole=0.4
    )

    fig.update_traces(
        textinfo="label+percent",
        hovertemplate=(
            "Status: %{label}<br>"
            "Total Orders: %{value}<br>"
            "Percentage: %{customdata[0]:.2f}%"
            "<extra></extra>"
        )
    )

    st.plotly_chart(fig)
    st.divider()


def gender_orders(df):
    st.subheader('4 . Gender Wise Orders')

    result = (
        df.groupby("gender", as_index=False)
          .agg(total_orders=("order_id", "count"))
    )

    # Calculate percentage of total orders
    result["perc_of_total"] = (
        result["total_orders"] / result["total_orders"].sum() * 100
    ).round(2)

    result = result.sort_values(
        by="total_orders",
        ascending=False
    )

    # Display table
    st.dataframe(result)

    # Pie chart
    fig = px.pie(
        result,
        names="gender",
        values="total_orders",
        title="Gender Wise Orders",
        hover_data=["perc_of_total"],
        labels={
            "gender": "Gender",
            "total_orders": "Total Orders",
            "perc_of_total": "Percentage of Total Orders"
        },
        hole=0.4
    )

    fig.update_traces(
        textinfo="label+percent",
        hovertemplate=(
            "Status: %{label}<br>"
            "Total Orders: %{value}<br>"
            "Percentage: %{customdata[0]:.2f}%"
            "<extra></extra>"
        )
    )

    st.plotly_chart(fig)
    st.divider()

def age_group_orders(df):
    st.subheader('5 . Age Group wise order')
    conditions = [
    df["age"].between(16, 20),
    df["age"].between(21, 25),
    df["age"].between(26, 35),
    df["age"].between(36, 45)
]

    choices = [
        "teenager",
        "young adult",
        "adult",
        "middle aged"
    ]

    df["age_group"] = np.select(
        conditions,
        choices,
        default="mature adult"
    )

    result = (
            df.groupby("age_group", as_index=False)
              .agg(total_orders=("order_id", "count"))
              .sort_values(by="total_orders", ascending=False)
        )
    st.dataframe(result)

    fig = px.bar(
        result,
        x="age_group",
        y="total_orders",
        title="age group wise orders",
        labels={"total_orders": "Total Orders", "age_group": "City"},
    )
    
    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig)
    st.divider()

def render_orders():
    df = get_clean_df()
    if df is None:
        st.warning("upload an already clean CSV.")
        return
    city_orders(df)
    chennal_orders(df)
    order_status_orders(df)
    gender_orders(df)
    age_group_orders(df)
    footer()
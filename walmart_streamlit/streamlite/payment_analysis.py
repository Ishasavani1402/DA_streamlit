import plotly.express as px
import streamlit as st
from db import run
from . import queries


def payment_analysis():
    st.subheader("Payment Mode Wise Sale")

    payment_df = run(queries.payment_analysis)

    st.dataframe(payment_df, use_container_width=True)

    fig = px.bar(
        payment_df,
        x="payment",
        y=["total_transactions", "total_sale"],
        barmode="group",
        title="Payment Mode Wise Transactions and Sales",
        labels={
            "payment": "Payment Mode",
            "value": "Count / Sales Amount",
            "variable": "Metric"
        },
        text_auto=True,
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    fig.update_layout(
        xaxis_title="Payment Mode",
        yaxis_title="Transactions / Sales Amount",
        legend_title="Metric",
        template="plotly_white"
    )

    st.plotly_chart(fig)
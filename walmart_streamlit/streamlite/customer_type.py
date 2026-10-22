import streamlit as st
from db import run
from . import queries
from .helpers import footer
from plotly import express as px

def custtomer_type():
    st.subheader("customer type distribution")
    customer_type = run(queries.customer_type)
    st.dataframe(customer_type)
    fig = px.bar(customer_type,
        x="customer_type",
        y=["male", "female"],
        barmode="group",
        title="Male vs Female by Customer Type",
        labels={
            "customer_type": "Customer Type",
            "value": "Customer Count",
            "variable": "Gender"
        },
        text_auto=True
    )

    fig.update_layout(
        xaxis_title="Customer Type",
        yaxis_title="Customer Count",
        legend_title="Gender",
        template="plotly_white"
    )

    st.plotly_chart(fig)

    footer()
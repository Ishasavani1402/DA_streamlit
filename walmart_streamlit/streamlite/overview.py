import streamlit as st
from db import run
from . import queries
from .helpers import kpi_card, footer


def overview():
    st.header("📌 Key Business Metrics")

    total_sale = run(queries.total_sale)
    total_qty = run(queries.total_qty)
    total_orders  = run(queries.total_order)
    avg_rate = run(queries.avg_rate)
    total_profit = run(queries.total_profit)

    k1,k2,k3 , k4 , k5= st.columns(5)
    kpi_card(k1, "total sale", f" {int(total_sale.iloc[0,0]):,} Rup.")
    kpi_card(k2, "total quantity", f"{int(total_qty.iloc[0,0]):,}")
    kpi_card(k3, "total orders", f"{int(total_orders.iloc[0,0]):,}")
    kpi_card(k4, "avg rate", f"{int(avg_rate.iloc[0,0]):,}")
    kpi_card(k5, "total profit", f"{int(total_profit.iloc[0,0]):,}")

    st.divider()


    footer()


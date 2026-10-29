import streamlit as st
from streamlit_.helper import footer
from streamlit_.helper import get_clean_df



def product_analysis(df):
    st.subheader('Product Analysis dataset')
    result = (
            df.groupby("product_name")
                .agg(total_orders=("order_id", "count") , 
                     total_revenue = ('total_amount' , 'sum') , 
                     total_qty = ('quantity' , 'sum') , 
                     avg_discount_pct = ('discount_percent' , 'mean') , 
                     total_delivery_days = ('delivery_days' , 'sum'))
                .sort_values(by="total_revenue", ascending=False)
                )
    st.dataframe(result , height='auto')
    st.divider()

def render_product_analysis():
    df = get_clean_df()
    if df is None:
        st.warning("upload an already clean CSV.")
        return
    product_analysis(df)
    footer()
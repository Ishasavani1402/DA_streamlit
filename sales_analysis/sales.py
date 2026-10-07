import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu

# page configuration
st.set_page_config(page_title='sales analysis' , layout='wide')
# CSS
st.markdown("""
<style>
.block-container {
    padding-top: 1.9rem;
    padding-bottom: 1rem;
}

/* Reduce vertical gaps */
div[data-testid="stVerticalBlock"] > div {
    gap: 0.4rem;
}

/* Style horizontal radio like navigation */
div[role="radiogroup"] {
    border-bottom: 1px solid #e0e0e0;
    padding-bottom: 6px;
}

div[role="radiogroup"] label {
    font-size: 15px !important;
    font-weight: 500;
    margin-right: 30px !important;
}

/* Hide radio circle */
div[role="radiogroup"] input[type="radio"] {
    display: none;
}

/* Active tab underline */
div[role="radiogroup"] input[type="radio"]:checked + div {
    border-bottom: 2px solid black;
    padding-bottom: 4px;
}
</style>
""", unsafe_allow_html=True)

# head part
st.markdown("""
<h2 style="margin-bottom:0;">📊 Sales Analysis System</h2>
<p style="color:gray; margin-top:0; margin-bottom:10px;">
</p>
""", unsafe_allow_html=True)

#uploader and column division
col1, col2 = st.columns([3, 2])

with col1:
    uploaded_file = st.file_uploader("Upload Sales CSV File", type=["csv"])

with col2:
    if uploaded_file is None:
        st.markdown(
            "<div style='margin-top:28px; color:gray;'>Please upload a CSV file to begin.</div>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"<div style='margin-top:28px;'>Uploaded: <b>{uploaded_file.name}</b></div>",
            unsafe_allow_html=True
        )

# menu
menu = st.radio(
    "",
    ["Home", "City-wise Sales", "Category Revenue", "Best Product","Time Analysis", "Filters"],
    horizontal=True,
    label_visibility="collapsed"
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df['revenue'] = df['Price'] * df['Quantity']

    if menu == 'Home':
        total_revenue = df['revenue'].sum()
        best_product = df.groupby('Product')['Quantity'].sum().idxmax()
        higest_revenue_product = df.groupby('Product')['revenue'].sum().idxmax()

        k1,k2,k3 = st.columns(3)
        card_style = """
            background-color:black;
            border:1px solid #e0e0e0;
            padding:12px;
            border-radius:6px;
            text-align:center;
        """
        k1.markdown(f"""
        <div style="{card_style}">
            <div style="font-size:14px; color:gray;">Total Revenue</div>
            <div style="font-size:22px; font-weight:600;">₹ {total_revenue}</div>
        </div>
        """, unsafe_allow_html=True)

        k2.markdown(f"""
        <div style="{card_style}">
            <div style="font-size:14px; color:gray;">Best Selling Product</div>
            <div style="font-size:20px; font-weight:600;">{best_product}</div>
        </div>
        """, unsafe_allow_html=True)

        k3.markdown(f"""
        <div style="{card_style}">
            <div style="font-size:14px; color:gray;">Highest Revenue Product</div>
            <div style="font-size:20px; font-weight:600;">{higest_revenue_product}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True)

    elif menu == 'City-wise Sales':
        city_sale = df.groupby('City')['revenue'].sum().sort_values(ascending=False)

        st.markdown("<br>", unsafe_allow_html=True)
        # st.dataframe(city_sale, use_container_width=True)
        st.bar_chart(city_sale)

    elif menu == 'Category Revenue':
            category_sale = df.groupby('Category').agg(
             total_sale = ('revenue','sum') , 
             total_product = ('Product' , 'nunique')    
            ).sort_values(by='total_sale' , ascending=False)
            st.markdown("<br>", unsafe_allow_html=True)
            # st.dataframe(category_sale, use_container_width=True)
            st.bar_chart(category_sale)

    elif menu == 'Best Product':
        best_product =df.groupby('Product')[['Quantity' , 'revenue']].sum().reset_index()

        col_a , col_b = st.columns(2)
        basic = col_a.selectbox(
              'select basic' , 
              ['quantity' , 'revenue']
         )
        top_n = col_b.slider(
              'select no of top products' , min_value=1 , 
              max_value=len(best_product) , 
              value=3
         )

        if basic == 'quantity':
              top_product = best_product.sort_values(by='Quantity' , ascending=False).head(top_n)
        else:
            top_product = best_product.sort_values(by='revenue' , ascending=False).head(top_n)
        st.dataframe(top_product , use_container_width=True)

    elif menu == 'Time Analysis':
         st.markdown("""
            <h2 style="margin-bottom:0;">📈 Daily Sales Analysis</h2>
            <p style="color:gray; margin-top:0; margin-bottom:10px;">
            </p>
            """, unsafe_allow_html=True)
         daily_revenue = df.groupby('Date')['revenue'].sum()
        #  st.dataframe(daily_revenue , use_container_width=True)
         st.line_chart(daily_revenue)

    elif menu == "Filters":

        colX, colY = st.columns(2)

        selected_category = colX.selectbox(
            "Select Category",
            df["Category"].unique()
        )

        min_revenue = colY.number_input(
            "Minimum Revenue",
            min_value=0,
            value=10000
        )

        filtered_df = df[
            (df["Category"] == selected_category) &
            (df["revenue"] >= min_revenue)
        ]

        st.dataframe(filtered_df, use_container_width=True)
else : 
     st.info('upload csv file for view analysis')
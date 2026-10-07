import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from streamlite.home import home
from streamlite.rating import rating_distribution
from streamlite.tv_movies import tv_movie


# page configuration
st.set_page_config(page_title='Netflix Content Analysis' , layout='wide')

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
<h2 style="margin-bottom:0;">📊 Netflix Content Analysis</h2>
<p style="color:gray; margin-top:0; margin-bottom:10px;">
</p>
""", unsafe_allow_html=True)

#uploader and column division
col1, col2 = st.columns([3, 2])

with col1:
    uploaded_file = st.file_uploader("Upload Netflix CSV File", type=["csv"])

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
    ["Home", "Tv / Movies Analysis", "yearly analysis","Director Analysis", "Rating Analysis" , "Country Analysis" , "Gener"],
    horizontal=True,
    label_visibility="collapsed"
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    if menu == 'Home':
        home(df)

    elif menu == 'Tv / Movies Analysis':
            tv_movie(df)
    elif menu =="Rating Analysis":
            rating_distribution()

else : 
     st.info('upload csv file for view analysis')
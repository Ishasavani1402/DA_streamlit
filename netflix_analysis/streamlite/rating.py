import streamlit as st
import plotly.express as px

def rating_distribution(df):
    st.subheader('What is the rating distribution for Movies vs TV Shows?')
    # Rating distribution for Movies vs TV Shows
    rating_dist = (
        df.groupby(['category', 'rating'])
        .size()
        .unstack(fill_value=0)
        .T
        .sort_values(by='Movie', ascending=False)
    )

    st.dataframe(rating_dist)
    fig = px.bar(rating_dist , x=rating_dist.index, y=['Movie', 'TV Show'], barmode='group', title='Rating Distribution: Movies vs TV Shows')
    st.plotly_chart(fig)
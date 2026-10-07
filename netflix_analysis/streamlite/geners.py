import streamlit as st
import plotly.express as px

def geners(df):
    st.subheader('top 10 primary_genre that have higest no of movies')
    top_10_tv_genres = (
    df[df['category'] == 'TV Show']['primary_genre']
    .value_counts()
    .head(10)
    .reset_index()
)
    top_10_tv_genres.columns = ['Primary Genre', 'Number of TV Shows']
    st.dataframe(top_10_tv_genres)
    fig = px.bar(top_10_tv_genres, x='Primary Genre', y='Number of TV Shows')
    st.plotly_chart(fig)

    st.divider()
    st.subheader('top 10 primary_genre that have higest no of movies')
    top_10_movies_genres = (
        df[df['category'] == 'Movie']['primary_genre']
        .value_counts()
        .head(10)
        .reset_index()
    )
    top_10_movies_genres.columns = ['Primary Genre', 'Number of Movies']
    st.dataframe(top_10_movies_genres)
    fig = px.bar(top_10_movies_genres, x='Primary Genre', y='Number of Movies')
    st.plotly_chart(fig)
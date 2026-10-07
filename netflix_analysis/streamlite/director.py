import streamlit as st
import plotly.express as px

def director(df):
    st.subheader('top 10 director who make higest no of movie')
    movies = df[df["category"] == "Movie"].copy()

    movies_exploded = (
        movies.assign(director=movies["director"].str.split(","))
        .explode("director")
    )
    movies_exploded["director"] = movies_exploded["director"].str.strip()

    top_10_directors = (
        movies_exploded.loc[movies_exploded["director"] != "Unknown", "director"]
        .value_counts()
        .head(10)
        .reset_index()
    )
    top_10_directors.columns = ["Director", "Number of Movies"]
    st.dataframe(top_10_directors)
    fig = px.bar(top_10_directors.sort_values('Number of Movies') , x='Number of Movies' , y='Director' ,orientation='h')
    st.plotly_chart(fig)
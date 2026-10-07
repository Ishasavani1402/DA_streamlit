import streamlit as st
from plotly import express as px
def country(df):
    st.subheader('Country Wise Movie Releases')
    # movies
    movies = df[df['category'] == 'Movie'].copy()

    movies_exploded = (
        movies.assign(
            country=movies['country'].str.split(',')
        )
        .explode('country')
    )

    movies_exploded['country'] = (
        movies_exploded['country'].str.strip()
    )

    movies_exploded = movies_exploded[
        ~movies_exploded['country'].isin(['Unknown', ''])
    ]

    country_movie_count = (
        movies_exploded['country']
        .value_counts()
        .reset_index()
    )

    country_movie_count.columns = [
        'Country',
        'Number of Movies'
    ]

    country_movie_count['Share %'] = (
        country_movie_count['Number of Movies']
        / len(movies)
        * 100
    ).round(1)

    country_movie_count = country_movie_count.reset_index(drop=True)

    st.dataframe(
        country_movie_count.head(15),
        use_container_width=True
    )
    fig = px.bar(country_movie_count.head(15),
                 x='Country',
                 y='Number of Movies')
    st.plotly_chart(fig)

    st.divider()
    st.subheader('Country Wise added Tv shows')

    # tv shows
    tv_shows = df[df['category'] == 'TV Show'].copy()

    tv_shows_exploded = (
        tv_shows.assign(
            country=tv_shows['country'].str.split(',')
        )
        .explode('country')
    )

    tv_shows_exploded['country'] = (
        tv_shows_exploded['country'].str.strip()
    )

    tv_shows_exploded = tv_shows_exploded[
        ~tv_shows_exploded['country'].isin(['Unknown', ''])
    ]

    country_tv_show_count = (
        tv_shows_exploded['country']
        .value_counts()
        .reset_index()
    )

    country_tv_show_count.columns = [
        'Country',
        'Number of TV Shows'
    ]

    country_tv_show_count['Share %'] = (
        country_tv_show_count['Number of TV Shows']
        / len(tv_shows)
        * 100
    ).round(1)

    country_tv_show_count = country_tv_show_count.reset_index(drop=True)

    st.dataframe(
        country_tv_show_count.head(15),
        use_container_width=True
    )
    fig = px.bar(country_tv_show_count.head(15),
                    x='Country',
                    y='Number of TV Shows')
    st.plotly_chart(fig)
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from plotly import express as px
def home(df):
    total_genres = df['primary_genre'].nunique()
    avg_duration = df['duration_min'].mean()
    total_movies = (df["category"] == "Movie").sum()
    total_tv_shows = (df["category"] == "TV Show").sum()

    k1,k2,k3 , k4= st.columns(4)
    card_style = """
                background-color:black;
                border:1px solid #e0e0e0;
                padding:12px;
                border-radius:6px;
                text-align:center;
            """
    k1.markdown(f"""
            <div style="{card_style}">
                <div style="font-size:14px; color:gray;">Total Genres</div>
                <div style="font-size:22px; font-weight:600;">{total_genres}</div>
            </div>
            """, unsafe_allow_html=True)
    
    k2.markdown(f"""
            <div style="{card_style}">
                <div style="font-size:14px; color:gray;">Total Movies</div>
                <div style="font-size:20px; font-weight:600;">{total_movies}</div>
            </div>
            """, unsafe_allow_html=True)
    
    k3.markdown(f"""
            <div style="{card_style}">
                <div style="font-size:14px; color:gray;">Total TV Shows</div>
                <div style="font-size:20px; font-weight:600;">{total_tv_shows}</div>
            </div>
            """, unsafe_allow_html=True)
    k4.markdown(f"""
                <div style="{card_style}">
                    <div style="font-size:14px; color:gray;">Avg Movie Duration (min)</div>
                    <div style="font-size:22px; font-weight:600;">{avg_duration}</div>
                </div>
                """, unsafe_allow_html=True)

    st.divider()
    st.subheader('What does the movie duration distribution look like, and what is the typical length?')

    # Filter only Movies and remove missing durations
    movies = df[df['category'] == 'Movie'].copy()
    movie_durations = movies['duration_min']

    # ==============================
    # 1. Distribution Visualization
    # ==============================
    plt.figure(figsize=(12, 6))

    # Histogram + KDE
    sns.histplot(movie_durations, bins=40, kde=True, color='steelblue', edgecolor='black')

    plt.axvline(movie_durations.mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {movie_durations.mean():.0f} min')
    plt.axvline(movie_durations.median(), color='green', linestyle='-', linewidth=2, label=f'Median: {movie_durations.median():.0f} min')

    plt.title('Distribution of Movie Durations on Netflix', fontsize=14, fontweight='bold')
    plt.xlabel('Duration (minutes)')
    plt.ylabel('Number of Movies')
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    st.pyplot(plt)
    plt.close()

    # ==============================
    # 2. Basic Statistics (Typical Length)
    # ==============================
    st.write(f"Mean Duration     : {movie_durations.mean():.1f} minutes")
    st.write(f"Median Duration   : {movie_durations.median():.1f} minutes")
    st.write(f"Mode Duration     : {movie_durations.mode().values[0]:.0f} minutes")
    st.write(f"Minimum Duration  : {movie_durations.min():.0f} minutes")
    st.write(f"Maximum Duration  : {movie_durations.max():.0f} minutes")
    st.write(f"Standard Deviation: {movie_durations.std():.1f} minutes")

    st.divider()
    st.subheader('Who are the top 10 most frequent actors')

        # Split the cast column and explode it
    actors = (
        df[df['cast'] != 'Unknown']['cast']
        .str.split(', ')                   # split by comma + space
        .explode()                         # one actor per row
    )

    # Count frequency of each actor
    top_10_actors = (
        actors
        .value_counts()
        .head(10)
        .reset_index()
    )
    top_10_actors.columns = ['Actor', 'Number of Appearances']
    st.dataframe(top_10_actors)
    fig = px.bar(top_10_actors, x='Actor', y='Number of Appearances')
    st.plotly_chart(fig)

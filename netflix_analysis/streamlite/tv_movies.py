import streamlit as st

def tv_movie(df):
    st.subheader('What % of TV shows have just 1 season??')
    # Filter only TV Shows
    tv_shows = df[df['category'] == 'TV Show']

    # Total number of TV Shows
    total_tv = len(tv_shows)

    # Number of TV Shows with exactly 1 season
    one_season = len(tv_shows[tv_shows['seasons'] == 1])

    # Calculate percentage
    percentage = (one_season / total_tv) * 100

    # Display result
    st.write(f"Total TV Shows          : {total_tv}")
    st.write(f"TV Shows with 1 Season  : {one_season}")
    st.write(f"Percentage              : {percentage:.2f}%")   

    st.divider()

 
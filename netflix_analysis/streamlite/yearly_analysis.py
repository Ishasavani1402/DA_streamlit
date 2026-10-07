import streamlit as st
import plotly.express as px

def yearly_content(df):
    st.subheader('content added per year IN netflix')
    # Yearly count of Movies and TV Shows (separate)
    yearly_counts = (
        df.groupby(["year_added", "category"])
        .size()
        .unstack(fill_value=0)
        .sort_index()
    )

    print("Yearly Total added (Movies vs TV Shows):\n")
    st.dataframe(yearly_counts)
    fig = px.line(yearly_counts , x=yearly_counts.index, y=["Movie", "TV Show"],  title='yearly add Movies and TV Shows')
    st.plotly_chart(fig)
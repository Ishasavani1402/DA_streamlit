import streamlit as st
import matplotlib.pyplot as plt
from IPython.display import display
import plotly.express as px

def footer():
    st.divider()
    st.caption('🍽 Swiggy Analysis | built by Isha')

def kpi_card(column, label, value):
    column.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
        </div>
    """, unsafe_allow_html=True)

def overview(df):
    st.header("📌 Key Business Metrics")

    total_restuarants = df['restaurant'].nunique()

    total_cities = df['city'].nunique() 

    avg_rate = df['avg_ratings'].mean()

    avg_delivery_time = df['delivery_time'].mean()

    avg_price = df['price'].mean()

    k1,k2,k3 , k4 , k5 = st.columns(5)
    kpi_card(k1, "Total Restuarant", f"{total_restuarants}")
    kpi_card(k2, "Total city", f"{total_cities}")
    kpi_card(k3, "avg rate", f"{avg_rate:.2f}")
    kpi_card(k4, "avg delivery time", f"{avg_delivery_time:.2f}")
    kpi_card(k5, "avg price", f"{avg_price:.2f}")

    st.divider()
    st.subheader("🍽️ Food Type Analysis")

# Split comma-separated values and create one row per food type
    df_food = (
        df.assign(food_type=df["food_type"].str.split(","))
        .explode("food_type")
    )

    # Remove extra spaces
    df_food["food_type"] = df_food["food_type"].str.strip()

    st.divider()

    # Total unique cuisines
    total_cuisines = df_food["food_type"].nunique()

    st.info(
        f"Total unique cuisines: {total_cuisines}",
        icon="📌"
    )

    # Top 15 food types
    food_counts = (
        df_food["food_type"]
        .value_counts()
        .head(15)
        .reset_index()
    )

    food_counts.columns = ["food_type", "count"]

    st.dataframe(food_counts)

    # Bar chart
    fig = px.bar(
        food_counts,
        x="food_type",
        y="count",
        title="Top 15 Food Types",
        labels={
            "food_type": "Food Type",
            "count": "Restaurant Count"
        }
    )

    st.plotly_chart(fig, use_container_width=True)


    # --------------------------------------------------
    # Cuisine-wise statistics
    # --------------------------------------------------

    cuisine_stats = (
        df_food.groupby("food_type")
        .agg(
            avg_rating=("avg_ratings", "mean"),
            avg_price=("price", "mean"),
            avg_delivery=("delivery_time", "mean"),
            count=("restaurant", "count")
        )
        .round(2).sort_values("count", ascending=False)

    )

    # Only cuisines with 100+ entries
    cuisine_stats = cuisine_stats[
        cuisine_stats["count"] >= 100
    ]

    st.subheader("📊 Cuisine-wise Performance")

    st.dataframe(cuisine_stats)

    footer()

def city_analysis(df):
    st.header("🏙️ City Wise Avg Delivery Time")
    city_distribution = (
        df.groupby("city")
        .agg(
            avg_delivery=("delivery_time", "mean")
        )
        .round(2)
        .sort_values(by="avg_delivery", ascending=False)
    )

    st.dataframe(city_distribution)

    fig = px.bar(
        city_distribution.reset_index(),
        x="city",
        y="avg_delivery",
    )

    st.plotly_chart(fig)
    footer()

def restuarant_analysis(df):
    st.subheader('highest avg rated restuarants(top 10)')
    high_rate = df[df['total_ratings'] > 500]
    avg_rating = high_rate.groupby('restaurant').agg(
        avg_rate = ('avg_ratings' , 'mean')
    ).round(2)
    # Prepare the data (Top 10 restaurants)
    top_10 = avg_rating.sort_values(by='avg_rate', ascending=False).head(10)
    st.dataframe(top_10)
    fig = px.bar(
        top_10.reset_index(),
        x="restaurant",
        y="avg_rate",
    )

    st.plotly_chart(fig)

    st.divider()

    st.subheader('do premium restaurants deliver faster?')
    restuarant_delivery = df.groupby('price_segment').agg(
    avg_delivery_time = ('delivery_time' , 'mean')
).round(2).sort_values(by="avg_delivery_time", ascending=False)
    st.dataframe(restuarant_delivery)
    fig = px.bar(
        restuarant_delivery.reset_index(),
        x="price_segment",
        y="avg_delivery_time",
    )

    st.plotly_chart(fig)

    footer()
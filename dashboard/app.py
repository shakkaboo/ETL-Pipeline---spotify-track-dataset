import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

from src.db_config import get_db_url


st.set_page_config(
    page_title="Spotify ETL Dashboard",
    page_icon="🎵",
    layout="wide"
)


@st.cache_data
def load_table(table_name):
    engine = create_engine(get_db_url())
    query = f"SELECT * FROM {table_name}"
    return pd.read_sql(query, engine)


st.title("🎵 Spotify ETL Dashboard")
st.write("Dashboard built from PostgreSQL data loaded by the Spotify ETL pipeline.")

api_df = load_table("spotify_tracks_api")
kaggle_df = load_table("spotify_tracks_cleaned")
#Adding sidebar after loading data
st.sidebar.title("🎛️ Dashboard Filters")

# Genre filter
genres = ["All"] + sorted(kaggle_df["track_genre"].dropna().unique().tolist())
selected_genre = st.sidebar.selectbox("Select Genre", genres)

# Mood filter
if "mood_category" in kaggle_df.columns:
    moods = ["All"] + sorted(kaggle_df["mood_category"].dropna().unique().tolist())
    selected_mood = st.sidebar.selectbox("Select Mood", moods)
else:
    selected_mood = "All"

# Popularity category filter
if "popularity_category" in kaggle_df.columns:
    popularity_categories = ["All"] + sorted(
        kaggle_df["popularity_category"].dropna().unique().tolist()
    )
    selected_popularity = st.sidebar.selectbox(
        "Select Popularity Category", popularity_categories
    )
else:
    selected_popularity = "All"

# Song search
search_text = st.sidebar.text_input("Search song or artist")

#Creating filtered dataframe
filtered_df = kaggle_df.copy()

if selected_genre != "All":
    filtered_df = filtered_df[filtered_df["track_genre"] == selected_genre]

if selected_mood != "All":
    filtered_df = filtered_df[filtered_df["mood_category"] == selected_mood]

if selected_popularity != "All":
    filtered_df = filtered_df[
        filtered_df["popularity_category"] == selected_popularity
    ]

if search_text:
    filtered_df = filtered_df[
        filtered_df["track_name"].str.contains(search_text, case=False, na=False)
        | filtered_df["artists"].str.contains(search_text, case=False, na=False)
    ]

tab1, tab2, tab3 = st.tabs(
    ["API Data Overview", "Kaggle Audio Features", "ML-ready Data"]
)

with tab1:
    st.header("Spotify API Data")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total API Tracks", len(api_df))
    col2.metric("Unique Artists", api_df["artists"].nunique())
    col3.metric("Average Duration (min)", round(api_df["duration_ms"].mean() / 60000, 2))

    st.subheader("Tracks from Spotify API")
    st.dataframe(api_df.head(20))

    if "search_query" in api_df.columns:
        query_count = api_df["search_query"].value_counts().reset_index()
        query_count.columns = ["Search Query", "Track Count"]

        fig = px.bar(
            query_count,
            x="Search Query",
            y="Track Count",
            title="Tracks Collected by Search Query"
        )
        st.plotly_chart(fig, use_container_width=True)

    if "explicit" in api_df.columns:
        explicit_count = api_df["explicit"].value_counts().reset_index()
        explicit_count.columns = ["Explicit", "Count"]

        fig = px.pie(
            explicit_count,
            names="Explicit",
            values="Count",
            title="Explicit vs Non-explicit Tracks"
        )
        st.plotly_chart(fig, use_container_width=True)


with tab2:
    st.header("Kaggle Spotify Audio Features")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Filtered Tracks", len(filtered_df))
    col2.metric("Genres", filtered_df["track_genre"].nunique())
    col3.metric("Avg Energy", round(filtered_df["energy"].mean(), 2))
    col4.metric("Avg Danceability", round(filtered_df["danceability"].mean(), 2))

    st.subheader("Cleaned Kaggle Dataset")
    st.dataframe(filtered_df.head(50))

    genre_energy = (
        filtered_df.groupby("track_genre")["energy"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig = px.bar(
        genre_energy,
        x="track_genre",
        y="energy",
        title="Top 10 Genres by Average Energy"
    )
    st.plotly_chart(fig, use_container_width=True)

    if "mood_category" in kaggle_df.columns:
        mood_count = filtered_df["mood_category"].value_counts().reset_index()
        mood_count.columns = ["Mood Category", "Count"]

        fig = px.pie(
            mood_count,
            names="Mood Category",
            values="Count",
            title="Mood Category Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Energy vs Danceability")

    fig = px.scatter(
    filtered_df.head(5000),
    x="energy",
    y="danceability",
    color="popularity_category" if "popularity_category" in filtered_df.columns else None,
    hover_data=["track_name", "artists", "track_genre"],
    title="Energy vs Danceability"
    )
    st.plotly_chart(fig, use_container_width=True)

    #recommendation section
    st.subheader("🎧 Song Recommendation")

    recommend_mood = st.selectbox(
        "Choose mood for recommendation",
        filtered_df["mood_category"].dropna().unique()
        if "mood_category" in filtered_df.columns
        else []
    )

    if st.button("Recommend Songs"):
        recommendations = filtered_df[
            filtered_df["mood_category"] == recommend_mood
        ].sort_values(by="popularity", ascending=False).head(10)

        st.dataframe(
            recommendations[
                ["track_name", "artists", "track_genre", "popularity", "energy", "danceability"]
            ]
        )


with tab3:
    st.header("ML-ready Features")

    ml_columns = [
        "popularity",
        "danceability",
        "energy",
        "tempo",
        "valence",
        "loudness",
        "speechiness",
        "acousticness",
        "instrumentalness",
        "duration_min",
    ]

    available_columns = [col for col in ml_columns if col in kaggle_df.columns]

    ml_df = kaggle_df[available_columns].dropna()

    st.write("These features can be used for popularity prediction or clustering.")
    st.dataframe(ml_df.head(20))

    corr = ml_df.corr(numeric_only=True)

    fig = px.imshow(
        corr,
        text_auto=True,
        title="Feature Correlation Heatmap"
    )
    st.plotly_chart(fig, use_container_width=True)
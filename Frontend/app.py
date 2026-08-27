import os
import pickle

import pandas as pd
import requests
import streamlit as st
from dotenv import load_dotenv


# ==========================================
# Load environment variables
# ==========================================
load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")


# ==========================================
# Load movie data
# ==========================================
movies_dict = pickle.load(
    open(
        r"Notebooks/movies_dict.pkl",
        "rb"
    )
)

movies = pd.DataFrame(movies_dict)


# ==========================================
# Load similarity matrix
# ==========================================
similarity = pickle.load(
    open(
        r"Notebooks/similarity.pkl",
        "rb"
    )
)


# ==========================================
# Fetch movie poster from TMDB
# ==========================================
def fetch_poster(movie_id):

    url = f"https://api.themoviedb.org/3/movie/{movie_id}"

    params = {
        "api_key": TMDB_API_KEY,
        "language": "en-US"
    }

    response = requests.get(url, params=params)

    # Check if API request was successful
    if response.status_code != 200:
        return None

    data = response.json()

    poster_path = data.get("poster_path")

    if poster_path:
        return f"https://image.tmdb.org/t/p/w500{poster_path}"

    return None


# ==========================================
# Recommendation function
# ==========================================
def recommend(movie):

    # Find index of selected movie
    movie_index = movies[movies["title"] == movie].index[0]

    # Get similarity scores for selected movie
    distances = similarity[movie_index]

    # Sort movies according to similarity score
    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []

    # Get top 5 recommendations
    for i in movies_list:

        movie_id = movies.iloc[i[0]]["movie_id"]
        movie_title = movies.iloc[i[0]]["title"]

        poster = fetch_poster(movie_id)

        recommended_movies.append(movie_title)
        recommended_posters.append(poster)

    return recommended_movies, recommended_posters


# ==========================================
# Streamlit UI
# ==========================================
st.title("Movie Recommender System")

selected_movie_name = st.selectbox(
    "Type or select a movie from the dropdown",
    movies["title"].values
)


# ==========================================
# Recommendation button
# ==========================================
if st.button("Show Recommendation"):

    recommendations, posters = recommend(selected_movie_name)

    cols = st.columns(5)

    for i in range(5):

        with cols[i]:

            st.text(recommendations[i])

            if posters[i]:
                st.image(posters[i])
            else:
                st.write("Poster not available")
import streamlit as st
import pandas as pd
import bz2
import requests
import io
from recommendation_system import find_similar_users, recommend_movies_with_diversity

# Function to stream large file directly from a URL
@st.cache_data
def load_datasets(ratings_url, movies_path):
    """
    Streams the ratings data from a URL and loads movie titles from a local file.
    """
    try:
        st.info("Loading large dataset... This may take a few minutes.")
        # Stream and decompress the ratings data
        response = requests.get(ratings_url, stream=True)
        if response.status_code != 200:
            st.error("Failed to fetch the ratings dataset.")
            return None, None
        
        compressed_file = io.BytesIO(response.content)
        with bz2.BZ2File(compressed_file, "rb") as file:
            ratings_data = pd.read_csv(file)
        
        # Load movie titles
        movie_titles = pd.read_csv(movies_path)
        st.success("Datasets loaded successfully!")
        return ratings_data, movie_titles

    except Exception as e:
        st.error(f"Error loading datasets: {e}")
        return None, None

# Dataset URLs and file paths
RATINGS_FILE_URL = "https://drive.google.com/uc?id=1e0XMFMh3mRAX2BQdKI89Gk8Imt_r5nzB&export=download"
MOVIE_TITLES_FILE_PATH = "cleaned_movie_titles.csv"

# Load datasets
ratings_data, movie_titles = load_datasets(RATINGS_FILE_URL, MOVIE_TITLES_FILE_PATH)

# Stop execution if datasets fail to load
if ratings_data is None or movie_titles is None:
    st.stop()

# Streamlit UI
st.title("🎬 Movie Recommendation System")
st.write("Select movies you like, and we'll recommend more!")

# User input: Select movies and assign ratings
movie_options = movie_titles["title"].tolist()
selected_movies = []
for i in range(5):
    movie = st.selectbox(f"Select Movie {i+1}", movie_options, key=f"movie_{i}")
    rating = st.slider(f"Rating for '{movie}'", 1, 5, 3, key=f"rating_{i}")
    movie_id = movie_titles.loc[movie_titles["title"] == movie, "movie_id"].values[0]
    selected_movies.append({"movie_id": movie_id, "rating": rating})

# Generate recommendations
if st.button("Get Recommendations"):
    tolerance = 1  # Allowable rating tolerance
    with st.spinner("Finding similar users and recommending movies..."):
        similar_users = find_similar_users(ratings_data, selected_movies, tolerance)
        recommendations = recommend_movies_with_diversity(
            ratings_data, movie_titles, similar_users, selected_movies
        )
    st.write("### Recommended Movies:")
    st.table(recommendations[["title", "year", "avg_rating"]])

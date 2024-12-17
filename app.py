import streamlit as st
import pandas as pd
import bz2
import requests
import os
from recommendation_system import find_similar_users, recommend_movies_with_diversity

# Function to download the file if it doesn't exist
def download_file(url, output_path):
    """
    Downloads a file from the provided URL if it does not already exist.
    """
    if not os.path.exists(output_path):
        st.info("Downloading large dataset... This may take a few minutes.")
        response = requests.get(url, stream=True)
        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        st.success("Download complete!")

# File paths and download URL
RATINGS_FILE_URL = "https://drive.google.com/uc?id=YOUR_FILE_ID&export=download"
RATINGS_FILE_PATH = "cleaned_ratings_data.csv.bz2"
MOVIE_TITLES_FILE_PATH = "cleaned_movie_titles.csv"

# Download the large ratings file if it doesn't exist
download_file(RATINGS_FILE_URL, RATINGS_FILE_PATH)

# Load datasets
@st.cache_data
def load_datasets(ratings_path, movies_path):
    """
    Loads and decompresses ratings data and loads movie titles.
    """
    with bz2.BZ2File(ratings_path, "rb") as file:
        ratings_data = pd.read_csv(file)
    movie_titles = pd.read_csv(movies_path)
    return ratings_data, movie_titles

# Load data
ratings_data, movie_titles = load_datasets(RATINGS_FILE_PATH, MOVIE_TITLES_FILE_PATH)

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
    similar_users = find_similar_users(ratings_data, selected_movies, tolerance)
    recommendations = recommend_movies_with_diversity(
        ratings_data, movie_titles, similar_users, selected_movies
    )
    st.write("### Recommended Movies:")
    st.table(recommendations[["title", "year", "avg_rating"]])

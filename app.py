import streamlit as st
from recommendation_system import load_datasets, find_similar_users, recommend_movies_with_diversity

# Load datasets
ratings_data, movie_titles = load_datasets("cleaned_ratings_data.csv.bz2", "cleaned_movie_titles.csv")

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

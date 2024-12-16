import pandas as pd
import bz2

# Load datasets
def load_datasets(ratings_path, movies_path):
    """
    Load the compressed ratings dataset and movie titles.
    """
    with bz2.BZ2File(ratings_path, "rb") as file:
        ratings_data = pd.read_csv(file)
    movie_titles = pd.read_csv(movies_path)
    return ratings_data, movie_titles

# Find similar users
def find_similar_users(ratings_data, selected_movies, tolerance=1):
    """
    Find users who have rated the selected movies similarly to the current user's ratings.
    """
    similar_users = set()
    for movie in selected_movies:
        movie_id = movie["movie_id"]
        user_rating = movie["rating"]
        matching_users = ratings_data[
            (ratings_data["movie_id"] == movie_id) &
            (ratings_data["rating"].between(user_rating - tolerance, user_rating + tolerance))
        ]["user_id"].unique()
        similar_users.update(matching_users)
    return list(similar_users)

# Recommend movies with diversity
def recommend_movies_with_diversity(ratings_data, movie_titles, similar_users, selected_movies, top_n=15):
    """
    Recommend movies by aggregating ratings from similar users while ensuring diversity.
    """
    similar_user_ratings = ratings_data[ratings_data["user_id"].isin(similar_users)]
    selected_movie_ids = [movie["movie_id"] for movie in selected_movies]
    similar_user_ratings = similar_user_ratings[~similar_user_ratings["movie_id"].isin(selected_movie_ids)]
    movie_scores = similar_user_ratings.groupby("movie_id")["rating"].mean().reset_index()
    movie_scores = movie_scores.rename(columns={"rating": "avg_rating"})
    recommendations = movie_scores.merge(movie_titles, on="movie_id")
    recommendations = recommendations.sort_values(by="avg_rating", ascending=False)
    recommendations = recommendations.drop_duplicates(subset=["title"])
    return recommendations.head(top_n).sample(n=min(top_n, len(recommendations)), random_state=42)

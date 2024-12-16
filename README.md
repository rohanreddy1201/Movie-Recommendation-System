# 🎬 Movie Recommendation System

This project is a **Movie Recommendation System** that dynamically recommends movies based on user-selected preferences and ratings. The system uses a **collaborative filtering approach** with an added diversity mechanism to ensure personalized and varied recommendations.

---

## 📂 Project Structure

The project directory is organized as follows:

```plaintext
Movie Recommendation System/
├── app.py                       # Main Streamlit application
├── recommendation_system.py     # Core logic for recommendations
├── cleaned_movie_titles.csv     # Movie titles metadata
├── cleaned_ratings_data.csv.bz2 # Compressed movie ratings dataset
├── compress_data.py             # Script to compress large datasets
├── requirements.txt             # Dependencies for the project
└── .gitignore                   # Ignore unnecessary files
```

## 📊 Datasets

### **1. Cleaned Ratings Data (`cleaned_ratings_data.csv.bz2`)**
- **Size**: 499MB (compressed)
- Contains **100,480,507 rows** of user ratings from the Netflix Prize Dataset.
- **Columns**:
  - `movie_id`: Unique ID for each movie.
  - `user_id`: Unique ID for each user.
  - `rating`: User rating for the movie (1-5).
  - `date`: Date of the rating.

### **2. Cleaned Movie Titles Data (`cleaned_movie_titles.csv`)**
- Contains metadata for **17,763 movies**.
- **Columns**:
  - `movie_id`: Unique movie ID.
  - `year`: Release year of the movie.
  - `title`: Title of the movie.

## 🧠 Recommendation Logic

The system uses a **collaborative filtering approach** with added diversity to ensure personalized and varied recommendations:

1. **Find Similar Users**:
   - Based on movies selected and ratings provided by the user.
   - A tolerance of `±1` in ratings is used to identify similar users.

2. **Aggregate Ratings**:
   - Fetch ratings for movies rated by similar users.
   - Exclude movies already selected by the user.

3. **Add Diversity**:
   - Remove duplicate movie titles to ensure unique recommendations.
   - Randomly sample movies from the top-rated list to introduce variety.

### **How It Works**:
- Users input 5 movies and their ratings.
- The system finds users with similar preferences (tolerance in ratings).
- The recommendations are ranked based on average ratings from similar users.
- Duplicates are removed, and diversity is added for a balanced result.

## 🚀 Features

- **Dynamic Input**:  
  Users can select **5 movies** of their choice and assign ratings (1-5).

- **Personalized Recommendations**:  
  Movies are recommended based on **similar users' ratings**, ensuring relevance.

- **Diversity Mechanism**:  
  - Duplicate movie titles are removed to avoid repetitive recommendations.  
  - Random sampling from top-rated movies ensures varied suggestions.

- **Compressed Data Handling**:  
  The system efficiently handles large datasets using `.bz2` compression for ratings data.

- **Streamlit Interface**:  
  A user-friendly web interface built with Streamlit makes it easy to interact with the system.

## 💻 Running the Project

Follow these steps to set up and run the project locally:

### **1. Install Dependencies**

Ensure you have Python installed (version 3.8 or later). Install required libraries using the following command:

```bash
pip install -r requirements.txt
```

### **2. Run the Streamlit App
Start the Streamlit application by running the following command in your terminal:

```bash
streamlit run app.py
```

### **3. User Interaction**

Once the app opens in your browser:

1. **Select 5 Movies**:  
   Use the dropdown menus to select 5 movies from the list of available titles.

2. **Provide Ratings**:  
   Assign ratings (from 1 to 5) for each selected movie using the provided sliders.

3. **Generate Recommendations**:  
   Click the **"Get Recommendations"** button. The system will analyze your inputs, find similar users, and recommend movies based on their ratings.

4. **View Results**:  
   The app will display a table of **recommended movies** with the following details:
   - **Title**: Name of the recommended movie.
   - **Year**: Release year of the movie.
   - **Avg Rating**: The average rating from users with similar preferences.

## 🤝 Contributing

We welcome contributions to improve this project!  
If you have suggestions for features or enhancements, feel free to open an issue or submit a pull request.

---

## 📜 License

This project is licensed under the **MIT License**. You are free to use, modify, and distribute this software, provided proper credit is given.

---

## ✨ Acknowledgments

- **Netflix Prize Dataset**: For providing the foundational data for this recommendation system.
- **Python Libraries**:
  - `Streamlit`: For creating a seamless web interface.
  - `Pandas`: For data processing and manipulation.

import streamlit as st
import pickle
import requests

# ---------------------------------------
# Fetch movie poster and rating from TMDB
# ---------------------------------------
def fetch_movie_details(movie_id):
    api_key = "445c4af013342bd13ffd2f705f483b9d"
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"

    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        poster_path = data.get("poster_path")
        rating = data.get("vote_average")

        if poster_path:
            poster_url = "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            poster_url = "https://via.placeholder.com/500x750?text=No+Image"

        return poster_url, rating

    except:
        return "https://via.placeholder.com/500x750?text=API+Error", "N/A"


# ---------------------------------------
# Recommendation function
# ---------------------------------------
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_posters = []
    recommended_ratings = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        title = movies.iloc[i[0]].title
        poster, rating = fetch_movie_details(movie_id)

        recommended_movies.append(title)
        recommended_posters.append(poster)
        recommended_ratings.append(rating)

    return recommended_movies, recommended_posters, recommended_ratings

# ---------------------------------------
# Load data
# ---------------------------------------
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movie_list = movies['title'].values

# ---------------------------------------
# Streamlit UI
# ---------------------------------------

st.title("🎬 Movie Recommender System")

selected_movie = st.selectbox(
    "Select a movie",
    movie_list
)

if st.button("Recommend"):

    names, posters, ratings = recommend(selected_movie)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])
        st.write("⭐", ratings[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])
        st.write("⭐", ratings[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])
        st.write("⭐", ratings[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])
        st.write("⭐", ratings[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])
        st.write("⭐", ratings[4])
import pickle
import streamlit as st
import requests
import pandas as pd

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=db7fc08aa2a8aae27c8a4eeea3d52a9b&language=en-US'
                            .format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)

        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_posters


movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    "Type or select a movie from the dropdown",
    movies['title'].values)

if st.button('Show Recommendation'):
    names,posters = recommend(selected_movie_name)

    cols = st.columns(5)

    col1 = cols[0]
    col2 = cols[1]
    col3 = cols[2]
    col4 = cols[3]
    col5 = cols[4]

    col1.text(" ")
    col2.text(" ")
    col3.text(" ")
    col4.text(" ")
    col5.text(" ")

    movie_posters = [
    posters[0],
    posters[1],
    posters[2],
    posters[3],
    posters[4],
    ]
    cols = st.columns(5)

    for i, col in enumerate(cols):
        if i < len(posters):
            col.image(posters[i], use_column_width=True, caption=f"Poster {i + 1}")

    col1.text(names[0])
    col2.text(names[1])
    col3.text(names[2])
    col4.text(names[3])
    col5.text(names[4])

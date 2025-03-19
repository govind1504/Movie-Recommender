import streamlit as st
import pandas as pd
import pickle
import requests
from streamlit import columns
similarity = pickle.load(open('similarity.pkl','rb'))
movies = pd.read_pickle('Movies.pickle')
movie_list = movies['title'].values
st.title('Movie Recommendation system')
selected_movie = st.selectbox('Select Movies' , movie_list)

def recommend(movie):
    movie_index = movies[movies['title']== movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse= True , key= lambda x : x[1]) [1:6]
    Recommended_movies = []
    MovieId = []
    for i in movies_list:
        MovieId.append(movies.iloc[i[0]].movie_id)
        Recommended_movies.append(movies.iloc[i[0]].title)
    return Recommended_movies,MovieId

Recommendation , MovieId = recommend(selected_movie)

if st.button('Recommend'):
    col1, col2, col3 , col4 , col5 = st.columns(5 , gap='small' )
    columns = [col1 , col2 , col3 , col4 , col5]
    for rec,id,col in zip(Recommendation,MovieId,columns):
        url = f"https://api.themoviedb.org/3/movie/{id}/images"

        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJiYzZmYjZiYzZjMjkyZmI0OWJjMTRmMWQ4ODhhYmJmMiIsIm5iZiI6MTc0MjMwMjkwMy4xNDgsInN1YiI6IjY3ZDk2ZWI3NmE3Yjk4MDQzNmM2YjkzNiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.L5ZApPFbY-lLDNkTOzBBnWqnc_6ZaUkbQfK1qQCtT9s"
        }

        response = requests.get(url, headers=headers)
        image = response.json()
        try:
            file_path = image['backdrops'][0]['file_path']
        except :
            file_path = ""
        with col:
            st.write(rec)
            if file_path == '':
                st.error('NO IMG')
            else:
                st.image(f"http://image.tmdb.org/t/p/w500{file_path}")
            st.write(id)

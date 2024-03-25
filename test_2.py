import pickle
import streamlit as st
import pandas as pd
import requests
# import requests
def fetch_poster(tmdbId):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=a3437eb04b986ef8745a7379ad8010d5&language=en-US".format(tmdbId)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    if poster_path != None:
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path


def recommend(movie):
    index = movies[movies['Title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    flag = 0
    for i in distances[1:6]:
        # fetch the movie poster
        tmdbId = movies.iloc[i[0]].tmdbId
        # st.text(tmdbId)
        # st.text(movies.iloc[i[0]].Title)
        poster = fetch_poster(tmdbId)
        
        if poster !=  None :
            flag = flag+1
            recommended_movie_posters.append(fetch_poster(tmdbId))
            recommended_movie_names.append(movies.iloc[i[0]].Title)

    return recommended_movie_names,recommended_movie_posters,flag

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movies = pd.DataFrame(movies_dict)

st.title('Movie Recommender System')

option = st.selectbox(
    "Type or select a movie from the dropdown",
    movies['Title'].values)

if st.button('Show Recommendation'):
    # recommendations = recommend(option)
    # for i in recommendations:
    #     st.write(i)
    recommended_movie_names,recommended_movie_posters,flag = recommend(option)
    # st.text(recommended_movie_posters)
    col1, col2, col3, col4, col5 = st.columns(5)
    if flag >=1 :
        with col1:
            st.image(recommended_movie_posters[0])
            st.text(recommended_movie_names[0])
    if flag >=2:
        with col2:
            st.image(recommended_movie_posters[1])
            st.text(recommended_movie_names[1])
    if flag >=3:
        with col3:
            st.image(recommended_movie_posters[2])
            st.text(recommended_movie_names[2])
    if flag>=4:
        with col4:
            st.image(recommended_movie_posters[3])
            st.text(recommended_movie_names[3])
    if flag>=5:
        with col5:
            st.image(recommended_movie_posters[4])
            st.text(recommended_movie_names[4])
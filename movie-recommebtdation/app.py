import streamlit as st
import pickle
import pandas as pd
import requests

# tmdb_api_key = c37f2b95fc2c56e8342325819a90c618

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=c37f2b95fc2c56e8342325819a90c618&language=en-US'.format(movie_id))
    data = response.json()
    return 'https://image.tmdb.org/t/p/w500'+data['poster_path']


def recommend(movie):
    movie_index = movies_df[movies_df['title'] == movie].index[0]
    print(movie_index)

    similar_movies_list = sorted(list(enumerate(similarity[movie_index])), reverse=True, key=lambda x: x[1])[1:6]
    print(similar_movies_list)

    similar_movies_names = []
    similar_movies_posters = []

    for i in similar_movies_list:
        similar_movies_names.append(movies_df.iloc[i[0]].title)
        similar_movies_posters.append(fetch_poster(movies_df.iloc[i[0]].id))
    return similar_movies_names, similar_movies_posters


movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
# rb = read binary
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies_df = pd.DataFrame(movies_dict)
st.title(' Movie Recommender System')


selected_movie_name = st.selectbox("Enter the movie name", movies_df['title'].values)

if st.button('Recommend'):
    recommended_movies, recommended_movie_posters = recommend(selected_movie_name)
    movie_index = movies_df[movies_df['title'] == selected_movie_name].index[0]
    st.write("The selected movie name is : ")
    st.write(selected_movie_name)
    poster = fetch_poster(movies_df.iloc[movie_index].id)
    st.image(poster, width=125, use_column_width=125)

    st.title("The recommended movies are : ")
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.write(recommended_movies[0])
        st.image(recommended_movie_posters[0])

    with col2:
        st.write(recommended_movies[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.write(recommended_movies[2])
        st.image(recommended_movie_posters[2])

    with col4:
        st.write(recommended_movies[3])
        st.image(recommended_movie_posters[3])

    with col5:
        st.write(recommended_movies[4])
        st.image(recommended_movie_posters[4])
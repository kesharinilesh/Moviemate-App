import sys
print(sys.executable)
import warnings
warnings.filterwarnings('ignore')

import pickle 
import streamlit as st
import pandas as pd
import requests
import webbrowser


movies_set = pickle.load(open('movie-recommender-system.sav','rb'))
similarity=pickle.load(open('movie-recommender-system.sav','rb'))
movies = pd.DataFrame(movies_set)


def fetch_data(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=f4b23bf84275e9cc787656b48e72e912&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def fetch_imdb(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=f4b23bf84275e9cc787656b48e72e912".format(movie_id)
    data = requests.get(url)
    data = data.json()
    imdb_id=data['imdb_id']
    imdb_page_path = "https://www.imdb.com/title/" + imdb_id
    return imdb_page_path

def recommend(movie):
    index = movies[movies['Title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    insert_imdb_page=[]
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].Movie_ID
        recommended_movie_posters.append(fetch_data(movie_id))
        insert_imdb_page.append(fetch_imdb(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].Title)

    return recommended_movie_names,recommended_movie_posters,insert_imdb_page

st.set_page_config(page_title="Moviemate",page_icon="https://i.pinimg.com/564x/84/22/28/84222812f50d6ebccb5ae4b040a6a2b5.jpg",layout="wide",initial_sidebar_state="expanded",)

st.header("Popcorn Ready? Let's roll!")
selected_movie = st.selectbox(
    'Discover your next favorite movie',
(movies['Title'].values))

try:
    if st.button('Get Suggestions'):
        recommended_movie_names,recommended_movie_posters,insert_imdb_page = recommend(selected_movie)
        st.caption('Your next cinematic obsession could be among these top-rated choices')
        col1, col2, col3, col4, col5 = st.columns(5)
        max_image_width = st.config.get_option("server.maxUploadSize")
        w = 220
        h = int(w / 0.80)
        st.markdown("""<style>.poster-img {max-width: 100%;height: auto;}</style>""", unsafe_allow_html=True)
        with col1:
            st.text(recommended_movie_names[0])
            st.markdown(f'<a href="{insert_imdb_page[0]}" target="_blank"><img class="poster-img" src="{recommended_movie_posters[0]}" width={w} height={h}></a>', unsafe_allow_html=True)
        with col2:
            st.text(recommended_movie_names[1])
            st.markdown(f'<a href="{insert_imdb_page[1]}" target="_blank"><img class="poster-img" src="{recommended_movie_posters[1]}" width={w} height={h}></a>', unsafe_allow_html=True)
        with col3:
            st.text(recommended_movie_names[2])
            st.markdown(f'<a href="{insert_imdb_page[2]}" target="_blank"><img class="poster-img" src="{recommended_movie_posters[2]}" width={w} height={h}></a>', unsafe_allow_html=True)
        with col4:
            st.text(recommended_movie_names[3])
            st.markdown(f'<a href="{insert_imdb_page[3]}" target="_blank"><img class="poster-img" src="{recommended_movie_posters[3]}" width={w} height={h}></a>', unsafe_allow_html=True)
        with col5:
            st.text(recommended_movie_names[4])
            st.markdown(f'<a href="{insert_imdb_page[4]}" target="_blank"><img class="poster-img" src="{recommended_movie_posters[4]}" width={w} height={h}></a>', unsafe_allow_html=True)
        st.caption("Thank you for using Moviemate! :sunglasses:" )
except:
    st.caption("Oops! {} is one of a kind.".format(selected_movie))
    st.caption("Thank you for using Moviemate! :sunglasses:")

col1, col2, col3,col4,col5,col6,col7= st.columns(7)
with col4:
    st.write("© 2023, Moviemate")
    st.write("Follow me on:")
    st.markdown(f'<a href="https://www.linkedin.com/in/nileshkeshari/" target="_blank"><img src="https://cdn1.iconfinder.com/data/icons/logotypes/32/circle-linkedin-512.png" alt="Linkedin" style="width:32px;height:32px;border-radius:50%;"></a>    <a href="https://github.com/kesharinilesh" target="_blank"><img src="https://cdn1.iconfinder.com/data/icons/bootstrap-fill-vol-2/16/github-256.png" alt="Github" style="width:32px;height:32px;border-radius:50%;"></a>    <a href="https://www.instagram.com/enigmatic._.star/" target="_blank"><img src="https://cdn1.iconfinder.com/data/icons/social-circle-3/32/instagram_circle-512.png" alt="Instagram" style="width:32px;height:32px;border-radius:50%;"></a>',unsafe_allow_html=True
    )









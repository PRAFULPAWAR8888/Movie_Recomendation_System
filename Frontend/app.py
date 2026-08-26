import streamlit as st
import pickle
import pandas as pd



movies_dict = pickle.load(open(r"C:\Users\pawar\OneDrive\Documents\ML Projects\Movie_Recomendation_System\Notebooks\movies_dict.pkl", 'rb'))
movies = pd.DataFrame(movies_dict)

st.title("Movie Recommender System")

option = st.selectbox(
    "Select Movies", movies['title'].values
    
)

import streamlit as st
import pandas as pd
import numpy as np
st.write("Hello there here world1")

#-------------------------------------------

df = pd.read_csv('data/movie_ratings.csv')
st.write(df.head())
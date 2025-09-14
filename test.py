import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
st.write("Hello there here world1")

#-------------------------------------------
#loading everything to dataframe
df = pd.read_csv('data/movie_ratings.csv')
#getting rid of lines with NaN in 'genres'
cleared = df.dropna()
#creating new dataframe to store sanitized rows
df_cleared = df[cleared].copy()
#creating a mask with grouped_by results
gb = df_cleared.groupby('genres')
#dispalaying grouped_by results on streamlit page 
st.write(gb['movie_id'].count())


fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=gb['movie_id'].count(),
        y=gb['genres']
    )
)

st.plotly_chart(fig, config = {'scrollZoom': False})
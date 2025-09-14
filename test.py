import streamlit as st
import plotly.graph_objects as go
import pandas as pd

#Question #1

st.write("Question #1, Part 1: All genres and amount of Movies belonging to those numbers. Moviea ID might be counted several times because they might belong to several 'genres' siltaneously")

# Load dataset
df = pd.read_csv('data/movie_ratings.csv')

# Drop rows where 'genres' is NaN
df_cleared = df.dropna(subset=['genres']).copy()

# Group by genres and count movies
genre_counts = df_cleared.groupby('genres')['movie_id'].count()

# Display grouped counts in Streamlit
st.write(genre_counts)

# Create plotly scatter
fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=genre_counts.index,   # genres
        y=genre_counts.values,  # counts
        mode='markers+lines'
    )
)
#st.write("Question #1, Part 2: Plotting of the stats above")

st.plotly_chart(fig, config={'scrollZoom': False})

#Question# 2




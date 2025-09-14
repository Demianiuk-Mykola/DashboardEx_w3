import streamlit as st
import plotly.graph_objects as go
import pandas as pd

st.write("Hello there here world1")

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

st.plotly_chart(fig, config={'scrollZoom': False})

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import altair as alt


st.set_page_config(
    page_title="MoviesRatings",
    page_icon="📽️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://docs.streamlit.io/',
        'Report a bug': 'https://github.com/streamlit/streamlit/issues',
        'About': "This is my awesome Streamlit app!"
    })

# Question# 1
#------------------

# Load dataset
df = pd.read_csv('data/movie_ratings.csv')
#------------------


# Drop rows where 'genres' is NaN
df_cleared = df.dropna(subset=['genres']).copy()

# Group by genres and count movies
genre_counts = df_cleared.groupby('genres')['movie_id'].count()


genre_counts_df = genre_counts.reset_index()
genre_counts_df.columns = ["genres", "movie_id"]  # rename for clarity

col = st.columns((1, 1), gap='medium')




with col[0]:
    st.markdown('#### Question #1')

    st.dataframe(
        genre_counts_df,
        column_order=("genres", "movie_id"),
        hide_index=True,
        width=600,
        column_config={
            "genres": st.column_config.TextColumn("Genre"),
            "movie_id": st.column_config.ProgressColumn(
                "Movies",
                format="%d",
                min_value=0,
                max_value=int(genre_counts_df["movie_id"].max())
            )
        }
    )
with col[1]:
    st.markdown('#### Question #2')
    # Create plotly scatter
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=genre_counts.index,   # genres
            y=genre_counts.values,  # counts
            mode='markers+lines',
            marker=dict(size=10, color='crimson'),
            line=dict(width=3, color='blue'),
            hovertemplate="<b>%{x}</b><br>Movies: %{y}<extra></extra>"
        )
    )
    fig.update_layout(
        title="Number of Movies per Genre",
        xaxis_title="Genres",
        yaxis_title="Movie Count",
        #plot_bgcolor="rgba(245,245,245,1)",
        #paper_bgcolor="white",
        #font=dict(size=14, family="Arial", color="black"),
        xaxis=dict(tickangle=30)
)
    st.plotly_chart(fig, config={'scrollZoom': False})
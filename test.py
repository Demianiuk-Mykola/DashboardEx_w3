import streamlit as st
#from vega_datasets import data
import plotly.graph_objects as go
import plotly.express as px
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
    st.markdown('###### Movies per Genre')

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

    # Compute mean rating per genre
    genre_mean = df_cleared.groupby('genres')['rating'].mean()
    # Convert to DataFrame if you want
    genre_mean_df = genre_mean.reset_index()
    genre_mean_df.columns = ["genres", "mean_rating"]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=genre_mean.index,   # genres
            y=genre_mean.values,  # counts
            mode='markers+lines',
            marker=dict(size=10, color='crimson'),
            line=dict(width=3, color='blue'),
            hovertemplate="<b>%{x}</b><br>Movies: %{y}<extra></extra>"
        )
    )
    fig.update_layout(
        title="Viewer satisfaction",
        xaxis_title="Genres",
        yaxis_title="Rating",
        #plot_bgcolor="rgba(245,245,245,1)",
        #paper_bgcolor="white",
        #font=dict(size=14, family="Arial", color="black"),
        xaxis=dict(tickangle=30)
)
    st.plotly_chart(fig, config={'scrollZoom': False})

#2nd row
#df = px.data.tips()
fig = px.histogram(df, x="genres", y="rating",
                color='year', barmode='group',
                histfunc='avg',
                height=400)

tab1, tab2 = st.tabs(["Streamlit theme (default)", "Plotly native theme"])
with tab1:
    st.plotly_chart(fig, theme="streamlit")
with tab2:
    st.plotly_chart(fig, theme=None)
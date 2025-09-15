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






# Load dataset
df = pd.read_csv('data/movie_ratings.csv')
#------------------



with st.sidebar:
    st.title('📽️*MoviesRatings*📽️')
    #selectbox for unique Years of cars
    year_list = sorted(df['year'].dropna().astype(int).unique(), reverse=True)
    selected_year = st.selectbox("Average rating for the year:", year_list)
    df_selected_year = df[df.year == selected_year]
    df_selected_year_sorted = df_selected_year.sort_values(by="rating", ascending=False)

# Question# 1
#------------------

# Group by genres and count movies
unique_movies_per_genre = df.groupby('genres')['title'].nunique().reset_index()
unique_movies_per_genre.columns = ["Genre", "Unique Movie Count"]

#st.write(unique_movies_per_genre)

col = st.columns((1, 1), gap='medium')

with col[0]:
    #Question #3

    st.markdown('#### Question #3')

    
    # Filter movies for the selected year
    df_selected_year = df[df['year'] == selected_year]
    overall_rating = round(df_selected_year['rating'].mean(), 2)  # round first

    # Find previous years
    previous_years = df['year'][df['year'] < selected_year]

    if len(previous_years) > 0:
        prev_year = previous_years.max()
        prev_rating = round(df[df['year'] == prev_year]['rating'].mean(), 2)
        delta = round(overall_rating - prev_rating, 2)  # numeric delta for coloring
    else:
        delta = None  # No previous year, Streamlit treats None as no delta

    # Display metric
    st.metric(
        label=f"🎬 Average Rating in {selected_year}",
        value=f"{overall_rating:.2f}",
        delta=delta  # numeric: green ↑ if positive, red ↓ if negative, neutral if 0
    )
    #Question #1

    #2nd row
    st.markdown('#### Question #1')
    st.markdown('###### Movies per Genre')
    st.dataframe(
        unique_movies_per_genre,
        column_order=("Genre", "Unique Movie Count"),
        hide_index=True,
        width=600,
        column_config={
            "Genre": st.column_config.TextColumn("Genre"),
            "Unique Movie Count": st.column_config.ProgressColumn(
                "Unique Movie Count",
                format="%d",
                min_value=0,
                max_value=int(unique_movies_per_genre["Unique Movie Count"].max())
            )
        }
    )
   
with col[1]:
    st.markdown('#### Question #2')
    # Create plotly scatter

    # Compute mean rating per genre
    genre_mean = df.groupby('genres')['rating'].mean()
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


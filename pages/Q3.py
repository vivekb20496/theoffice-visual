import streamlit as st
import plotly.express as px
import pandas as pd

from Home import df_exploded


df_exploded["word_count"] = df_exploded["line"].apply(lambda x: len(str(x).split()))

# Title
st.title("Question 3. Average Words Per Line Per Character Analysis")

all_seasons = sorted(df_exploded["season"].unique())
all_episodes = sorted(df_exploded["episode"].unique())

# Filter placement using columns
col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    selected_seasons = st.multiselect("Select Seasons", all_seasons, default=all_seasons)

with col2:
    selected_episodes = st.multiselect("Select Episodes", all_episodes, default=all_episodes)

with col3:
    top_n_options = [5, 10, 25, "All"]
    top_n = st.selectbox("Select Top N Characters", top_n_options, index=0)


filtered_df = df_exploded[
    (df_exploded["season"].isin(selected_seasons)) & 
    (df_exploded["episode"].isin(selected_episodes))
]


filtered_avg_words = filtered_df.groupby("unique_speakers")["word_count"].mean().reset_index()
filtered_avg_words.rename(columns={"word_count": "Avg_Words_Per_Line"}, inplace=True)

# Apply Top N filter
if top_n != "All":
    top_n_df = filtered_avg_words.nlargest(int(top_n), "Avg_Words_Per_Line")
else:
    top_n_df = filtered_avg_words

fig = px.bar(
    top_n_df, 
    x="unique_speakers", 
    y="Avg_Words_Per_Line", 
    title=f"Top {top_n} Characters by Avg Words Per Line",
    labels={"unique_speakers": "Character", "Avg_Words_Per_Line": "Average Words Per Line"},
    color="Avg_Words_Per_Line",
    color_continuous_scale="thermal"
)

st.plotly_chart(fig)

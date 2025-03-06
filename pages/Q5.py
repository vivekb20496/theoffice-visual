import streamlit as st
import plotly.express as px
import pandas as pd

from Home import df_exploded

# Title
st.title("Question 5. Most Common Word Per Character Analysis")

df_exploded['line'] = df_exploded['line'].replace('', None)
df_filtered = df_exploded.dropna(subset=['line'])


spoken_episodes = df_filtered.groupby('unique_speakers')[['season', 'episode']].apply(lambda x: set(zip(x['season'], x['episode'])))


all_episodes = set(zip(df_exploded['season'], df_exploded['episode']))


no_lines_data = [(char,  len(all_episodes - episodes)) for char, episodes in spoken_episodes.items()]

df_no_lines = pd.DataFrame(no_lines_data, columns=['Character', 'Episodes Without Lines'])


st.dataframe(df_no_lines)

import streamlit as st
import plotly.express as px
import pandas as pd

from Home import df_exploded

st.title("Q6. That's What She Said Analysis")

filtered_df = df_exploded[df_exploded["line"].str.contains(r"\bThat's what she said\b", case=False, na=False, regex=True)]

filtered_df_q6 = pd.DataFrame(filtered_df, columns=['season', 'episode', 'title', 'scene', 'unique_speakers', 'line'])

filtered_df_q6 = filtered_df_q6.rename(columns={'season': 'Season', 'episode': 'Episode', 'title':'Title', 'scene': 'Scene', 'unique_speakers':'Character', 'line':'Line'})
st.dataframe(filtered_df_q6)

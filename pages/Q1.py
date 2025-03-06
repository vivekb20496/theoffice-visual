import streamlit as st
import plotly.express as px
import pandas as pd

from home import df_exploded

st.title("Q1. Total Characters & Their Names ")

unique_names = df_exploded['unique_speakers'].unique()


unique_names_df = pd.DataFrame({'Characters': list(unique_names)})
total_unique_names = len(unique_names_df)
st.text(f"Approximate number of characters: {total_unique_names}" )
st.dataframe(unique_names_df)

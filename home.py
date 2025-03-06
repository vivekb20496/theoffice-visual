import streamlit as st
import pandas as pd
import re
import plotly
import plotly.graph_objects as go
from plotly._subplots import make_subplots
import plotly.express as px

@st.cache_data
def load_data():
    df = pd.read_csv('The-Office-Lines-V4.csv')
    return df

df = load_data() 

df = df.drop(columns=['Unnamed: 6'])

df = df.drop_duplicates(subset=['season', 'episode', 'title', 'scene', 'speaker', 'line'])

df.reset_index(drop=True, inplace=True)

def extract_unique_names(speaker):
    names = set(re.split(r'\s*(?:,|&|\band\b|/)\s*', speaker)) 
    names.discard('') 
    return ', '.join(sorted(names))

df['unique_speakers'] = df['speaker'].apply(extract_unique_names)

df['unique_speakers'] = df['unique_speakers'].str.strip().str.replace(r'^[:"]+|[:"]+$', '', regex=True)

df["unique_speakers"] = df["unique_speakers"].str.split(", ")


df_exploded = df.explode("unique_speakers", ignore_index=True)

st.dataframe(df_exploded)

)

st.plotly_chart(fig)

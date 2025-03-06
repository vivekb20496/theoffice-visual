import streamlit as st
import plotly.express as px
import pandas as pd

from main_app import df_exploded

count_lines = df_exploded.groupby(['season', 'episode', 'unique_speakers']).size().reset_index(name='count')
count_lines = count_lines.sort_values(by=['season', 'episode', 'count'], ascending=[True, True, False])

total_counts = count_lines.groupby('unique_speakers')['count'].sum().reset_index()

col1, col2, col3 = st.columns([1.2,2.5,0.5])

with col1:
    selected_seasons = st.multiselect("Select Season(s)", sorted(count_lines['season'].unique()), default=sorted(count_lines['season'].unique()))

with col2:
    selected_episodes = st.multiselect("Select Episode(s)", sorted(count_lines['episode'].unique()), default=sorted(count_lines['episode'].unique()))

with col3:
    top_n = st.selectbox("Show Top N Speakers", [5, 10, 25, "All"], index=0)

filtered_df = count_lines[
    count_lines['season'].isin(selected_seasons) & count_lines['episode'].isin(selected_episodes)
]

# Filter data based on selections
filtered_counts = filtered_df.groupby('unique_speakers')['count'].sum().reset_index()

# Apply Top N filter
if top_n != "All":
    filtered_counts = filtered_counts.nlargest(top_n, 'count')

# If no filter applied, show total counts
if filtered_df.empty:
    filtered_counts = total_counts if top_n == "All" else total_counts.nlargest(top_n, 'count')


# Bar chart
fig = px.bar(
    filtered_counts if not filtered_df.empty else total_counts,
    x='unique_speakers',
    y='count',
    title="Total Count of Lines by Speaker",
    labels={'count': 'Total Lines', 'unique_speakers': 'Speaker'},
    color='unique_speakers',
)

st.plotly_chart(fig)

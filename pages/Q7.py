import streamlit as st
import plotly.express as px
import pandas as pd

from Home import df_exploded

st.title("Q7. Average Percent Of Lines Per Episode By Each Character")

total_lines_per_episode = df_exploded.groupby(["season", "episode"]).size().reset_index(name="Total_Lines")

# Calculate speaker lines per episode
speaker_lines_per_episode = df_exploded.groupby(["season", "episode", "unique_speakers"]).size().reset_index(name="Speaker_Lines")
speaker_lines_per_episode = speaker_lines_per_episode.merge(total_lines_per_episode, on=["season", "episode"])

# Calculate percent contribution
speaker_lines_per_episode["Percent_Contribution"] = (
    speaker_lines_per_episode["Speaker_Lines"] / speaker_lines_per_episode["Total_Lines"]
) * 100

# Calculate average percent contribution per season
avg_percent_per_season = speaker_lines_per_episode.groupby(["season", "unique_speakers"])["Percent_Contribution"].mean().reset_index()

# Layout: Filters on top
st.title("Speaker Contribution Analysis")

col1, col2 = st.columns([1, 2])  # First column smaller for season, second larger for episodes

# Season filter (single select with "All" option)
seasons = sorted(df_exploded["season"].unique())
selected_season = col1.selectbox("Select Season", ["All"] + seasons)

# Episode filter (multi-select with all selected by default)
if selected_season == "All":
    episodes = sorted(df_exploded["episode"].unique())
else:
    episodes = sorted(df_exploded[df_exploded["season"] == selected_season]["episode"].unique())

selected_episodes = col2.multiselect("Select Episodes", episodes, default=episodes)

# Filter data based on selections
filtered_data = speaker_lines_per_episode[
    ((speaker_lines_per_episode["season"] == selected_season) | (selected_season == "All")) &
    (speaker_lines_per_episode["episode"].isin(selected_episodes))
]

filtered_avg_data = avg_percent_per_season[
    (avg_percent_per_season["season"] == selected_season) | (selected_season == "All")
]

top_25_avg_speakers = filtered_avg_data.nlargest(25, "Percent_Contribution")



fig = px.pie(
    top_25_avg_speakers,
    names="unique_speakers",
    values="Percent_Contribution",
    title="Average Speaker Contribution per Season",
)

# Display the pie charts side by side
st.plotly_chart(fig, use_container_width=True)

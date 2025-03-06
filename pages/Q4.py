import streamlit as st
import plotly.express as px
import pandas as pd
import re
from collections import Counter
from Home import df_exploded

# Title
st.title("Question 4. Most Common Word Per Character Analysis")

stopwords = set([
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours",
    "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers",
    "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves",
    "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are",
    "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does",
    "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until",
    "while", "of", "at", "by", "for", "with", "about", "against", "between", "into",
    "through", "during", "before", "after", "above", "below", "to", "from", "up", "down",
    "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here",
    "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more",
    "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so",
    "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"
])


def preprocess_text(text):
    text = re.sub(r'[^\w\s]', '', text.lower()) 
    words = text.split()  
    words = [word for word in words if word not in stopwords]  
    return words


word_counts = {}
for character, lines in df_exploded.groupby('unique_speakers')['line']:
    all_words = []
    for line in lines:
        all_words.extend(preprocess_text(line))
    word_counts[character] = Counter(all_words)


most_common_words = {char: counts.most_common(1)[0] if counts else ('None', 0) for char, counts in word_counts.items()}


result_df = pd.DataFrame(
    [(char, word, count) for char, (word, count) in most_common_words.items()],
    columns=['Character', 'Most Common Word', 'Occurrence']
)


st.dataframe(result_df)

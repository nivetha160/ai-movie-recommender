import streamlit as st
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from textblob import TextBlob

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

st.set_page_config(page_title="AI Movie Recommender", layout="centered")

st.title("🎬 AI Movie Recommendation App")
st.write("Upload your reviews CSV file")

uploaded_file = st.file_uploader("Upload CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    def clean_text(text):
        text = text.lower()
        text = re.sub(r'[^a-z\s]', '', text)
        words = text.split()
        words = [w for w in words if w not in stop_words]
        return " ".join(words)

    df['clean_review'] = df['review'].apply(clean_text)
    df['sentiment'] = df['review'].apply(lambda x: TextBlob(x).sentiment.polarity)
    df['norm_rating'] = df['rating'] / 5

    alpha, beta = 0.6, 0.4
    df['final_score'] = alpha * df['norm_rating'] + beta * df['sentiment']

    st.subheader("⭐ Top Recommended Movies")
    st.table(
        df.sort_values(by='final_score', ascending=False)
          [['movie','final_score']]
          .head(3)
    )

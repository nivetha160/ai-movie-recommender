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
st.write("Mood-aware & Explainable AI Recommender")

# ---------------- Upload CSV ----------------
uploaded_file = st.file_uploader("Upload reviews CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # ---------------- Clean Text ----------------
    def clean_text(text):
        text = text.lower()
        text = re.sub(r'[^a-z\s]', '', text)
        words = text.split()
        words = [w for w in words if w not in stop_words]
        return " ".join(words)

    df['clean_review'] = df['review'].apply(clean_text)

    # ---------------- Sentiment ----------------
    df['sentiment'] = df['review'].apply(lambda x: TextBlob(x).sentiment.polarity)

    # ---------------- USER CONTROLS ----------------
    st.subheader("🎛 Customize Recommendation")

    mood = st.selectbox(
        "Select your mood",
        ["😊 Happy", "😢 Sad", "🤔 Thoughtful"]
    )

    alpha = st.slider(
        "Rating Importance",
        min_value=0.0,
        max_value=1.0,
        value=0.6
    )
    beta = 1 - alpha

    top_n = st.selectbox("Number of recommendations", [3, 5, 10])

    # ---------------- Mood Filter ----------------
    if mood == "😊 Happy":
        df = df[df['sentiment'] > 0]
    elif mood == "😢 Sad":
        df = df[df['sentiment'] < 0]

    # ---------------- Fusion Score ----------------
    df['norm_rating'] = df['rating'] / 5
    df['final_score'] = alpha * df['norm_rating'] + beta * df['sentiment']

    # ---------------- Explainable AI ----------------
    def explain(row):
        if row['sentiment'] > 0.4:
            return "Highly positive reviews"
        elif row['sentiment'] > 0:
            return "Positive feedback"
        elif row['sentiment'] < 0:
            return "Negative reviews reduced score"
        else:
            return "Neutral reviews"

    df['reason'] = df.apply(explain, axis=1)

    # ---------------- Show Output ----------------
    st.subheader("⭐ Recommended Movies")
    st.table(
        df.sort_values(by='final_score', ascending=False)
          [['movie', 'final_score', 'reason']]
          .head(top_n)
    )

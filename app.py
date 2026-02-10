import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="Book Recommender", layout="centered")

st.title("📚 AI Book Recommendation System")

uploaded_file = st.file_uploader("Upload reviews.csv", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("📄 Dataset Preview")
    st.dataframe(df.head())

    # Combine book name + review
    df["content"] = df["book"] + " " + df["review"]

    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(df["content"])

    similarity = cosine_similarity(tfidf_matrix)

    st.subheader("🔍 Choose a Book")
    selected_book = st.selectbox("Select book", df["book"].unique())

    if st.button("Recommend Books"):
        idx = df[df["book"] == selected_book].index[0]

        scores = list(enumerate(similarity[idx]))
        scores = sorted(scores, key=lambda x: x[1], reverse=True)

        recommended_books = []
        for i in scores[1:6]:
            book_name = df.iloc[i[0]]["book"]
            if book_name not in recommended_books:
                recommended_books.append(book_name)

        st.subheader("✨ Recommended Books")
        for book in recommended_books:
            st.write("📘", book)

import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(page_title="AI Book Recommender", layout="wide")

st.title("📚 AI Book Recommendation System")

uploaded_file = st.file_uploader("Upload reviews.csv", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("📄 Dataset Preview")
    st.dataframe(df)

    # Filters
    st.sidebar.header("🔎 Filters")
    min_rating = st.sidebar.slider("Minimum Rating", 1, 5, 4)
    selected_genre = st.sidebar.selectbox(
        "Select Genre",
        ["All"] + sorted(df["genre"].unique())
    )

    filtered_df = df[df["rating"] >= min_rating]
    if selected_genre != "All":
        filtered_df = filtered_df[filtered_df["genre"] == selected_genre]

    # Text similarity
    filtered_df["content"] = filtered_df["book"] + " " + filtered_df["review"]

    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(filtered_df["content"])

    similarity = cosine_similarity(tfidf_matrix)

    st.subheader("📘 Choose a Book")
    selected_book = st.selectbox(
        "Select book",
        filtered_df["book"].unique()
    )

    if st.button("✨ Recommend Books"):
        idx = filtered_df[filtered_df["book"] == selected_book].index[0]
        scores = list(enumerate(similarity[list(filtered_df.index).index(idx)]))
        scores = sorted(scores, key=lambda x: x[1], reverse=True)

        st.subheader("🔥 Recommended Books")

        shown = set()
        for i in scores[1:6]:
            book_row = filtered_df.iloc[i[0]]
            if book_row["book"] not in shown:
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.image(book_row["image_url"], width=120)
                with col2:
                    st.write(f"📗 **{book_row['book']}**")
                    st.write(f"⭐ Rating: {book_row['rating']}")
                    st.write(f"📂 Genre: {book_row['genre']}")
                shown.add(book_row["book"])

else:
    st.info("👆 Upload reviews.csv to start")


import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Book Recommender App",
    page_icon="📚",
    layout="centered"
)

st.title("📚 Book Recommendation App")
st.write("Upload CSV and get book recommendations")

uploaded_file = st.file_uploader("Upload reviews.csv", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.success("✅ File uploaded successfully")


    # 🔒 Auto-detect column names
    book_col = None
    genre_col = None
    rating_col = None

    for col in df.columns:
        if col.lower() in ["book", "title", "book_name"]:
            book_col = col
        if col.lower() == "genre":
            genre_col = col
        if col.lower() == "rating":
            rating_col = col

    if book_col is None or genre_col is None or rating_col is None:
        st.error("❌ CSV must have book/title, genre, rating columns")
    else:
        st.subheader("📖 Dataset")
        st.dataframe(df)

        # Search
        search = st.text_input("🔍 Search book")

        if search:
            results = df[df[book_col].str.contains(search, case=False, na=False)]
        else:
            results = df

        book_list = results[book_col].unique().tolist()

        if book_list:
            selected_book = st.selectbox("Select a book", book_list)

            if selected_book:
                row = df[df[book_col] == selected_book].iloc[0]
                genre = row[genre_col]

                st.info(f"📌 Genre: {genre}")

                recommendations = df[
                    (df[genre_col] == genre) &
                    (df[book_col] != selected_book) &
                    (df[rating_col] >= 4)
                ]

                st.subheader("📚 Recommended Books")

                if recommendations.empty:
                    st.warning("No recommendations found")
                else:
                    st.dataframe(
                        recommendations[[book_col, genre_col, rating_col]]
                    )
        else:
            st.warning("No books found")

else:
    st.info("👆 Please upload a CSV file")


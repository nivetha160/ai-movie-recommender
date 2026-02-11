import streamlit as st
import pandas as pd

# ------------------------
# Page configuration
# ------------------------
st.set_page_config(
    page_title="Book Recommender App",
    page_icon="📚",
    layout="centered"
)

st.title("📚 Book Recommendation App")
st.write("Upload a CSV file and get book recommendations based on genre and rating.")

# ------------------------
# File uploader
# ------------------------
uploaded_file = st.file_uploader("Upload reviews.csv", type=["csv"])

if uploaded_file is not None:
    uploaded_file.seek(0)
    df = pd.read_csv(uploaded_file)

    st.success("✅ File uploaded successfully")

    # ------------------------
    # Auto-detect columns
    # ------------------------
    book_col = None
    genre_col = None
    rating_col = None

    for col in df.columns:
        if col.lower() in ["book", "title", "book_name"]:
            book_col = col
        elif col.lower() == "genre":
            genre_col = col
        elif col.lower() == "rating":
            rating_col = col

    if book_col is None or genre_col is None or rating_col is None:
        st.error("❌ CSV must have columns: book/title, genre, rating")
    else:
        # Ensure ratings are numeric
        df[rating_col] = pd.to_numeric(df[rating_col], errors='coerce')

        # ------------------------
        # NOTE: Dataset will NOT be shown
        # ------------------------
        # st.dataframe(df)  <-- intentionally hidden

        # ------------------------
        # Search book
        # ------------------------
        search = st.text_input("🔍 Search book by name")

        if search:
            results = df[df[book_col].str.contains(search, case=False, na=False)]
        else:
            results = df

        book_list = results[book_col].dropna().unique().tolist()

        if book_list:
            selected_book = st.selectbox("Select a book", book_list)

            if selected_book:
                row = df[df[book_col] == selected_book].iloc[0]
                genre = row[genre_col]

                st.info(f"📌 Genre: {genre}")

                # ------------------------
                # Recommendations
                # ------------------------
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
                        recommendations[[book_col, genre_col, rating_col]],
                        height=300
                    )
        else:
            st.warning("No books found matching your search")
else:
    st.info("👆 Please upload a CSV file with columns: book/title, genre, rating")


)


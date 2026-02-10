import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Book Recommender",
    page_icon="📚",
    layout="wide"
)

st.markdown("""
<style>
.card {
    border-radius: 12px;
    padding: 15px;
    margin: 10px 0;
    background: #ffffff;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}
.book-title {
    font-size: 20px;
    font-weight: bold;
}
.genre {
    color: #555;
}
.rating {
    color: #ff9800;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.title("📚 Book Recommender App")
st.caption("Search books & get smart recommendations")

uploaded_file = st.file_uploader("📂 Upload reviews.csv", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("✅ File uploaded")

    search = st.text_input("🔍 Search book name")

    if search:
        results = df[df["book"].str.contains(search, case=False)]

        if results.empty:
            st.warning("❌ No book found")
        else:
            st.subheader("📖 Search Results")

            book_list = results["book"].unique().tolist()
            selected_book = st.selectbox("Select a book", book_list)

            if selected_book:
                book_row = df[df["book"] == selected_book].iloc[0]
                genre = book_row["genre"]

                st.markdown(f"""
                <div class="card">
                    <div class="book-title">{book_row['book']}</div>
                    <div class="genre">Genre: {genre}</div>
                    <div class="rating">⭐ Rating: {book_row['rating']}</div>
                </div>
                """, unsafe_allow_html=True)

                st.subheader("📚 Recommended Books")

                recs = df[
                    (df["genre"] == genre) &
                    (df["book"] != selected_book) &
                    (df["rating"] >= 4)
                ]

                if recs.empty:
                    st.info("No similar books found")
                else:
                    for _, row in recs.iterrows():
                        st.markdown(f"""
                        <div class="card">
                            <div class="book-title">{row['book']}</div>
                            <div class="genre">Genre: {row['genre']}</div>
                            <div class="rating">⭐ Rating: {row['rating']}</div>
                        </div>
                        """, unsafe_allow_html=True)
    else:
        st.info("✍️ Type a book name to search")
else:
    st.info("⬆️ Upload CSV to start")


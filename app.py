import streamlit as st
import pandas as pd

st.set_page_config(page_title="Book Recommender Test")

st.title("📚 AI Book Recommender – Test Page")

st.write("If you are seeing this page, Streamlit is working perfectly ✅")

st.subheader("Sample Book Table")

data = {
    "Book": ["Harry Potter", "Atomic Habits", "The Alchemist"],
    "Rating": [5, 4, 5],
    "Genre": ["Fantasy", "Self Help", "Fiction"]
}

df = pd.DataFrame(data)
st.table(df)

st.success("🎉 App loaded successfully!")

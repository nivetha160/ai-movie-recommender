import streamlit as st
import pandas as pd

st.set_page_config(page_title="Review Analyzer", layout="centered")

st.title("📱 Review Analyzer App")
st.write("Upload your **reviews.csv** file")

# File upload
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        st.success("✅ File uploaded successfully!")
        st.subheader("📄 Preview")
        st.dataframe(df)

        # Basic analysis
        if "rating" in df.columns:
            avg_rating = df["rating"].mean()
            st.subheader("⭐ Average Rating")
            st.write(round(avg_rating, 2))

        # New feature: sentiment
        st.subheader("🧠 Simple Sentiment Check")

        def sentiment(text):
            text = text.lower()
            if "good" in text or "excellent" in text:
                return "Positive 😊"
            elif "bad" in text or "worst" in text:
                return "Negative 😡"
            else:
                return "Neutral 😐"

        if "review" in df.columns:
            df["Sentiment"] = df["review"].apply(sentiment)
            st.dataframe(df)

    except Exception as e:
        st.error("❌ Error reading file")
        st.write(e)
else:
    st.info("📂 Please upload reviews.csv")

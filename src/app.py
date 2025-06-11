import streamlit as st
import pandas as pd
import docx
import PyPDF2
import plotly.express as px
from utils import process_batch, export_results
from sentiment import analyze_sentiment
from keyword_extraction import extract_keywords

# -------------- File Uploader and Input Options --------------
st.set_page_config(page_title="Sentiment Analysis Dashboard", layout="wide")
st.title("📊 Sentiment Analysis Dashboard")
st.markdown("Analyze sentiment from **text**, **PDF**, **Word**, or **CSV** files with confidence scoring, keyword extraction, and detailed explanations.")

# Sidebar for instructions
with st.sidebar:
    st.header("ℹ️ How to Use")
    st.markdown("""
    1. Upload a file or type your text.
    2. Click **Analyze**.
    3. Review the sentiment scores and keywords.
    4. Expand **Detailed Explanations** for insights.
    5. Download results in PDF, DOCX, or CSV format.
    """)

col1 , col2 = st.columns(2)
with col1:
    uploads = st.file_uploader(
        "Upload a one or more files", 
        type=["csv", "txt", "pdf", "docx"], accept_multiple_files=True
    )
with col2:
    sample_text = st.text_area("Or enter a single text to analyze")

# -------------- Read and Process Uploaded Files ----------------- 
def read_uploaded_file(upload):
    if upload.name.endswith(".csv"):
        df = pd.read_csv(upload)
        return df["text"].tolist() if "text" in df.columns else None
    elif upload.name.endswith(".txt"):
        text = upload.read().decode("utf-8")
        return text.split("\n")
    elif upload.name.endswith(".docx"):
        doc = docx.Document(upload)
        return [para.text for para in doc.paragraphs if para.text.strip()]
    elif upload.name.endswith(".pdf"):
        reader = PyPDF2.PdfReader(upload)
        text = [page.extract_text() for page in reader.pages]
        return [line for page in text for line in page.split("\n") if line.strip()]
    else:
        return None



# -------------- Main Action Button --------------------------
if st.button("Analyze"):
    if uploads:
        all_dfs = []
        for upload in uploads:
            texts = read_uploaded_file(upload)
            if texts:
                df = pd.DataFrame(texts, columns=["text"])
                df["source"] = upload.name
                results = process_batch(df, "text")
                # Ensure 'sentiment' column exists
                if "sentiment" not in results.columns:
                    st.error(f"No 'sentiment' column found in results for file: {upload.name}")
                else:
                    all_dfs.append(results)
            else:
                st.error(f"Unsupported or malformed file: {upload.name}")
        
        if all_dfs:
            full_df = pd.concat(all_dfs, ignore_index=True)
            st.subheader("🔍 Analysis Results")
            st.dataframe(full_df)
            if "sentiment" in full_df.columns:
                with st.expander("🔎 View Detailed Sentiment Explanations"):
                    sentiment_icon = {
                        "positive": "😊",
                        "neutral": "😐",
                        "negative": "😠"
                    }
                    sentiment_color = {
                        "positive": "green",
                        "neutral": "gray",
                        "negative": "red"
                    }
                
                    for i, row in full_df.iterrows():
                       
                        sent = row['sentiment'].lower()  # Normalize sentiment to lowercase
                        st.markdown(
                        f"### {sentiment_icon[sent]} Text {i+1}: "
                        f"<span style='color:{sentiment_color[sent]}'>**{row['sentiment'].capitalize()}**</span>",
                        unsafe_allow_html=True)

                        with st.container():
                            st.markdown(f"**🧾 Original Text:** {row['text']}")
                            st.markdown(f"**📊 Sentiment:** {row['sentiment']}  \n**🎯 Confidence:** {row['confidence']}")
                            st.markdown(f"**🔑 Keywords:** {row['keywords']}")
                            st.markdown(f"**🧠 Explanation:** {row['explanation']}")
            else:
                st.error("No 'sentiment' column found in the combined results. Please check your processing pipeline.")
            
            # Export results
            export_results(full_df)

            # Sentiment Distribution
            sentiment_counts = full_df["sentiment"].value_counts().reset_index()
            sentiment_counts.columns = ["Sentiment", "Count"]
            dist_fig = px.bar(sentiment_counts, x="Sentiment", y="Count", color="Sentiment", title="Sentiment Distribution")
            st.plotly_chart(dist_fig)

            # Comparative Sentiment by Source
            if "source" in full_df.columns and full_df["source"].nunique() > 1:
                compare_fig = px.histogram(
                    full_df, 
                    x="sentiment", 
                    color="source", 
                    barmode="group", 
                    title="Sentiment Comparison by File"
                )
                st.plotly_chart(compare_fig)

            

    elif sample_text.strip():
        st.subheader("🔍 Single Text Analysis")
        label, score = analyze_sentiment(sample_text)
        keywords = extract_keywords(sample_text)
        st.markdown(f"**Sentiment**: {label} | **Confidence**: {score}")
        st.markdown(f"**Keywords**: {', '.join(keywords)}")
    else:
        st.warning("Please provide input via file upload or text box.")
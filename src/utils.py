import pandas as pd
from io import BytesIO
from docx import Document
from fpdf import FPDF
import streamlit as st
from sentiment import analyze_sentiment
from keyword_extraction import extract_keywords

def process_batch(df, text_col):
    results = []
    
    for text in df[text_col]:
        sentiment, confidence = analyze_sentiment(text)
        keywords = extract_keywords(text)
        explanation = f"The sentiment was determined based on these keywords: {', '.join(keywords)}"
        results.append({
            "text": text,
            "sentiment": sentiment,
            "confidence": confidence,
            "keywords": ", ".join(keywords),
             "explanation": explanation
        })
    return pd.DataFrame(results)

def export_results(df):
    st.markdown("### 📤 Export Results")

    # Export CSV
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download CSV", data=csv, file_name="sentiment_results.csv", mime="text/csv")

    # Export DOCX
    docx_buffer = BytesIO()
    doc = Document()
    table = doc.add_table(rows=1, cols=len(df.columns))
    hdr_cells = table.rows[0].cells
    for i, col in enumerate(df.columns):
        hdr_cells[i].text = col

    for _, row in df.iterrows():
        row_cells = table.add_row().cells
        for i, item in enumerate(row):
            row_cells[i].text = str(item)

    doc.save(docx_buffer)
    st.download_button("Download DOCX", data=docx_buffer.getvalue(), file_name="sentiment_results.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

    # Export PDF
    pdf_buffer = BytesIO()
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    col_names = " | ".join(df.columns)
    pdf.multi_cell(0, 10, col_names)
    for _, row in df.iterrows():
        row_data = " | ".join([str(item) for item in row])
        pdf.multi_cell(0, 10, row_data)
    pdf_bytes = pdf.output(dest='S').encode('latin-1')  # 'S' = return as string
    pdf_io = BytesIO(pdf_bytes)
    st.download_button("Download PDF", data=pdf_io, file_name="sentiment_results.pdf", mime="application/pdf")

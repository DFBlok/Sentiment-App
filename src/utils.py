import pandas as pd
from io import BytesIO
from docx import Document
from fpdf import FPDF
import streamlit as st
import unicodedata
from sentiment import analyze_sentiment
from keyword_extraction import extract_keywords

def clean_text(text):
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')

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

    """ for i in range(len(pdf.pages)):
        pdf.pages[i] = clean_text(pdf.pages[i])
    pdf_bytes = pdf.output(dest='S').encode('latin-1')  # 'S' = return as string """
    

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
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)

    col_names = " | ".join([clean_text(col) for col in df.columns])
    pdf.multi_cell(0, 10, col_names)

    for _, row in df.iterrows():
        """ row_data = " | ".join([str(item) for item in row]) """
        row_data = " | ".join([clean_text(str(item)) for item in row])
        """ safe_row_data = row_data.encode('ascii', 'ignore').decode('ascii') """
        pdf.multi_cell(0, 10, row_data)


    pdf_bytes = pdf.output(dest='S').encode('latin-1')  # 'S' = return as string
    pdf_io = BytesIO(pdf_bytes)

    st.download_button(
        label="Download PDF",
        data=pdf_io,
        file_name="sentiment_results.pdf", mime="application/pdf")
    

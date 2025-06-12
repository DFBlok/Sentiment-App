# 📊 Sentiment Analysis Dashboard

An interactive NLP-powered sentiment analysis web application that analyzes input text or uploaded documents, visualizes results, and allows exporting in multiple formats. Built with **Streamlit** and powered by **Hugging Face Transformers**.

**🔗 Live App:** [https://dfblok-sentiment-app-srcapp-fwvh5u.streamlit.app/](https://dfblok-sentiment-app-srcapp-fwvh5u.streamlit.app/)  
**📁 GitHub Repository:** [Insert your GitHub repo link here]

---

## 🚀 Features

- ✅ Text input and file uploads (`.csv`, `.pdf`, `.docx`, `.txt`)
- 🔄 Batch sentiment processing
- 🧠 Multi-class sentiment classification: **Positive**, **Neutral**, **Negative**
- 🎯 Confidence scoring for each prediction
- 🗝️ Keyword extraction and explanation of sentiment drivers
- 📊 Visualizations (distribution graphs, icons, cues)
- 🔍 Comparative analysis across multiple sources
- 🧾 Export results as **CSV**, **PDF**, or **DOCX**
- 🧰 Error handling and validation

---

## 📦 Setup Instructions

### 🔧 Requirements

- Python 3.8+
- pip (Python package manager)

### 🛠 Installation

```bash
# Clone the repository
git clone https://github.com/DFBlok/Sentiment-App

# Navigate to the app
cd sentiment-dashboard/src

# (Optional) Create and activate virtual environment
python -m venv venv
source venv/bin/activate       # For macOS/Linux
venv\Scripts\activate          # For Windows

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py


# 🎥 Demo Video Outline


# 📘 Example Usage
Upload a .csv with a text column OR paste a paragraph manually

Click Analyze

Expand results for explanations and keywords

View sentiment graphs

Download PDF, CSV, or DOCX results

# 🙌 Contributing
Feel free to open issues, suggest improvements, or contribute to the project via PRs.

# 📄 License
MIT License. See LICENSE for details.
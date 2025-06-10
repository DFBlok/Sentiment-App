from transformers import pipeline

# Load the sentiment analysis pipeline
sentiment_pipeline = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")

label_map = {
    "LABEL_0": "Negative",
    "LABEL_1": "Neutral",
    "LABEL_2": "Positive"
}



def analyze_sentiment(text):
    result = sentiment_pipeline(text)[0]
    label = label_map[result['label']]
    score = round(result['score'], 3)
    return label, score
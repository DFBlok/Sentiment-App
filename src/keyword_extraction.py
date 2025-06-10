import yake

# Initialize keyword extractor
kw_extractor = yake.KeywordExtractor(top=5, stopwords=None)

def extract_keywords(text):
    keywords = kw_extractor.extract_keywords(text)
    return [kw for kw, _ in keywords]
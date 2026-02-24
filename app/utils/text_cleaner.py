import spacy
import re

# Load English model
nlp = spacy.load("en_core_web_sm")

def clean_text(text):
    text = text.lower()

    # Remove special characters and numbers
    text = re.sub(r'[^a-z\s]', '', text)

    doc = nlp(text)

    cleaned_tokens = []

    for token in doc:
        if not token.is_stop and not token.is_punct:
            cleaned_tokens.append(token.lemma_)

    return " ".join(cleaned_tokens)
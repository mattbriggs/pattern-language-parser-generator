import nltk
import logging
from sentence_transformers import SentenceTransformer


def download_nltk_resources():
    try:
        nltk.data.find("tokenizers/punkt")
        logging.info("NLTK 'punkt' tokenizer is already available.")
    except LookupError:
        logging.info("Downloading NLTK 'punkt' tokenizer...")
        nltk.download("punkt")


def test_sentence_transformer_model(model_name="all-MiniLM-L6-v2"):
    try:
        _ = SentenceTransformer(model_name)
        logging.info(f"SentenceTransformer model '{model_name}' is available.")
    except Exception as e:
        logging.error(f"Failed to load SentenceTransformer model: {e}")

def ensure_nltk_resource(resource):
    try:
        nltk.data.find(resource)
    except LookupError:
        print(f"📦 Downloading missing resource: {resource}")
        nltk.download(resource.split("/")[-1])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info("📦 Checking NLP resources for Pattern Language Miner...")
    download_nltk_resources()
    ensure_nltk_resource('tokenizers/punkt')
    ensure_nltk_resource('taggers/averaged_perceptron_tagger')
    test_sentence_transformer_model()
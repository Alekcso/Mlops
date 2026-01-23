# src/preprocessing.py

import os
import re
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


# ============================================================
# NLTK initialization (lazy)
# ============================================================

_stop_words = None
_lemmatizer = None


def init_nltk():
    """Initialize NLTK resources once."""
    global _stop_words, _lemmatizer

    if _stop_words is not None and _lemmatizer is not None:
        return  # already loaded

    nltk.download('stopwords', quiet=True)
    nltk.download('wordnet', quiet=True)
    nltk.download('omw-1.4', quiet=True)

    _stop_words = set(stopwords.words('english'))
    _lemmatizer = WordNetLemmatizer()


# ============================================================
# Text cleaning
# ============================================================

def clean_text(text: str) -> str:
    """Complete cleaning pipeline."""
    init_nltk()

    text = str(text).lower()

    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)

    # Remove HTML
    text = re.sub(r'<.*?>', '', text)

    # Keep only letters and spaces
    text = re.sub(r'[^a-z\s]', '', text)

    tokens = text.split()

    cleaned_tokens = [
        _lemmatizer.lemmatize(word)
        for word in tokens
        if word not in _stop_words
    ]

    return " ".join(cleaned_tokens)


# ============================================================
# VERSION 1: Base dataset
# ============================================================

def make_binary_dataset(raw_csv_path: str, out_path: str) -> pd.DataFrame:
    """Create binary dataset with sentiment."""
    df = pd.read_csv(raw_csv_path)

    df["sentiment"] = df["score"].apply(lambda x: "negative" if x <= 2 else "positive")
    df = df.dropna(subset=["content"])
    df = df.drop_duplicates(subset=["content"])

    df["content"] = df["content"].str.lower()
    df["review_length"] = df["content"].apply(lambda x: len(str(x).split()))

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    df.to_csv(out_path, index=False)

    return df


def make_clean_dataset_v1(binary_csv_path: str, out_path: str) -> pd.DataFrame:
    """
    Version 1: standard cleaning
    """
    df = pd.read_csv(binary_csv_path)

    df["clean_text"] = df["content"].apply(clean_text)
    df["clean_length"] = df["clean_text"].apply(lambda x: len(str(x).split()))

    # remove empty
    df = df[df["clean_length"] > 0]

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    df.to_csv(out_path, index=False)
    return df


# ============================================================
# VERSION 2: Modified preprocessing
# ============================================================

def make_clean_dataset_v2(binary_csv_path: str, out_path: str) -> pd.DataFrame:
    """
    Version 2: more strict cleaning
    - filter out very short cleaned texts (<=3 words)
    """
    df = pd.read_csv(binary_csv_path)

    df["clean_text"] = df["content"].apply(clean_text)
    df["clean_length"] = df["clean_text"].apply(lambda x: len(str(x).split()))

    # VERSION 2 DIFFERENCE:
    df = df[df["clean_length"] > 3]   # KEY CHANGE vs V1

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    df.to_csv(out_path, index=False)
    return df


# ============================================================
# 3-class label generation (used for both versions)
# ============================================================

def make_3class_dataset(clean_csv_path: str, out_path: str) -> pd.DataFrame:
    """Create 3-class labels."""
    df = pd.read_csv(clean_csv_path)

    def map_3(score):
        if score == 1:
            return "negative"
        elif score in [2, 3, 4]:
            return "neutral"
        else:
            return "positive"

    df["sentiment_3class"] = df["score"].apply(map_3)

    df.to_csv(out_path, index=False)
    return df


# ============================================================
# MAIN script
# ============================================================

if __name__ == "__main__":
    """
    Run preprocessing:
    python -m src.preprocessing
    """

    RAW = "data/raw/netflix_reviews.csv"

    # Binary dataset (common for both versions)
    BINARY = "data/processed/reviews_binary.csv"
    df_bin = make_binary_dataset(RAW, BINARY)

    # Version 1
    CLEAN_V1 = "data/processed/reviews_binary_clean_v1.csv"
    df_clean_v1 = make_clean_dataset_v1(BINARY, CLEAN_V1)

    THREECLASS_V1 = "data/processed/reviews_3class_clean_v1.csv"
    df_3cls_v1 = make_3class_dataset(CLEAN_V1, THREECLASS_V1)

    # Version 2
    CLEAN_V2 = "data/processed/reviews_binary_clean_v2.csv"
    df_clean_v2 = make_clean_dataset_v2(BINARY, CLEAN_V2)

    THREECLASS_V2 = "data/processed/reviews_3class_clean_v2.csv"
    df_3cls_v2 = make_3class_dataset(CLEAN_V2, THREECLASS_V2)

    # Logs
    print("V1 Clean:", df_clean_v1.shape)
    print("V2 Clean:", df_clean_v2.shape)
    print("3-class V1:", df_3cls_v1["sentiment_3class"].value_counts().to_dict())
    print("3-class V2:", df_3cls_v2["sentiment_3class"].value_counts().to_dict())


from fastapi import FastAPI
from pydantic import BaseModel
import joblib

# Загружаем обученные модели
model_binary = joblib.load("models/model_lr_binary.pkl")
vec_binary = joblib.load("models/tfidf_vectorizer_binary.pkl")
model_3class = joblib.load("models/model_lr_3class.pkl")
vec_3class = joblib.load("models/tfidf_vectorizer_3class.pkl")

app = FastAPI(title="Netflix Sentiment API")

class InputText(BaseModel):
    text: str
    mode: str = "binary"  # "binary" или "3class"

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(data: InputText):
    text = [data.text]
    if data.mode == "3class":
        X = vec_3class.transform(text)
        pred = model_3class.predict(X)[0]
    else:
        X = vec_binary.transform(text)
        pred = model_binary.predict(X)[0]
    return {"sentiment": pred, "mode": data.mode}

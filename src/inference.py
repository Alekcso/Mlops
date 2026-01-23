# src/inference.py
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import yaml

# -------------------------------------------------------------------
# 1. Читаем конфиг inference
# -------------------------------------------------------------------
with open("configs/inference.yaml", "r") as f:
    cfg = yaml.safe_load(f)

inf_cfg = cfg["inference"]

BINARY_MODEL_PATH = inf_cfg["binary_model_path"]
CLASS3_MODEL_PATH = inf_cfg["class3_model_path"]

# -------------------------------------------------------------------
# 2. Загружаем PIPLINE-модели (vectorizer внутри)
# -------------------------------------------------------------------
model_binary = joblib.load(BINARY_MODEL_PATH)
model_3class = joblib.load(CLASS3_MODEL_PATH)

# -------------------------------------------------------------------
# 3. FastAPI-приложение
# -------------------------------------------------------------------
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
        pred = model_3class.predict(text)[0]
    else:
        pred = model_binary.predict(text)[0]

    return {"sentiment": pred, "mode": data.mode}


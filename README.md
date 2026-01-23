# Netflix Sentiment Analysis — MLOps Project

## 1. Описание проекта
Проект демонстрирует полный MLOps-пайплайн:
- подготовка и версионирование данных,
- обучение моделей через MLflow,
- сравнение экспериментов,
- FastAPI-инференс,
- Gradio UI (опционально),
- Docker-деплой,
- документация (Model Card, Dataset Card, Pipeline Diagram).

Модель работает в двух режимах:
- binary — positive / negative
- 3-class — positive / neutral / negative

---

## 2. Структура проекта

mlops-sentiment-netflix/  
├── src/  
│   ├── preprocessing.py  
│   ├── train.py  
│   └── inference.py  
├── configs/  
│   ├── exp1.yaml  
│   ├── exp2.yaml  
│   ├── exp3.yaml  
│   └── inference.yaml  
├── models/  
├── data/  
│   ├── raw/  
│   └── processed/  
├── reports/  
│   └── mlflow/  
├── MODEL_CARD.md  
├── DATASET_CARD.md  
├── pipeline-diagram.md  
├── Dockerfile  
└── README.md

---

## 3. Установка окружения

python -m venv .venv  
.\.venv\Scripts\activate  
pip install -r requirements.txt

---

## 4. Препроцессинг данных

python -m src.preprocessing

Создаются файлы:
- reviews_binary_clean_v1.csv  
- reviews_binary_clean_v2.csv  
- reviews_3class_clean_v1.csv  
- reviews_3class_clean_v2.csv  

---

## 5. Обучение моделей (MLflow)

### 5.1 MLflow UI

mlflow ui --port 5001  
http://127.0.0.1:5001

### 5.2 Эксперименты

python -m src.train --config configs/exp1.yaml  
python -m src.train --config configs/exp2.yaml  
python -m src.train --config configs/exp3.yaml  

Создаётся:
- model_exp1.pkl / model_exp2.pkl / model_exp3.pkl  
- ONNX-версии (не используются в инференсе)  
- записи в mlruns/

---

## 6. Docker

### Сборка

docker build -t netflix-sentiment-api .

### Запуск

docker run -p 8000:8000 netflix-sentiment-api

FastAPI:

http://127.0.0.1:8000

---

## 7. FastAPI — инференс

### Проверка

curl http://127.0.0.1:8000/health

### Binary

curl -X POST "http://127.0.0.1:8000/predict" ^
     -H "Content-Type: application/json" ^
     -d "{\"text\":\"I liked this movie\", \"mode\":\"binary\"}"

### 3-class

curl -X POST "http://127.0.0.1:8000/predict" ^
     -H "Content-Type: application/json" ^
     -d "{\"text\":\"The plot was boring\", \"mode\":\"3class\"}"

Swagger:  
http://127.0.0.1:8000/docs

---

## 8. Gradio UI (опционально)

cd C:\Users\sergb\Py2025\09-Sep\Big_Data\mlops-sentiment-netflix  
.\.venv\Scripts\activate  
python src/ui.py

UI:

http://127.0.0.1:7860

---

## 9. Документация
MODEL_CARD.md  
DATASET_CARD.md  
pipeline-diagram.md  

---

## 10. Видео-демо
Показать:
- docker build  
- docker run  
- /health  
- /predict  
- /docs  

---

## 11. Автор
ALEX


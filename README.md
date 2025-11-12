# mlops-sentiment-netflix
ECHO is off.
Netflix review sentiment analysis MLOps project.
ECHO is off.
## Quick Start
1. python -m venv .venv
2. .\.venv\Scripts\Activate
3. pip install -r requirements.txt
4. python -m src.preprocessing
5. python -m src.train
6. uvicorn src.inference:app --host 0.0.0.0 --port 8000 --reload

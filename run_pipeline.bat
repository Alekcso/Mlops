@echo off
setlocal

echo ---------------------------------------------
echo    RUNNING FULL MLOPS PIPELINE
echo ---------------------------------------------

cd /d "C:\Users\akimo\OneDrive\Desktop\mlops-sentiment-netflix"

:: Activate venv
call .\.venv\Scripts\activate

:: Step 1. Preprocessing
echo [1/3] Data preprocessing...
python -m src.preprocessing

:: Step 2. Model training
echo [2/3] Training models...
python -m src.train

:: Step 3. Start API (in new window)
echo [3/3] Starting FastAPI service...
start cmd /k "uvicorn src.inference:app --host 0.0.0.0 --port 8000 --reload"

echo ---------------------------------------------
echo PIPELINE COMPLETE
echo Service available at:
echo   http://127.0.0.1:8000/health
echo   http://127.0.0.1:8000/docs
echo ---------------------------------------------
pause

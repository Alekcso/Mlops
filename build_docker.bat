@echo off
setlocal

echo ---------------------------------------------
echo    BUILDING DOCKER IMAGE FOR MLOPS PROJECT
echo ---------------------------------------------

cd /d "C:\Users\akimo\OneDrive\Desktop\mlops-sentiment-netflix"

:: Check Docker
docker --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker not found! Install Docker Desktop first.
    pause
    exit /b
)

:: Create Dockerfile if missing
if not exist "Dockerfile" (
(
echo FROM python:3.10-slim
echo WORKDIR /app
echo COPY requirements.txt .
echo RUN pip install --no-cache-dir -r requirements.txt
echo COPY src ./src
echo COPY models ./models
echo EXPOSE 8000
echo CMD ["uvicorn", "src.inference:app", "--host", "0.0.0.0", "--port", "8000"]
) > Dockerfile
)

:: Build image
docker build -t netflix-sentiment-api .

:: Run container
docker run -d -p 8000:8000 --name sentiment_service netflix-sentiment-api

echo ---------------------------------------------
echo DOCKER CONTAINER RUNNING
echo Open:
echo   http://127.0.0.1:8000/health
echo   http://127.0.0.1:8000/docs
echo ---------------------------------------------
pause

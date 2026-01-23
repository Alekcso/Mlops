@echo off
setlocal

echo ---------------------------------------------
echo   BOOTSTRAPPING MLOPS SENTIMENT PROJECT
echo ---------------------------------------------

cd /d "C:\Users\akimo\OneDrive\Desktop\mlops-sentiment-netflix"

:: Step 1. Create venv if missing
if not exist ".venv\" (
    echo [INFO] Creating virtual environment...
    python -m venv .venv
) else (
    echo [INFO] Virtual environment already exists.
)

:: Step 2. Activate
call .\.venv\Scripts\activate

:: Step 3. Install dependencies
if exist "requirements.txt" (
    echo [INFO] Installing dependencies...
    pip install --upgrade pip
    pip install -r requirements.txt
) else (
    echo [WARN] No requirements.txt found.
)

:: Step 4. Initialize Git
git --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Git not found! Install from https://git-scm.com/download/win
    pause
    exit /b
)
if not exist ".git\" (
    git init
)

:: Step 5. Create .gitignore if missing
if not exist ".gitignore" (
(
echo .venv/
echo __pycache__/
echo *.pyc
echo data/processed/
echo logs/
echo models/
echo mlruns/
echo .vscode/
echo .idea/
echo .DS_Store
) > .gitignore
)

:: Step 6. Create README.md if missing
if not exist "README.md" (
(
echo # mlops-sentiment-netflix
echo
echo Netflix review sentiment analysis MLOps project.
echo
echo ## Quick Start
echo 1. python -m venv .venv
echo 2. .\.venv\Scripts\Activate
echo 3. pip install -r requirements.txt
echo 4. python -m src.preprocessing
echo 5. python -m src.train
echo 6. uvicorn src.inference:app --host 0.0.0.0 --port 8000 --reload
) > README.md
)

:: Step 7. Git user and commit
git config --global user.name "Sergei"
git config --global user.email "sergei@example.com"
git add .
git commit -m "Project bootstrap: environment, dependencies, Git setup"

echo ---------------------------------------------
echo ✅ BOOTSTRAP COMPLETE
echo ---------------------------------------------
pause

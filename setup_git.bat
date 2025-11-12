@echo off
echo ---------------------------------------------
echo   FULL PROJECT SETUP: ENVIRONMENT + GIT INIT
echo ---------------------------------------------

:: Go to project folder (change if needed)
cd /d "C:\Users\sergb\Py2025\09-Sep\Big_Data\mlops-sentiment-netflix"

:: Check if venv exists
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
) else (
    echo Virtual environment already exists.
)

:: Activate environment
call .\.venv\Scripts\activate

:: Upgrade pip
python -m pip install --upgrade pip

:: Install dependencies if requirements.txt exists
if exist "requirements.txt" (
    echo Installing dependencies...
    pip install -r requirements.txt
) else (
    echo No requirements.txt found!
)

:: Check Git installation
git --version

:: Initialize repository if not yet initialized
if not exist ".git" (
    echo Initializing Git repository...
    git init
) else (
    echo Git repository already initialized.
)

:: Create .gitignore
(
echo # Virtual environment
echo .venv/
echo
echo # Python cache
echo __pycache__/
echo *.pyc
echo
echo # Data and artifacts
echo data/processed/
echo logs/
echo models/
echo mlruns/
echo
echo # IDE and system files
echo .vscode/
echo .idea/
echo .DS_Store
) > .gitignore

:: Create README.md
(
echo # mlops-sentiment-netflix
echo
echo Machine Learning Operations (MLOps) coursework project for Netflix review sentiment analysis.
echo
echo ## Quick Start
echo
echo 1. Create and activate virtual environment:
echo    - python -m venv .venv
echo    - .\.venv\Scripts\Activate
echo
echo 2. Install dependencies:
echo    - pip install -r requirements.txt
echo
echo 3. Run preprocessing:
echo    - python -m src.preprocessing
echo
echo 4. Train model:
echo    - python -m src.train
echo
echo 5. Start inference API:
echo    - uvicorn src.inference:app --host 0.0.0.0 --port 8000 --reload
echo
echo 6. Check endpoints:
echo    - http://127.0.0.1:8000/health
echo    - http://127.0.0.1:8000/docs
) > README.md

:: Configure Git user (only once globally)
git config --global user.name "Sergei"
git config --global user.email "sergei@example.com"

:: Stage and commit files
git add .
git commit -m "Initial full setup: env + git + project files"

:: Show commits
git log --oneline

echo ---------------------------------------------
echo       ✅ FULL PROJECT SETUP COMPLETED
echo ---------------------------------------------
pause

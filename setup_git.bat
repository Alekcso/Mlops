@echo off
echo ---------------------------------------------
echo   ИНИЦИАЛИЗАЦИЯ GIT ПРОЕКТА MLOPS SENTIMENT
echo ---------------------------------------------

:: Переходим в папку проекта (изменить путь под себя)
cd /d "C:\Users\sergb\Py2025\09-Sep\Big_Data\mlops-sentiment-netflix"

:: Активируем виртуальное окружение
call .\.venv\Scripts\activate

:: Проверка Git
git --version

:: Инициализация репозитория
git init

:: Создание .gitignore
echo # Виртуальное окружение > .gitignore
echo .venv/>> .gitignore
echo # Кэш Python >> .gitignore
echo __pycache__/ >> .gitignore
echo *.pyc >> .gitignore
echo # Данные и артефакты >> .gitignore
echo data/processed/ >> .gitignore
echo logs/ >> .gitignore
echo models/ >> .gitignore
echo mlruns/ >> .gitignore
echo # IDE и служебные файлы >> .gitignore
echo .vscode/ >> .gitignore
echo .idea/ >> .gitignore
echo .DS_Store >> .gitignore

:: Создание README.md
echo # mlops-sentiment-netflix > README.md
echo Курсовой проект по операционализации ML-модели анализа тональности отзывов на Netflix. >> README.md
echo. >> README.md
echo ## Быстрый запуск >> README.md
echo 1. Создать и активировать окружение: >> README.md
echo    - python -m venv .venv >> README.md
echo    - .\.venv\Scripts\Activate >> README.md
echo 2. Установить зависимости: >> README.md
echo    - pip install -r requirements.txt >> README.md
echo 3. Предобработка данных: >> README.md
echo    - python -m src.preprocessing >> README.md
echo 4. Обучение моделей: >> README.md
echo    - python -m src.train >> README.md
echo 5. Запуск сервиса: >> README.md
echo    - uvicorn src.inference:app --host 0.0.0.0 --port 8000 --reload >> README.md
echo 6. Проверка: >> README.md
echo    - http://127.0.0.1:8000/health >> README.md
echo    - http://127.0.0.1:8000/docs >> README.md

:: Настройка имени и почты (делается один раз)
git config --global user.name "Sergei"
git config --global user.email "sergei@example.com"

:: Добавляем файлы и делаем коммит
git add .
git commit -m "Initial project setup: code, data, env, API"

:: Показываем историю
git log --oneline

echo ---------------------------------------------
echo       ✅ GIT НАСТРОЕН И КОММИТ СДЕЛАН
echo ---------------------------------------------
pause

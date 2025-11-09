# mlops-sentiment-netflix

Курсовой проект по операционализации ML-модели анализа тональности отзывов на Netflix.

## Быстрый запуск

1. Создать и активировать окружение:
   - `python -m venv .venv`
   - `.\.venv\Scripts\Activate`
2. Установить зависимости:
   - `pip install -r requirements.txt`
3. Предобработка данных:
   - `python -m src.preprocessing`
4. Обучение моделей:
   - `python -m src.train`
5. Запуск сервиса:
   - `uvicorn src.inference:app --host 0.0.0.0 --port 8000 --reload`
6. Проверка:
   - `http://127.0.0.1:8000/health`
   - `http://127.0.0.1:8000/docs`

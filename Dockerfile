# 1. Базовый образ
FROM python:3.10-slim

# 2. Рабочая директория
WORKDIR /app

# 3. Копируем файлы зависимостей
COPY requirements.txt .

# 4. Установка зависимостей
RUN pip install --no-cache-dir -r requirements.txt \
    && python -m nltk.downloader stopwords \
    && python -m nltk.downloader wordnet \
    && python -m nltk.downloader omw-1.4

# 5. Создаём директории заранее
RUN mkdir -p /app/models \
    && mkdir -p /app/configs \
    && mkdir -p /app/src

# 6. Копируем весь проект
COPY . .

# 7. Экспонируем порт
EXPOSE 8000

# 8. Команда запуска API
CMD ["uvicorn", "src.inference:app", "--host", "0.0.0.0", "--port", "8000"]


# 1. Базовый образ Python
FROM python:3.10-slim

# 2. Рабочая директория внутри контейнера
WORKDIR /app

# 3. Копируем зависимости
COPY requirements.txt .

# 4. Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# 5. Копируем весь проект внутрь контейнера
COPY . .

# 6. Открываем порт
EXPOSE 8000

# 7. Команда запуска Uvicorn
CMD ["uvicorn", "src.inference:app", "--host", "0.0.0.0", "--port", "8000"]

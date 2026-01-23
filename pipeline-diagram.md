# Pipeline Diagram

## Общая схема пайплайна MLOps

```mermaid
flowchart TD

A[Raw CSV: netflix_reviews.csv] --> B[preprocessing.py]

B --> C[Binary Clean V1]
B --> D[Binary Clean V2]

C --> E[Exp1: Logistic Regression (unigrams)]
C --> F[Exp2: Logistic Regression (bigrams)]

D --> G[Exp3: Multinomial Logistic Regression (3-class)]

E --> H[Binary PROD Model]
F --> H
G --> I[3-Class PROD Model]

H --> J[FastAPI /predict (binary)]
I --> J[FastAPI /predict (3-class)]
```

---

Диаграмма отражает все этапы:

1. Сырые данные → препроцессинг  
2. Создание *двух версий датасета*  
3. Обучение *трёх моделей*  
4. Выбор лучших моделей  
5. Упаковка в FastAPI  
6. Деплой через Docker


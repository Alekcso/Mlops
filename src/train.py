# src/train.py
import yaml
import os
import pandas as pd
import joblib
import mlflow
import argparse

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, f1_score, classification_report


def train_model(
    data_path: str,
    target_col: str,
    model_out: str,
    vectorizer_out: str,
    log_path: str,
    max_features: int = 5000,
    ngram_range=(1, 2),
    random_state: int = 42,
    multi_class: bool = False
):
    """Тренировка Pipeline(TFIDF → LogisticRegression) + pkl + ONNX + MLflow."""

    # === 1. Загружаем датасет ===
    df = pd.read_csv(data_path)

    # очистка
    df = df.dropna(subset=["clean_text"])
    df = df[df["clean_text"].str.strip() != ""]

    X = df["clean_text"].astype(str)
    y = df[target_col]

    # === 2. Сплит ===
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=random_state, stratify=y
    )

    # === 3. Конструируем Pipeline ===
    if multi_class:
        logreg = LogisticRegression(
            max_iter=1000, multi_class="multinomial", random_state=random_state
        )
    else:
        logreg = LogisticRegression(max_iter=1000, random_state=random_state)

    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(max_features=max_features, ngram_range=ngram_range)),
        ("logreg", logreg)
    ])

    # === 4. Обучение ===
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)

    # === 5. Метрики ===
    acc = accuracy_score(y_test, y_pred)
    macro_f1 = f1_score(y_test, y_pred, average="macro")

    # === 6. Report ===
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    with open(log_path, "w", encoding="utf-8") as f:
        f.write("=== Classification report ===\n")
        f.write(classification_report(y_test, y_pred))
        f.write(f"\nAccuracy: {acc:.4f}\nMacro-F1: {macro_f1:.4f}\n")

    # === 7. Сохранение pkl ===
    os.makedirs(os.path.dirname(model_out), exist_ok=True)

    # pkl модели = весь pipeline
    joblib.dump(pipeline, model_out)

    # pkl векторайзера отдельно (для удобства FastAPI)
    vectorizer = pipeline.named_steps["tfidf"]
    joblib.dump(vectorizer, vectorizer_out)

    # === 8. Экспорт в ONNX ===
    try:
        from skl2onnx import convert_sklearn
        from skl2onnx.common.data_types import StringTensorType

        onnx_path = model_out.replace(".pkl", ".onnx")

        # вход — строка (текст)
        initial_type = [('input', StringTensorType([None, 1]))]

        onnx_model = convert_sklearn(
            pipeline,
            initial_types=initial_type
        )

        with open(onnx_path, "wb") as f:
            f.write(onnx_model.SerializeToString())

        print(f"[OK] Saved ONNX model → {onnx_path}")

    except Exception as e:
        print("[WARN] ONNX export failed:", e)

    # === 9. MLflow-трекинг ===
    with mlflow.start_run():
        mlflow.log_param("dataset_version", data_path)
        mlflow.log_param("max_features", max_features)
        mlflow.log_param("ngram_range", ngram_range)
        mlflow.log_param("multi_class", multi_class)

        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("macro_f1", macro_f1)

        mlflow.sklearn.log_model(pipeline, artifact_path="model")

    print(f"[OK] {target_col} | acc={acc:.4f} | f1={macro_f1:.4f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default="configs/train.yaml")
    args = parser.parse_args()

    cfg = yaml.safe_load(open(args.config, "r"))
    params = cfg["train"]

    train_model(
        data_path=params["data_path"],
        target_col=params["target_col"],
        model_out=params["model_out"],
        vectorizer_out=params["vectorizer_out"],
        log_path=params["log_path"],
        max_features=params["max_features"],
        ngram_range=tuple(params["ngram_range"]),
        random_state=params["random_state"],
        multi_class=params["multi_class"],
    )


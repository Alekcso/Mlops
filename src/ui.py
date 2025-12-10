import gradio as gr
import requests
import json

API = "http://localhost:8000/predict"

def predict(text, mode):
    payload = {"text": text, "mode": mode}
    r = requests.post(API, json=payload)
    return r.json()["sentiment"]

gr.Interface(
    fn=predict,
    inputs=[gr.Textbox(label="Text"), gr.Radio(["binary", "3class"], value="binary")],
    outputs="text",
    title="Netflix Sentiment Classifier",
).launch()

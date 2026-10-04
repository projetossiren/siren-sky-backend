import os
import time
import mlflow
import pandas as pd
from PIL import Image

from ultralytics import YOLO
from huggingface_hub import hf_hub_download

def load_model(repo_id: str, model_filename: str) -> YOLO:
    """
    Load a YOLO model from the Hugging Face Hub.

    Args:
        repo_id (str): The repository ID on Hugging Face Hub.
        model_filename (str): The filename of the model to load.

    Returns:
        YOLO: The loaded YOLO model.
    """

    model_path = hf_hub_download(repo_id=repo_id, filename=model_filename)
    model = YOLO(model_path)
    return model

def predict(model: YOLO, image: Image.Image) -> pd.DataFrame:
    start = time.perf_counter()
    results = model.predict(image, verbose=False)
    end = time.perf_counter()
    inference_time = end - start

    detections = []

    for result in results:
        for box in result.boxes:
            detections.append({
                "classe": result.names[int(box.cls[0])],
                "confianca": float(box.conf[0]),
                "tempo_inferencia": inference_time,
                "x1": float(box.xyxy[0][0]),
                "y1": float(box.xyxy[0][1]),
                "x2": float(box.xyxy[0][2]),
                "y2": float(box.xyxy[0][3])
            })

    return pd.DataFrame(
        detections,
        columns=["classe", "confianca", "tempo_inferencia", "x1", "y1", "x2", "y2"]
    )
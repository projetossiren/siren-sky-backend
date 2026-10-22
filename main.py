from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from io import BytesIO
from ai_model import predict, load_model
from PIL import Image
from image_process import transform_image

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

REPO_ID = "FathomNet/trash-detector"
FILENAME = "trash_mbari_09072023_640imgsz_50epochs_yolov8.pt"

@app.post("/image")
async def receber_imagem(image: UploadFile = File(...)):
    conteudo = await image.read()
    model = load_model(REPO_ID, FILENAME)
    converted_image = transform_image(conteudo)
    results = predict(model, converted_image)

    return {
        "results": results.to_dict(orient="records")
    }

@app.post("/teste")
async def teste():
    return {
        "message": "API funcionando corretamente!"
    }
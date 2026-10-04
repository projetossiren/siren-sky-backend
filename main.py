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
    print(f"Modelo carregado: {model.model_name} com {len(model.names)} classes.")
    converted_image = transform_image(conteudo)
    print(f"Imagem recebida: {image.filename}, tamanho: {converted_image.size}, modo: {converted_image.mode}")
    results = predict(model, converted_image)

    return {
        "results": results.to_dict(orient="records")
    }
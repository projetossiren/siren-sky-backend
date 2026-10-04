from PIL import Image
from io import BytesIO

def transform_image(image: bytes):
    """Transforma a imagem recebida em bytes para um objeto PIL Image no modo RGB."""
    return Image.open(BytesIO(image)).convert("RGB")

def resize_image(image: Image.Image, x: int, y: int) -> Image.Image:
    """
    Redimensiona a imagem para as dimensões especificadas (x, y).
    """
    return image.resize((x, y))

def reduce_quality(image: Image.Image, quality: int) -> Image.Image:
    """
    Reduz a qualidade da imagem para o valor especificado (quality).
    """
    buffer = BytesIO()

    image.save(buffer, format="JPEG", quality=quality)

    buffer.seek(0)

    with Image.open(buffer) as imagem:
        imagem.load()
        return imagem.copy()
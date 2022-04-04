from email.policy import HTTP
import os
from io import BytesIO

import requests
from PIL import Image, UnidentifiedImageError
from fastapi.exceptions import HTTPException


STATIC_DIR = os.environ.get("STATIC_DIR", "/tmp/static")
SIZE = 128, 128

def create(url, filename):
    try:
        content = requests.get(url).content
        with Image.open(BytesIO(content)) as img:
            img.thumbnail(SIZE)
            img.save(f"{STATIC_DIR}/{filename}", "JPEG")
    except requests.models.MissingSchema as ms:
        raise HTTPException(status_code=400, detail="Invalid input")
    except UnidentifiedImageError as uie:
        raise HTTPException(status_code=400, detail="Invalid output")
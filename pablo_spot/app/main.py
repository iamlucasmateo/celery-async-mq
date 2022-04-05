import os
import logging

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from wonderwords import RandomWord
from fastapi.staticfiles import StaticFiles

# from app.thumbnail_maker import create
from workers import thumbnail

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
STATIC_DIR = os.environ.get("STATIC_DIR", "/tmp/static")

class Thumbnail(BaseModel):
    url: str
    filename: Optional[str] = None 

app = FastAPI()
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.post("/thumbnail/", response_model=Thumbnail)
def create_thumbnail(tn: Thumbnail):
    try:
        rw = RandomWord()
        filename = '_'.join(rw.random_words(
            3, include_parts_of_speech=["nouns", "adjectives"]
        ))
        thumbnail.create.delay(tn.url, filename)
        tn.filename = filename
        return tn
    except Exception as e:
        logger.error(f"Error encountered: {e}")
        raise HTTPException(
            status_code=500, 
            detail="Internal Server Error"
        )

@app.get("/test")
def test():
    return { "working": "fine" }
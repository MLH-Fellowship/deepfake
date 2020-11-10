from typing import Optional
import shutil
from fastapi import FastAPI, File, UploadFile
import random
import os.path
from os import path
from fastapi.responses import FileResponse



app = FastAPI()

@app.post("/upload")
async def upload(image: UploadFile = File(...), video: UploadFile = File(...)):
    image_hash = "%016x" % random.getrandbits(128)
    video_hash = image_hash

    image_ext = image.filename.split('.')[-1].lower()
    if image_ext not in ['png', 'jpg', 'jpeg']:
        return {"error": "Only allowed [png, jpg, jpeg] for image"}


    video_ext = video.filename.split('.')[-1].lower()
    if video_ext not in ['mp4']:
        return {"error": "Only allowed [mp4] for video"}


    image_filename = f"{image_hash}.{image_ext}"
    with open(f"storage/uploads/images/{image_filename}", "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    video_filename = f"{video_hash}.{video_ext}"
    with open(f"storage/uploads/videos/{video_filename}", "wb") as buffer:
        shutil.copyfileobj(video.file, buffer)

    return {"status": "processing", "id": image_hash}

@app.get("/get")
async def get(id: str):
    
    filename = f'storage/results/{id}.mp4'
    if path.exists(filename):
        return FileResponse(filename)
    else:
        return {'status': 'not_ready'}

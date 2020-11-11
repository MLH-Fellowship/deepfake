from typing import Optional
from fastapi import FastAPI, File, UploadFile, Form
from os import path
from fastapi.responses import FileResponse, HTMLResponse
from starlette.responses import JSONResponse, PlainTextResponse, RedirectResponse
from engine import start_processing_thread
import shutil
import random
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/upload")
async def upload(image: UploadFile = File(...), video: UploadFile = File(...), redirect: str = Form(...), response_class=HTMLResponse):
    print(redirect)
    image_hash = "%016x" % random.getrandbits(128)
    video_hash = image_hash

    image_ext = image.filename.split('.')[-1].lower()
    if image_ext not in ['png', 'jpg', 'jpeg']:
        return {"error": "Only allowed [png, jpg, jpeg] for image"}

    video_ext = video.filename.split('.')[-1].lower()
    if video_ext not in ['mp4', 'gif']:
        return {"error": "Only allowed [mp4, gif] for video"}

    image_filename = f"{image_hash}.{image_ext}"

    with open(f"storage/uploads/images/{image_filename}", "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    video_filename = f"{video_hash}.{video_ext}"

    with open(f"storage/uploads/videos/{video_filename}", "wb") as buffer:
        shutil.copyfileobj(video.file, buffer)

    result_filename = f"{image_hash}.mp4"

    start_processing_thread(
        progress_filename=f'storage/progress/{image_hash}',
        image_filename=f'storage/uploads/images/{image_filename}',
        video_filename=f'storage/uploads/videos/{video_filename}',
        result_filename=f'storage/uploads/results/{result_filename}'
    )

    return HTMLResponse(content=f'<script>location.href="{redirect}{image_hash}";</script>', status_code=200)


@app.get("/get")
async def get(id: str):

    filename = f'storage/uploads/results/{id}.mp4'

    if path.exists(filename):
        return JSONResponse({"status": "ready", "filename": id})
    else:
        progressFilename = f'storage/progress/{id}'
        if not path.exists(progressFilename):
            return JSONResponse({"status": "not_ready", "progress": "0/0"})

        progressFile = open(progressFilename, 'r')

        progress = progressFile.read()
        progressFile.close()
        return JSONResponse({"status": "not_ready", "progress": progress})


@app.get("/getvideo")
async def get(id: str):
    filename = f'storage/uploads/results/{id}.mp4'
    if path.exists(filename):
        return FileResponse(path=filename)
    else:
        return "Oops"

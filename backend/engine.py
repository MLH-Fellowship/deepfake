from typing import Optional
from threading import Thread
from ml.demo import generate
from pathlib import Path


def start_processing_thread(progress_filename: str, image_filename: str, video_filename: str, result_filename: str):
    ml_thread = Thread(target=process, args=[
                       progress_filename, image_filename, video_filename, result_filename])
    ml_thread.start()


def process(progress_filename: str, image_filename: str, video_filename: str, result_filename: str):
    checkpoint = 'ml/models/vox-cpk.pth.tar'
    config = 'ml/config/vox-256.yaml'

    generate(progress_file=progress_filename, source_image=image_filename, driving_video=video_filename,
             result_video=result_filename, checkpoint=checkpoint, config=config)

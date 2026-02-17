from fastapi import FastAPI, UploadFile, File
import shutil
import os
from app.ml.video_processor import analyze_video
from app.ml.audio_processor import analyze_audio

from datetime import datetime

app = FastAPI(
    title="AI Interview Intelligence Platform",
    version="1.0.0"
)

UPLOAD_FOLDER = "uploads"

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.get("/")
def root():
    return {"message": "AI Interview Intelligence Backend Running 🚀"}


@app.post("/upload-interview")
async def upload_interview(video: UploadFile = File(...)):
    # Create unique filename
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    file_path = os.path.join(
        UPLOAD_FOLDER, f"{timestamp}_{video.filename}"
    )

    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(video.file, buffer)

    analysis_result = analyze_video(file_path)
    audio_result = analyze_audio(file_path)
    return {
    "filename": video.filename,
    "saved_path": file_path,
    "vision_analysis": analysis_result,
    "audio_analysis": audio_result
    }

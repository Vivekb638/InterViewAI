from fastapi import FastAPI, UploadFile, File
import shutil
import os
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

    return {
        "filename": video.filename,
        "saved_path": file_path,
        "status": "uploaded successfully"
    }

from fastapi import FastAPI, UploadFile, File
import shutil
import os
from app.processor import process_video
from fastapi.middleware.cors import CORSMiddleware

from app.database.database import SessionLocal, TrackingRecord


app = FastAPI(
    title="AI CCTV Surveillance Platform"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "message": "AI CCTV Surveillance API is running"
    }


@app.get("/tracking")
def get_tracking_history():

    db = SessionLocal()

    records = db.query(TrackingRecord).all()

    data = []

    for record in records:

        data.append({
            "id": record.id,
            "track_id": record.track_id,
            "object_type": record.object_type,
            "camera_id": record.camera_id,
            "timestamp": record.timestamp,
            "latitude": record.latitude,
            "longitude": record.longitude
        })

    db.close()

    return data

@app.get("/tracking/{track_id}")
def get_tracking_by_id(track_id: int):

    db = SessionLocal()

    records = db.query(TrackingRecord).filter(
        TrackingRecord.track_id == track_id
    ).all()

    data = []

    for record in records:

        data.append({
            "id": record.id,
            "track_id": record.track_id,
            "object_type": record.object_type,
            "camera_id": record.camera_id,
            "timestamp": record.timestamp,
            "latitude": record.latitude,
            "longitude": record.longitude
        })

    db.close()

    return data

@app.post("/upload")
def upload_video(file: UploadFile = File(...)):

    os.makedirs("videos", exist_ok=True)

    file_path = f"videos/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    process_video(file_path)

    return {
        "message": "Video uploaded successfully",
        "filename": file.filename
    }
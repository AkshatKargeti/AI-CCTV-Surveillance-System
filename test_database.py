from app.database.database import SessionLocal, TrackingRecord

db = SessionLocal()

records = db.query(TrackingRecord).all()

for record in records:
    print(
        record.track_id,
        record.object_type,
        record.camera_id,
        record.timestamp,
        record.latitude,
        record.longitude
    )

db.close()
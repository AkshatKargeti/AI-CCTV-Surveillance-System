import cv2

from app.tracking.tracker import ObjectTracker
from app.database.database import SessionLocal, TrackingRecord


def process_video(video_path):

    tracker = ObjectTracker()
    video = cv2.VideoCapture(video_path)
    db = SessionLocal()

    while True:

        success, frame = video.read()

        if not success:
            break

        results = tracker.track(frame)
        result = results[0]

        if result.boxes.id is not None:

            track_ids = result.boxes.id.int().cpu().tolist()
            class_ids = result.boxes.cls.int().cpu().tolist()

            for track_id, class_id in zip(track_ids, class_ids):

                object_type = result.names[class_id]

                record = TrackingRecord(
                    track_id=track_id,
                    object_type=object_type,
                    camera_id="camera_1",
                    latitude=28.6139,
                    longitude=77.2090
                )

                db.add(record)

            db.commit()

    video.release()
    db.close()

    print("Video processing completed")
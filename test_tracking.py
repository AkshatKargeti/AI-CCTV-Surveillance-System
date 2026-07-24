import cv2

from app.tracking.tracker import ObjectTracker
from app.database.database import SessionLocal, TrackingRecord


tracker = ObjectTracker()

video = cv2.VideoCapture("videos/test.mp4")

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

    annotated_frame = result.plot()

    annotated_frame = cv2.resize(
        annotated_frame,
        (960, 540)
    )

    cv2.imshow("AI CCTV Tracking", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


video.release()

db.close()

cv2.destroyAllWindows()
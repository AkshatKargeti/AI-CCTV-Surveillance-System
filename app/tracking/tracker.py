from ultralytics import YOLO


class ObjectTracker:

    def __init__(self):
        self.model = YOLO("yolo11n.pt")

    def track(self, frame):
        results = self.model.track(
            frame,
            persist=True,
            tracker="bytetrack.yaml"
        )

        return results
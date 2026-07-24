import cv2

from app.detection.detector import ObjectDetector


detector = ObjectDetector()

video = cv2.VideoCapture("videos/test.mp4")
if not video.isOpened():
    print("ERROR: Video not found or could not be opened")
else:
    print("Video opened successfully")


while True:

    success, frame = video.read()

    if not success:
        break

    results = detector.detect(frame)

    annotated_frame = results[0].plot()
    annotated_frame = cv2.resize(
    annotated_frame,
    (960, 540)
    )

    cv2.imshow("AI CCTV Detection", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


video.release()

cv2.destroyAllWindows()
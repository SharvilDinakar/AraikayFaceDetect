import cv2
import datetime
import logging

class FaceDetection:
    def __init__(self, cascade_path, scaleFactor, minNeighbors, minSize_width, minSize_height):
        self.cascade_classifier = cv2.CascadeClassifier(cascade_path)
        self.scaleFactor = scaleFactor
        self.minNeighbors = minNeighbors
        self.minSize = (minSize_width, minSize_height)
        self.first_frame = None
        self.face_detected = False
        self.last_face_time = None

    def process_frame(self, frame, capture_callback):
        """Process the frame for face detection and capture images."""
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)

            if self.first_frame is None:
                self.first_frame = gray
                return

            frame_delta = cv2.absdiff(self.first_frame, gray)
            thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
            thresh = cv2.dilate(thresh, None, iterations=2)

            faces = self.cascade_classifier.detectMultiScale(
                gray,
                scaleFactor=self.scaleFactor,
                minNeighbors=self.minNeighbors,
                minSize=self.minSize
            )

            for (x, y, w, h) in faces:
                if not self.face_detected:
                    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                    capture_callback(frame, timestamp)
                    self.last_face_time = datetime.datetime.now()
                    self.face_detected = True

            if self.face_detected:
                if (datetime.datetime.now() - self.last_face_time).total_seconds() > 5:
                    self.face_detected = False

        except Exception as e:
            logging.error(f"Error during face detection: {e}")

    def reset(self):
        """Reset the first frame and face detection state."""
        self.first_frame = None
        self.face_detected = False
        self.last_face_time = None

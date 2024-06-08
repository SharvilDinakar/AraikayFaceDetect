from picamera2 import Picamera2, Preview
import cv2
import numpy as np
import datetime

# Initialize Picamera2
picam2 = Picamera2()
config = picam2.create_still_configuration(main={"size": (640, 480)})
picam2.configure(config)
picam2.start()

# Load the pre-trained Haar Cascade classifier for face detection
cascade_classifier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

def capture_image(frame, timestamp):
    parentID=1
    folder_path = "Image_Bucket"
    filename = f"{folder_path}/{parentID}-face_detect{timestamp}.jpg"
    cv2.imwrite(filename, frame)
    print(f"Face captured: {filename}")

# Capture the first frame for background
first_frame = None
face_detected = False
last_face_time = None

while True:
    # Capture a frame
    frame = picam2.capture_array()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if first_frame is None:
        first_frame = gray
        continue

    # Compute the absolute difference between the current frame and the first frame
    frame_delta = cv2.absdiff(first_frame, gray)
    thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)

    # Find faces in the grayscale frame
    faces = cascade_classifier.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Loop through detected faces
    for (x, y, w, h) in faces:
        # Draw a rectangle around the face
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        # Capture image if face is detected and no face was previously detected
        if not face_detected:
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            capture_image(frame[y:y+h, x:x+w], timestamp)  # Capture only the face region
            last_face_time = datetime.datetime.now()
            face_detected = True

    # Check if face was detected in the previous frame
    if face_detected:
        # If no faces are detected for 5 seconds, reset face_detected flag
        if (datetime.datetime.now() - last_face_time).total_seconds() > 5:
            face_detected = False

    # Display the frame
    cv2.imshow("Face Detector", frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
picam2.stop()
cv2.destroyAllWindows()


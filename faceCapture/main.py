import cv2
import logging
from camera import Camera
from face_detection import FaceDetection
from utils import load_configuration, setup_logging, capture_image

def main():
    config = load_configuration()

    # Setup logging
    setup_logging(config.get('Logging', 'log_filename'),
                  getattr(logging, config.get('Logging', 'log_level').upper()))

    # Initialize camera
    camera = Camera(
        config.getint('Camera', 'resolution_width'),
        config.getint('Camera', 'resolution_height')
    )
    camera.initialize()

    # Initialize face detection
    face_detection = FaceDetection(
        config.get('FaceDetection', 'cascade_path'),
        config.getfloat('FaceDetection', 'scaleFactor'),
        config.getint('FaceDetection', 'minNeighbors'),
        config.getint('FaceDetection', 'minSize_width'),
        config.getint('FaceDetection', 'minSize_height')
    )

    try:
        while True:
            frame = camera.capture_frame()
            color_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            face_detection.process_frame(
                color_frame,
                lambda frame, timestamp: capture_image(frame, timestamp, config.get('ImageCapture', 'folder_path'),
                                                       config.getint('ImageCapture', 'parentID'))
            )

            cv2.imshow("Face Detector", color_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                logging.info("Exiting face detection loop")
                break
    finally:
        camera.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

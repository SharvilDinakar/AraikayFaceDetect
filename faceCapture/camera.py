from picamera2 import Picamera2
import logging

class Camera:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.picam2 = None

    def initialize(self):
        """Initialize the Picamera2 with the specified resolution."""
        try:
            self.picam2 = Picamera2()
            camera_config = self.picam2.create_still_configuration(main={"size": (self.width, self.height)})
            self.picam2.configure(camera_config)
            self.picam2.start()
            logging.info("Camera initialized successfully")
        except Exception as e:
            logging.error(f"Failed to initialize camera: {e}")
            raise

    def capture_frame(self):
        """Capture a frame using the camera."""
        if self.picam2:
            return self.picam2.capture_array()
        else:
            raise RuntimeError("Camera is not initialized")

    def stop(self):
        """Stop the camera."""
        if self.picam2:
            self.picam2.stop()
            logging.info("Camera stopped successfully")
        else:
            logging.warning("Camera stop called, but camera was not initialized")

import configparser
import logging
import cv2

def load_configuration(config_file='config.ini'):
    """Load and return the configuration details from the ini file."""
    config = configparser.ConfigParser()
    try:
        config.read(config_file)
    except Exception as e:
        logging.error(f"Failed to read config file: {e}")
        raise
    return config

def setup_logging(log_filename, log_level):
    """Set up logging configuration."""
    logging.basicConfig(filename=log_filename,
                        level=log_level,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("Logging initialized")

def capture_image(frame, timestamp, folder_path, parentID):
    """Capture and save the image frame with the given timestamp."""
    try:
        filename = f"{folder_path}/{parentID}-face_detect{timestamp}.jpg"
        cv2.imwrite(filename, frame)
        logging.info(f"Image captured: {filename}")
    except Exception as e:
        logging.error(f"Failed to capture image: {e}")

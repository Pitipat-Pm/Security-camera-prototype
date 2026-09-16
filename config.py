import os
import cv2

# Base Directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Camera Configuration
CAM_RESOLUTION = (320, 240)
FPS = 8

# Storage Directories
PHOTO_DIR = os.path.join(BASE_DIR, "photos")
VIDEO_DIR = os.path.join(BASE_DIR, "videos")
RECORD_DIR = os.path.join(BASE_DIR, "recordings")

# Ensure directories exist
os.makedirs(PHOTO_DIR, exist_ok=True)
os.makedirs(VIDEO_DIR, exist_ok=True)
os.makedirs(RECORD_DIR, exist_ok=True)

# Face Detection Model
CASCADE_PATH = os.path.join(BASE_DIR, "haarcascade_frontalface_default.xml")
# Fallback to OpenCV built-in cascade file if local file does not exist
if not os.path.exists(CASCADE_PATH):
    try:
        builtin_path = os.path.join(cv2.data.haarcascades, "haarcascade_frontalface_default.xml")
        if os.path.exists(builtin_path):
            CASCADE_PATH = builtin_path
    except Exception:
        pass

CSV_LOG_FILE = os.path.join(RECORD_DIR, "object_log.csv")

# Server Configuration
HOST = "0.0.0.0"
PORT = 5000
DEBUG = False

import cv2
import threading
import time
import os
import psutil
import csv
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
import config


class SecurityCamera:
    def __init__(self):
        self.frame_buffer = None
        self.latest_photo = None
        self.running = False
        self.camera_thread = None
        self.mode = None
        self.total_detect_count = 0
        self.recording = False
        self.h264_file = None
        self.encoder = None

        # Initialize CSV log file
        if not os.path.exists(config.CSV_LOG_FILE):
            with open(config.CSV_LOG_FILE, 'w', newline='', encoding='utf-8') as f:
                csv.writer(f).writerow(['timestamp', 'faces_detected', 'total_detect_count'])

        # Initialize Haar Cascade
        self.face_cascade = cv2.CascadeClassifier(config.CASCADE_PATH)

        # Initialize PiCamera2
        self.picam2 = Picamera2()
        cam_config = self.picam2.create_preview_configuration(main={"size": config.CAM_RESOLUTION})
        self.picam2.configure(cam_config)
        self.picam2.start()
        time.sleep(1)

    def camera_loop(self):
        last_detect_time = time.time()
        while self.running:
            frame_start_time = time.time()
            frame = self.picam2.capture_array()

            # CPU / Temp
            cpu = psutil.cpu_percent()
            try:
                with open("/sys/class/thermal/thermal_zone0/temp") as f:
                    temp = float(f.read()) / 1000.0
            except Exception:
                temp = 0.0

            faces_detected = 0

            # 1. PHOTO MODE
            if self.mode == "photo":
                timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
                filename = os.path.join(config.PHOTO_DIR, f"{timestamp}.jpg")
                cv2.imwrite(filename, frame)
                # Store path relative or absolute
                self.latest_photo = filename
                self.mode = None

            # 2. DETECTION MODE
            elif self.mode == "detection":
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)
                faces_detected = len(faces)
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y, w, h), (0, 255, 0), 2)

                now = time.time()
                if now - last_detect_time >= 1.0:  # Log every 1 second
                    self.total_detect_count += faces_detected
                    with open(config.CSV_LOG_FILE, 'a', newline='', encoding='utf-8') as f:
                        csv.writer(f).writerow([
                            time.strftime('%Y-%m-%d %H:%M:%S'),
                            faces_detected,
                            self.total_detect_count
                        ])
                    last_detect_time = now

                print(f"Mode: {self.mode} | Faces: {faces_detected} | Total: {self.total_detect_count} | CPU: {cpu}% | Temp: {temp:.1f}°C | FPS: {config.FPS}")

            # 3. VIDEO MODE
            elif self.mode == "video":
                print(f"Mode: {self.mode} | CPU: {cpu}% | Temp: {temp:.1f}°C | FPS: {config.FPS}")

            # Encode frame for MJPEG stream
            ret, buffer = cv2.imencode('.jpg', frame)
            if ret:
                self.frame_buffer = buffer.tobytes()

            frame_time = time.time() - frame_start_time
            time.sleep(max(0, (1.0 / config.FPS) - frame_time))

    def video_loop(self):
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        self.h264_file = os.path.join(config.VIDEO_DIR, f"{timestamp}.h264")
        self.encoder = H264Encoder(bitrate=1000000)
        self.picam2.start_recording(self.encoder, self.h264_file)
        print(f"Recording started: {self.h264_file}")
        while self.recording:
            time.sleep(0.1)

    def start_mode(self, selected_mode):
        self.mode = selected_mode
        if not self.running:
            self.running = True
            self.camera_thread = threading.Thread(target=self.camera_loop, daemon=True)
            self.camera_thread.start()

        if self.mode == "video" and not self.recording:
            self.recording = True
            t_video = threading.Thread(target=self.video_loop, daemon=True)
            t_video.start()

    def stop_save(self):
        response_msg = ""
        if self.mode == "video" and self.h264_file and os.path.exists(self.h264_file):
            self.recording = False
            self.picam2.stop_recording()
            mp4_file = self.h264_file.replace(".h264", ".mp4")
            os.system(f"MP4Box -add {self.h264_file} {mp4_file}")
            if os.path.exists(self.h264_file):
                os.remove(self.h264_file)
            response_msg = f"Video saved: {os.path.basename(mp4_file)}"
            self.h264_file = None
        elif self.mode == "detection":
            response_msg = f"Detection stopped. CSV saved: {os.path.basename(config.CSV_LOG_FILE)}"
        else:
            response_msg = f"{self.mode or 'All'} mode stopped."

        self.mode = None
        return response_msg

    def reset(self):
        self.mode = None
        self.recording = False
        self.running = False
        time.sleep(0.1)
        self.running = True
        self.camera_thread = threading.Thread(target=self.camera_loop, daemon=True)
        self.camera_thread.start()
        return "System reset. Ready for next function."

    def generate_mjpeg(self):
        while True:
            if self.frame_buffer:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + self.frame_buffer + b'\r\n')
            else:
                time.sleep(0.05)

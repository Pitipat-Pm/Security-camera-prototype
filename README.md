# 🎥 Raspberry Pi Security Camera Web Application

ระบบกล้องวงจรปิดอัจฉริยะ (Security Camera) ทำงานบน Raspberry Pi ด้วย **Flask**, **Picamera2**, และ **OpenCV (Haar Cascade)**

---

## 📁 โครงสร้างโปรเจกต์ (Project Structure)

```text
Security camera/
├── app.py                     # Entry point หลักของ Flask Application (Routes & APIs)
├── camera.py                  # Module ควบคุมกล้อง Picamera2, Face Detection & Video Recording
├── config.py                  # ค่าตั้งค่าระบบ (Resolution, FPS, Storage Paths, Port)
├── requirements.txt           # รายการ Python packages
├── .gitignore                 # กำหนดไฟล์ที่ไม่ต้อง push ขึ้น Git
│
├── templates/
│   └── index.html             # UI หน้าเว็บควบคุมกล้อง
│
├── static/
│   ├── css/
│   │   └── style.css          # สไตล์หน้าเว็บ (Dark UI)
│   └── js/
│       └── main.js            # JavaScript ควบคุมปุ่มและดึงข้อมูลแบบ Real-time
│
├── photos/                    # โฟลเดอร์เก็บภาพนิ่งที่ถ่าย (.jpg)
├── videos/                    # โฟลเดอร์เก็บวิดีโอที่บันทึก (.mp4)
├── recordings/                # โฟลเดอร์เก็บบันทึก Log ตรวจจับใบหน้า (object_log.csv)
│
└── security-camera-prototpy/  # ไฟล์ Prototype ดั้งเดิม (Backup)
```

---

## ⚙️ ข้อกำหนดเบื้องต้น (Prerequisites)
- บอร์ด **Raspberry Pi 3 / 4 / 5 / Zero 2 W** (รัน Raspberry Pi OS)
- โมดูลกล้อง **Raspberry Pi Camera Module** (V1, V2, V3 หรือ HQ Camera)
- เชื่อมต่อเครือข่าย Wi-Fi/LAN วงเดียวกับคอมพิวเตอร์หรือมือถือที่จะเปิดดู

---

## 🚀 การติดตั้งและใช้งานบน Raspberry Pi (Step-by-Step Setup)

### 1. ติดตั้ง System Packages ที่จำเป็น
```bash
sudo apt update
sudo apt install -y python3-picamera2 python3-opencv python3-flask python3-psutil gpac wget
```
> [!NOTE]
> - `gpac` ใช้สำหรับคำสั่ง `MP4Box` ในการรวม/แปลงไฟล์ `.h264` เป็น `.mp4`
> - บน Raspberry Pi OS (Debian Bookworm) แนะนำให้ติดตั้ง Python library ผ่าน `apt` ตามคำสั่งด้านบนเพื่อเลี่ยงข้อผิดพลาด *PEP 668 externally-managed-environment*

*(ทางเลือก) หากต้องการใช้ Virtual Environment:*
```bash
python3 -m venv --system-site-packages venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. ดาวน์โหลด Haar Cascade Model สำหรับตรวจจับใบหน้า
ดาวน์โหลดไฟล์โมเดล Haar Cascade เข้ามาไว้ในโฟลเดอร์โปรเจกต์:
```bash
wget https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml
```

### 3. รันโปรแกรม
```bash
python3 app.py
```

### 4. การเข้าใช้งานผ่านเบราว์เซอร์
1. ตรวจสอบหมายเลข IP ของ Raspberry Pi:
   ```bash
   hostname -I
   ```
2. เปิดเบราว์เซอร์บนมือถือหรือคอมพิวเตอร์ที่อยู่วง Wi-Fi เดียวกัน แล้วไปที่:
   ```text
   http://<IP_ของ_Raspberry_Pi>:5000
   ```
   *(ตัวอย่าง: `http://192.168.1.150:5000`)*

---

## 🛠️ การตั้งค่าระบบ (Configuration)
สามารถปรับแต่งค่าต่าง ๆ ได้ในไฟล์ [`config.py`](config.py):
- `CAM_RESOLUTION = (320, 240)` : ปรับความละเอียดกล้อง (เช่น `(640, 480)`, `(1280, 720)`)
- `FPS = 8` : ปรับอัตราเฟรมเรตตามความสามารถของบอร์ด (แนะนำ 8-15 FPS สำหรับ Pi Zero/Pi 3)
- `PORT = 5000` : เปลี่ยนพอร์ตการทำงานของ Web Server

---

## ✨ ฟังก์ชันการทำงาน (Features)
| ฟังก์ชัน | คำอธิบาย |
|---|---|
| 📹 **Live Stream** | สตรีมวิดีโอสดแบบ MJPEG Stream ผ่านเบราว์เซอร์ Real-time |
| 📸 **Take Photo** | ถ่ายภาพนิ่งความละเอียดตามตั้งค่า และบันทึกลง `photos/` |
| 🎬 **Start Video** | บันทึกวิดีโอ H.264 และแปลงเป็น MP4 อัตโนมัติลง `videos/` เมื่อกด Stop |
| 🎯 **Start Detection** | ตรวจจับใบหน้าแบบเรียลไทม์ พร้อมบันทึก Timestamp และจำนวนที่พบลำดับลง `recordings/object_log.csv` |
| 📁 **Media Management** | ดูรูปภาพ, เล่นวิดีโอ, ดาวน์โหลด Log CSV และสั่งลบไฟล์ผ่านหน้าเว็บได้ทันที |
| 🔄 **System Reset** | รีเซ็ตระบบกล้องกลับสู่โหมด Standby เพื่อพร้อมรับคำสั่งใหม่ |

---

## 🔄 (ทางเลือก) ตั้งค่าให้โปรแกรมเริ่มทำงานอัตโนมัติเมื่อเปิดเครื่อง (Autostart with systemd)

สร้าง service file:
```bash
sudo nano /etc/systemd/system/security-camera.service
```

วางข้อความนี้ลงไป (แก้ไข `WorkingDirectory` และ `User` ให้ตรงกับของคุณ):
```ini
[Unit]
Description=Raspberry Pi Security Camera Web Service
After=network.target

[Service]
User=pi
WorkingDirectory=/home/pi/Security-camera
ExecStart=/usr/bin/python3 app.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

เปิดใช้งาน service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable security-camera.service
sudo systemctl start security-camera.service
```

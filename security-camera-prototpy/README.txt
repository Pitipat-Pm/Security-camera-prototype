WiFi Security Camera With a Pi Zero 2W
ระบบกล้องวงจรปิดไร้สายต้นทุนต่ำ พร้อมระบบตรวจจับใบหน้าและควบคุมผ่าน Web Application

1. ภาพรวม (Project Overview)
โครงการนี้พัฒนาระบบกล้องวงจรปิดแบบไร้สายขนาดเล็ก ต้นทุนต่ำ โดยใช้บอร์ด Raspberry Pi Zero 2 W ร่วมกับ Raspberry Pi Camera Module ทำงานร่วมกับ Web Application ที่พัฒนาด้วย Flask Framework เพื่อให้ผู้ใช้สามารถดูภาพสด (Live Streaming) ถ่ายภาพนิ่ง บันทึกวิดีโอ และตรวจจับใบหน้าแบบเรียลไทม์ผ่านเว็บเบราว์เซอร์

2. คุณสมบัติหลัก (Key Features)
ระบบรองรับการทำงาน 3 โหมดหลัก ผ่าน Web Interface (http://<IP_RaspberryPi>:5000):
- Photo Mode: สั่งถ่ายภาพนิ่งและบันทึกไฟล์ภาพไว้ในโฟลเดอร์ photos/
- Video Mode: บันทึกวิดีโอไฟล์ .h264 แล้วแปลงเป็น .mp4 อัตโนมัติในโฟลเดอร์ videos/
- Detection Mode: ตรวจจับใบหน้าแบบเรียลไทม์ด้วย OpenCV (Haar Cascade) พร้อมบันทึกประวัติและ Timestamp ลงไฟล์ CSV (recordings/object_log.csv)
- Live Streaming: สตรีมวิดีโอสดแบบ MJPEG ผ่าน Web Browser

3. อุปกรณ์ฮาร์ดแวร์ (Hardware Components)
- บอร์ดหลัก: Raspberry Pi Zero 2 W (Quad-core Arm Cortex-A53 @ 1GHz, RAM 512MB, WiFi 2.4GHz)
- กล้อง: Raspberry Pi Camera Module / NoIR Camera Version 2 (ต่อผ่านพอร์ต CSI)
- หน่วยความจำ: MicroSD Card 32GB (Class 10 / A1)
- แหล่งจ่ายไฟ: 5V Micro USB (2.5A)
- อุปกรณ์ภายนอก: ปุ่มกดสั่งการ (Push Button) ต่อเข้าพอร์ต GPIO27 พร้อม Resistor 10kΩ และไฟ LED แสดงสถานะ ต่อเข้าพอร์ต GPIO10 ผ่าน Resistor 330Ω

4. ซอฟต์แวร์และไลบรารี (Software Stack)
- ระบบปฏิบัติการ: Raspberry Pi OS 32-bit (Legacy Lite)
- ภาษาที่ใช้: Python 3
- Web Framework: Flask Framework
- Computer Vision: OpenCV (haarcascade_frontalface_default.xml)
- ควบคุมกล้อง: Picamera2
- แปลงไฟล์วิดีโอ: MP4Box (แปลงไฟล์ .h264 เป็น .mp4)
- ตรวจสอบระบบ: psutil (สำหรับตรวจสอบ CPU Load และอุณหภูมิ)

5. สรุปผลการทดสอบระบบ (Experimental Results)
จากการทดลองระบบจำนวน 100 ครั้งในแต่ละโหมด:
- การถ่ายภาพ (100 ครั้ง): อัตราความสำเร็จ 100% เวลาเฉลี่ยที่ไฟล์ภาพปรากฏประมาณ 0.2 มิลลิวินาที
- การบันทึกวิดีโอ (100 ครั้ง): อัตราความสำเร็จ 100% ความเร็วเฟรมคงที่ที่ 8 FPS, ภาระงาน CPU อยู่ที่ ~30–50%, และอุณหภูมิ CPU อยู่ที่ประมาณ 50–60°C
- การตรวจจับใบหน้า (100 ครั้ง): สามารถตรวจจับและบันทึกประวัติลงไฟล์ CSV ได้ถูกต้อง ใช้พลังงานและทรัพยากรต่ำ

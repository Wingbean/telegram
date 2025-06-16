# ใช้ Python base image
FROM python:3.11-slim

# ตั้ง working directory ใน container
WORKDIR /app

# คัดลอกไฟล์ requirements.txt และติดตั้ง dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# คัดลอกโค้ดทั้งหมดมายัง container
COPY . .

# สั่งให้ container ใช้ UTF-8
ENV PYTHONUNBUFFERED=1
ENV LANG=C.UTF-8

# สั่งให้รัน main.py เมื่อ container เริ่มทำงาน
CMD ["python", "main.py"]
FROM python:3.11-slim

# ติดตั้ง system dependencies ที่จำเป็นสำหรับ lxml, playwright, etc.
RUN apt-get update && apt-get install -y \
    build-essential \
    libxml2-dev \
    libxslt-dev \
    libffi-dev \
    libssl-dev \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Optional: อัปเดต pip เป็นเวอร์ชันล่าสุด
RUN pip install --upgrade pip

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
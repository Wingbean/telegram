FROM python:3.11-slim

# 2. ติดตั้ง supercronic (ตัวจัดการ cron ที่เหมาะกับ Docker)
# ดาวน์โหลดเวอร์ชันสำหรับ ARM64
ENV SUPERCRONIC_URL=https://github.com/aptible/supercronic/releases/download/v0.2.29/supercronic-linux-arm64
ENV SUPERCRONIC_SHA1=623b1e102f7412354ea38d10037a8955b2597405

# ติดตั้ง packages ที่จำเป็น
RUN apt-get update && apt-get install -y \
        build-essential \
        pkg-config \
        wget \
    # ดาวน์โหลดและติดตั้ง supercronic
    && wget -q "${SUPERCRONIC_URL}" -O /usr/local/bin/supercronic \
    && echo "${SUPERCRONIC_SHA1}  /usr/local/bin/supercronic" | sha1sum -c - \
    && chmod +x /usr/local/bin/supercronic \
    # ทำความสะอาด: ลบ package ชั่วคราว (wget) และไฟล์ขยะทั้งหมด
    && apt-get purge -y wget \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# 3. ตั้งค่า Working Directory ภายใน Container
WORKDIR /app

# 4. คัดลอกไฟล์ requirements.txt และติดตั้ง Library
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. คัดลอกไฟล์ crontab ที่เราสร้างไว้
COPY crontab.txt /etc/crontab

# 6. คัดลอกโค้ดโปรเจคทั้งหมดเข้าไปใน container
COPY . .

# 7. คำสั่งที่จะรันเมื่อ container เริ่มทำงาน
# ให้ supercronic อ่านไฟล์ crontab แล้วเริ่มทำงาน
CMD ["supercronic", "/etc/crontab"]

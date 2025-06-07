# utils/logger.py

import logging
import os
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

def setup_logger(name: str = __name__, level: int = logging.INFO) -> logging.Logger:
    """
    สร้างและตั้งค่า logger สำหรับแอปพลิเคชัน

    Args:
        name (str): ชื่อ logger (ค่าเริ่มต้นคือ __name__)
        level (int): ระดับของ log เช่น logging.INFO, logging.DEBUG

    Returns:
        logging.Logger: อินสแตนซ์ของ logger ที่ตั้งค่าเสร็จแล้ว
    """
    
    # โฟลเดอร์สำหรับเก็บ log
    log_dir = os.path.join(os.getcwd(), "logs")
    os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # หลีกเลี่ยงการเพิ่ม handler ซ้ำ
    if logger.handlers:
        return logger

    # รูปแบบของ log message
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Console handler (แสดงบนหน้าจอ)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler (เก็บเป็นไฟล์)
    #log_filename = f"app_{datetime.now().strftime('%Y%m%d')}.log"
    #log_file_path = os.path.join(log_dir, log_filename)
    #file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
    #file_handler.setLevel(level)
    #file_handler.setFormatter(formatter)
    #logger.addHandler(file_handler)


    # Timed rotating file handler (หมุนทุกวัน, เก็บย้อนหลัง 7 วัน)
    log_file_path = os.path.join(log_dir, f"{name}.log")
    time_handler = TimedRotatingFileHandler(
        log_file_path,
        when='midnight',
        interval=1,
        backupCount=7,
        encoding='utf-8'
    )
    time_handler.setLevel(level)
    time_handler.setFormatter(formatter)
    logger.addHandler(time_handler)

    return logger

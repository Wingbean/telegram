"""
ฟังก์ชันช่วยเหลือทั่วไปที่ใช้ในหลายส่วนของแอปพลิเคชัน
"""

import os
import re
import json
import hashlib
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Union
from decimal import Decimal
import pandas as pd
import socket

# ตรวจสอบพอร์ตว่าง
def is_port_available(port: int, host: str = "0.0.0.0") -> bool:
    """ตรวจสอบว่าพอร์ตสามารถใช้งานได้หรือไม่"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) != 0

# ตรวจสอบว่าไฟล์ CSV มี header ที่ต้องการ
def validate_csv_headers(file_path: str, required_headers: List[str]) -> bool:
    """ตรวจสอบว่า CSV มี header ครบถ้วน"""
    try:
        df = pd.read_csv(file_path, nrows=1)
        return all(col in df.columns for col in required_headers)
    except Exception:
        return False


# ===== แปลงและจัดรูปแบบ =====
def safe_str_convert(value: Any) -> str:
    """แปลงค่าเป็น string อย่างปลอดภัย"""
    if value is None:
        return ""
    elif isinstance(value, Decimal):
        return str(value)
    elif isinstance(value, (int, float)):
        return str(value)
    elif isinstance(value, datetime):
        return value.strftime('%Y-%m-%d %H:%M:%S')
    else:
        return str(value)


def format_thai_date(date_value: Union[str, datetime]) -> str:
    """แปลงวันที่เป็นรูปแบบไทย เช่น 7 มิถุนายน 2567"""
    thai_months = [
        "", "มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน",
        "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"
    ]
    if isinstance(date_value, str):
        try:
            date_obj = datetime.strptime(date_value, '%Y-%m-%d')
        except ValueError:
            return date_value
    elif isinstance(date_value, datetime):
        date_obj = date_value
    else:
        return str(date_value)

    thai_year = date_obj.year + 543
    thai_month = thai_months[date_obj.month]
    return f"{date_obj.day} {thai_month} {thai_year}"


def format_file_size(size_bytes: int) -> str:
    """แปลงขนาดไฟล์เป็น human-readable format"""
    if size_bytes == 0:
        return "0B"
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    return f"{size_bytes:.1f}{size_names[i]}"


def format_currency(amount: Union[int, float, Decimal], currency: str = "฿") -> str:
    """จัดรูปแบบจำนวนเงิน"""
    if isinstance(amount, Decimal):
        amount = float(amount)
    return f"{currency}{amount:,.2f}"


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """ตัดข้อความให้สั้นลงตามความยาวที่กำหนด"""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


# ===== การตรวจสอบและความปลอดภัย =====
def validate_email(email: str) -> bool:
    """ตรวจสอบรูปแบบอีเมล"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_thai_id(thai_id: str) -> bool:
    """ตรวจสอบเลขบัตรประชาชนไทย"""
    if not thai_id or len(thai_id) != 13 or not thai_id.isdigit():
        return False
    check_sum = sum(int(thai_id[i]) * (13 - i) for i in range(12))
    check_digit = (11 - (check_sum % 11)) % 10
    return check_digit == int(thai_id[12])


def mask_sensitive_data(data: str, mask_char: str = "*", visible_chars: int = 4) -> str:
    """ซ่อนข้อมูลสำคัญ เช่น บัตร ปชช หรือเบอร์โทร"""
    if not data or len(data) <= visible_chars:
        return mask_char * len(data) if data else ""
    return data[:visible_chars] + mask_char * (len(data) - visible_chars)


def sanitize_filename(filename: str) -> str:
    """ทำความสะอาดชื่อไฟล์ให้ปลอดภัยและไม่ยาวเกิน"""
    cleaned = re.sub(r'[<>:"/\\|?*]', '', filename)
    if len(cleaned) > 255:
        name, ext = os.path.splitext(cleaned)
        cleaned = name[:250] + ext
    return cleaned


# ===== การประมวลผลข้อมูล =====
def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    """แบ่งลิสต์เป็นชิ้นเล็กๆ ขนาดตามต้องการ"""
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def retry_operation(func, max_retries: int = 3, delay: float = 1.0):
    """ทำซ้ำการทำงานหากเกิดข้อผิดพลาดแบบมี backoff"""
    import time
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            time.sleep(delay * (2 ** attempt))  # exponential backoff


def calculate_age(birth_date: Union[str, datetime]) -> int:
    """คำนวณอายุจากวันเกิด"""
    if isinstance(birth_date, str):
        try:
            birth_date = datetime.strptime(birth_date, '%Y-%m-%d')
        except ValueError:
            return 0
    today = datetime.now()
    age = today.year - birth_date.year
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1
    return age


def generate_hash(data: str, algorithm: str = 'sha256') -> str:
    """สร้าง hash เช่น SHA-256 จากข้อมูล string"""
    hash_func = getattr(hashlib, algorithm, hashlib.sha256)
    return hash_func(data.encode('utf-8')).hexdigest()


# ===== การจัดการไฟล์ JSON =====
def load_json_file(filepath: str, default: Any = None) -> Any:
    """โหลดไฟล์ JSON อย่างปลอดภัย"""
    try:
        if not os.path.exists(filepath):
            return default
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return default


def save_json_file(data: Any, filepath: str) -> bool:
    """บันทึกข้อมูลเป็นไฟล์ JSON"""
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except (IOError, TypeError):
        return False


# ===== การแปลงข้อมูลกับ Pandas =====
def dataframe_to_dict_list(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """แปลง DataFrame เป็น list of dictionaries"""
    return df.to_dict('records')


def dict_list_to_dataframe(data: List[Dict[str, Any]]) -> pd.DataFrame:
    """แปลง list of dictionaries เป็น DataFrame"""
    return pd.DataFrame(data)


# ===== เวลาทำงาน =====
def get_business_days(start_date: datetime, end_date: datetime) -> int:
    """คำนวณจำนวนวันทำงาน (ไม่รวมเสาร์-อาทิตย์)"""
    business_days = 0
    current_date = start_date
    while current_date <= end_date:
        if current_date.weekday() < 5:
            business_days += 1
        current_date += timedelta(days=1)
    return business_days


# ===== การจัดการเบอร์โทร =====
def clean_phone_number(phone: str) -> str:
    """ทำความสะอาดเบอร์โทรศัพท์ให้เป็นรูปแบบเบอร์ไทย"""
    if not phone:
        return ""
    cleaned = re.sub(r'[^\d]', '', phone)
    if cleaned.startswith('66'):
        cleaned = '0' + cleaned[2:]
    elif len(cleaned) == 9 and not cleaned.startswith('0'):
        cleaned = '0' + cleaned
    return cleaned


# ===== ตัวช่วยตรวจสอบข้อมูล =====
class DataValidator:
    """คลาสสำหรับตรวจสอบข้อมูล"""

    @staticmethod
    def is_not_empty(value: Any) -> bool:
        """ตรวจสอบว่าข้อมูลไม่ว่าง"""
        if value is None:
            return False
        if isinstance(value, str):
            return bool(value.strip())
        if isinstance(value, (list, dict)):
            return bool(value)
        return True

    @staticmethod
    def is_positive_number(value: Any) -> bool:
        """ตรวจสอบว่าเป็นตัวเลขบวก"""
        try:
            return float(value) > 0
        except (ValueError, TypeError):
            return False

    @staticmethod
    def is_valid_date(date_string: str, format_string: str = '%Y-%m-%d') -> bool:
        """ตรวจสอบรูปแบบวันที่"""
        try:
            datetime.strptime(date_string, format_string)
            return True
        except ValueError:
            return False


# ===== ค่าคงที่ =====
DEFAULT_DATE_FORMAT = '%Y-%m-%d'
DEFAULT_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
THAI_DATE_FORMAT = '%d/%m/%Y'
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

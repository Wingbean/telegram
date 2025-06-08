import requests
from config.settings import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from utils.logger import setup_logger
import os
from dotenv import load_dotenv
import re

load_dotenv()

logger = setup_logger(__name__)

def send_report_to_telegram(df):
    filename = os.getenv("SQL_NAME")
    base_dir = os.path.dirname(__file__)
    sql_path = os.path.normpath(os.path.join(base_dir, "..", "sql", filename))

    """หาวันที่ในSQL"""

    # อ่านไฟล์ SQL มาเป็น string
    with open(sql_path, "r", encoding="utf-8") as f:
        sql_text = f.read()

        # ใช้ regex หา pattern วันที่ รูปแบบ "YYYY-MM-DD"
        date_pattern = r'"(\d{4}-\d{2}-\d{2})"'

        match = re.search(date_pattern, sql_text)

        date_str = match.group(1)
    
    if df.empty:
        message = "ไม่พบข้อมูลผู้ป่วยที่เข้าเงื่อนไขในวันนี้"
    else:
        
        intro = f"HN ผู้ป่วยยังไม่มีวันลงทะเบียน\nประจำวันที่ {date_str} \n"
        df_text = df.to_markdown(index=False)
        message = intro + "\n" + df_text

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        response = requests.post(url, data=payload, timeout=10)
        if response.ok:
            logger.info(f"[Telegram] Sent successfully: {response.status_code}")
        else:
            logger.warning(f"[Telegram] Failed: {response.status_code}, {response.text}")
    except Exception as e:
        logger.error(f"[Telegram] Exception occurred: {e}")

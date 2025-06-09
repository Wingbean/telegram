import requests
from config.settings import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from utils.logger import setup_logger
import os
from dotenv import load_dotenv
import re
from datetime import date


load_dotenv()

logger = setup_logger(__name__)

def send_report_to_telegram(df):
    
    date_str = date.today().isoformat()

    if df.empty:
        intro = f"รายงาน HN ผู้ป่วยยังไม่มีวันลงทะเบียน\nประจำวันที่ {date_str} \n"
        message = intro + "--ไม่พบข้อมูลผู้ป่วยที่เข้าเงื่อนไขในวันนี้--"
    else:
        
        intro = f"รายงาน HN ผู้ป่วยยังไม่มีวันลงทะเบียน\nประจำวันที่ {date_str} \n"
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

import requests
from config.settings import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_IDS
from utils.logger import setup_logger
import os
from dotenv import load_dotenv
import re
from datetime import date


load_dotenv()

logger = setup_logger(__name__)

def send_report_to_telegram(df, title, chat_group):

    chat_id = TELEGRAM_CHAT_IDS.get(chat_group)

    if not chat_id:
        logger.warning(f"[Telegram] Unknown [CHAT GROUP]: {chat_group}")
        return
    
    date_str = date.today().isoformat()

    if df.empty:
        intro = f"{title}\nประจำวันที่ {date_str} \n \n"
        message = intro + "--ไม่พบข้อมูลผู้ป่วยที่เข้าเงื่อนไขในวันนี้--"
    else:
        
        intro = f"{title}\n \nประจำวันที่ {date_str} \n"
        df_text = df.to_markdown(index=False)
        message = intro + "\n" + df_text

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }

    try:
        response = requests.post(url, data=payload, timeout=10)
        if response.ok:
            logger.info(f"[Telegram] Sent to GROUP : {chat_group} successfully: {response.status_code}")
        else:
            logger.warning(f"[Telegram] Failed for GROUP: {chat_group}: {response.status_code}, {response.text}")
    except Exception as e:
        logger.error(f"[Telegram] Exception for {chat_group}: {e}")

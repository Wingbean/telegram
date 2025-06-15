#pip install matplotlib
#pip install dataframe-image

import requests
from config.settings import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_IDS
from utils.logger import setup_logger
from dotenv import load_dotenv
from datetime import date
from tabulate import tabulate
import matplotlib.pyplot as plt
import dataframe_image as dfi
import tempfile


load_dotenv()

logger = setup_logger(__name__)

def send_report_to_telegram(df, title, chat_group):

    chat_id = TELEGRAM_CHAT_IDS.get(chat_group)

    if not chat_id:
        logger.warning(f"[Telegram] Unknown [CHAT GROUP]: {chat_group}")
        return
    
    date_str = date.today().isoformat()
    """
    if df.empty:
        intro = f"{title}\nประจำวันที่ {date_str} \n \n"
        message = intro + "--ไม่พบข้อมูลผู้ป่วยที่เข้าเงื่อนไขในวันนี้--"
    else:
        
        intro = f"{title}\n \nประจำวันที่ {date_str} \n"
        #df_text = df.to_markdown(index=False)
        df_text = tabulate(df.values.tolist(), headers=df.columns.tolist(), tablefmt="plain")
        message = intro + "\n" + df_text
    """
    if df.empty:
        message = f"{title}\n\nประจำวันที่ {date_str}\n\n--ไม่พบข้อมูลผู้ป่วยที่เข้าเงื่อนไขในวันนี้--"
    else:
        col_count = len(df.columns)

        # กำหนด colalign ให้ตรงกับจำนวนคอลัมน์ เช่น คอลัมน์แรกชิดกลาง, คอลัมน์สุดท้ายชิดขวา, ที่เหลือชิดซ้าย
        if col_count == 1:
            colalign = ("center",)
        elif col_count == 2:
            colalign = ("center", "right")
        else:
            colalign = ("center",) + ("left",) * (col_count - 2) + ("right",)

        table_text = tabulate(
            df,
            headers="keys",
            tablefmt="psql",
            showindex=False,
            colalign=colalign
        )
        message = f"{title}\n\nประจำวันที่ {date_str}\n\n{table_text}"

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        #"parse_mode": "Markdown"
        #"parse_mode": "HTML"
    }

    try:
        response = requests.post(url, data=payload, timeout=10)
        if response.ok:
            logger.info(f"[Telegram] Sent to GROUP : {chat_group} successfully: {response.status_code}")
        else:
            logger.warning(f"[Telegram] Failed for GROUP: {chat_group}: {response.status_code}, {response.text}")
    except Exception as e:
        logger.error(f"[Telegram] Exception for {chat_group}: {e}")

#--ส่งเป็นรูป

def send_dataframe_as_image(df, title, chat_group):
    chat_id = TELEGRAM_CHAT_IDS.get(chat_group)
    if not chat_id:
        logger.warning(f"[Telegram] Unknown [CHAT GROUP]: {chat_group}")
        return

    try:
        # ซ่อน index ก่อน export
        styler = (
            df.style
            .hide(axis="index")  # ซ่อน index
            .set_caption("รายงานผู้มาใช้บริการแยกแผนก")  # ตั้งหัวตาราง
            .set_table_styles([
                {
                    "selector": "caption",
                    "props": [("color", "#333"), ("font-size", "16px"), ("text-align", "left"), ("font-weight", "bold")]
                },
                {
                    "selector": "thead th",
                    "props": [
                        ("background-color", "#4472C4"),
                        ("color", "white"),
                        ("font-size", "14px"),
                        ("text-align", "center"),
                        ("border", "1px solid #ddd")
                    ]
                },
                {
                    "selector": "td",
                    "props": [
                        ("font-size", "13px"),
                        ("text-align", "center"),
                        ("border", "1px solid #eee"),
                        ("padding", "6px")
                    ]
                }
            ])
            .set_properties(**{
                "font-family": "Tahoma",
                "border-collapse": "collapse",
                "text-align": "center"
            })
            .format(na_rep="-")  # แทนค่า NaN ด้วย -
        )


        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
            dfi.export(styler, tmpfile.name)

        with open(tmpfile.name, 'rb') as photo:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
            response = requests.post(
                url,
                data={"chat_id": chat_id, "caption": title},
                files={"photo": photo},
                timeout=10
            )
            if response.ok:
                logger.info(f"[Telegram] Image sent to GROUP: {chat_group}")
            else:
                logger.warning(f"[Telegram] Image failed for GROUP: {chat_group} - {response.text}")

    except Exception as e:
        logger.error(f"[Telegram] Exception while sending image: {e}")
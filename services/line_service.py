import requests
from datetime import date
from tabulate import tabulate
from config.settings import LINE_ACCESS_TOKEN, LINE_RECIPIENT_IDS
from utils.logger import setup_logger
import tempfile
import dataframe_image as dfi
import json

logger = setup_logger(__name__)

# ส่ง ข้อความ เข้า LINE
def send_report_to_line(df, title, group):

    recipient_id = LINE_RECIPIENT_IDS.get(group)

    if not recipient_id:
        logger.warning(f"[LINE] Unknown group: {group}")
        return

    date_str = date.today().isoformat()

    if df.empty:
        message = f"{title}\n\nประจำวันที่ {date_str}\n\n--ไม่พบข้อมูล--"
    else:
        col_count = len(df.columns)

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

    payload = {
        "to": recipient_id,
        "messages": [
            {
                "type": "text",
                "text": message
            }
        ]
    }

    headers = {
        "Authorization": f"Bearer {LINE_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post("https://api.line.me/v2/bot/message/push", headers=headers, json=payload, timeout=10)
        if response.ok:
            logger.info(f"[LINE] Sent to GROUP: {group} successfully")
        else:
            logger.warning(f"[LINE] Failed to send to GROUP: {group} - {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"[LINE] Exception for GROUP: {group} - {e}")

def send_dataframe_as_line_flex(df, title, group):
    
    recipient_id = LINE_RECIPIENT_IDS.get(group)

    if not recipient_id:
        logger.warning(f"[LINE] Unknown group: {group}")
        return

    try:
        date_str = date.today().strftime("%Y-%m-%d")

        data_rows = []

        # 👇 สร้างหัวตาราง (Header)
        header_row = {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "text",
                    "text": str(col),
                    "size": "sm",
                    "color": "#888888",
                    "weight": "bold",
                    "flex": 1,
                    "wrap": True
                }
                for col in df.columns
            ]
        }
        data_rows.append(header_row)

        # 👇 สร้าง row สำหรับข้อมูล
        for _, row in df.iterrows():
            contents = []
            for i, col in enumerate(df.columns):
                cell = {
                    "type": "text",
                    "text": str(row[col]),
                    "size": "sm",
                    "color": "#111111",
                    "flex": 1,
                    "wrap": True,
                }
                # 👇 ชิดขวาเฉพาะ column สุดท้าย
                if i == len(df.columns) - 1:
                    cell["align"] = "start"
                contents.append(cell)

            data_rows.append({
                "type": "box",
                "layout": "horizontal",
                "contents": contents
            })

        # 👇 สร้าง Flex Message
        flex_message = {
            "type": "flex",
            "altText": title,
            "contents": {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": title,
                            "weight": "bold",
                            "color": "#1DB446",
                            "size": "sm"
                        },
                        {
                            "type": "text",
                            "text": f"วันที่ {date_str}",
                            "weight": "bold",
                            "size": "xxl",
                            "margin": "md"
                        },
                        {
                            "type": "separator",
                            "margin": "xxl"
                        },
                        {
                            "type": "box",
                            "layout": "vertical",
                            "margin": "xxl",
                            "spacing": "sm",
                            "contents": data_rows
                        },
                        {
                            "type": "separator",
                            "margin": "xxl"
                        },
                        {
                            "type": "box",
                            "layout": "horizontal",
                            "margin": "md",
                            "contents": [
                                {
                                    "type": "text",
                                    "text": "Power By",
                                    "size": "xs",
                                    "color": "#aaaaaa",
                                    "flex": 0
                                },
                                {
                                    "type": "text",
                                    "text": "DataSloth",
                                    "color": "#aaaaaa",
                                    "size": "xs",
                                    "align": "end"
                                }
                            ]
                        }
                    ]
                },
                "styles": {
                    "footer": {
                        "separator": True
                    }
                }
            }
        }

        # ส่งข้อความเข้า LINE API
        headers = {
            "Authorization": f"Bearer {LINE_ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }
        payload = {
            "to": recipient_id,
            "messages": [flex_message]
        }
        response = requests.post("https://api.line.me/v2/bot/message/push", headers=headers, json=payload)

        if response.ok:
            logger.info(f"[LINE] Flex message sent to GROUP: {group}")
        else:
            logger.warning(f"[LINE] Flex message failed for GROUP: {group} - {response.text}")

    except Exception as e:
        logger.error(f"[LINE] Exception while sending flex message: {e}")

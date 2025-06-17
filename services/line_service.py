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


def send_dataframe_as_line_image(df, title, group):

    recipient_id = LINE_RECIPIENT_IDS.get(group)

    if not recipient_id:
        logger.warning(f"[LINE] Unknown group: {group}")
        return

    try:
        # สร้าง image จาก dataframe ด้วย styler
        styler = (
            df.style
            .hide(axis="index")
            .set_caption(title)
            .set_table_styles([
                {"selector": "caption", "props": [("font-size", "16px"), ("font-weight", "bold")]},
                {"selector": "thead th", "props": [("background-color", "#4CAF50"), ("color", "white")]}
            ])
            .set_properties(**{
                "font-family": "Tahoma",
                "text-align": "center",
                "border": "1px solid #ccc"
            })
        )

        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
            dfi.export(styler, tmpfile.name)

            with open(tmpfile.name, "rb") as image_file:
                headers = {
                    "Authorization": f"Bearer {LINE_ACCESS_TOKEN}"
                }
                files = {
                    "message": (None, json.dumps({
                        "to": recipient_id,
                        "messages": [{
                            "type": "image",
                            "originalContentUrl": "https://example.com/fake.png",  # Required placeholder
                            "previewImageUrl": "https://example.com/fake.png"
                        }]
                    })),
                    "imageFile": image_file
                }

                response = requests.post("https://api-data.line.me/v2/bot/message/push", headers=headers, files=files)

                if response.ok:
                    logger.info(f"[LINE] Image sent to GROUP: {group}")
                else:
                    logger.warning(f"[LINE] Image failed for GROUP: {group} - {response.text}")

    except Exception as e:
        logger.error(f"[LINE] Exception while sending image: {e}")


def send_dataframe_as_line_flex(df, title, group):

    recipient_id = LINE_RECIPIENT_IDS.get(group)

    if not recipient_id:
        logger.warning(f"[LINE] Unknown group: {group}")
        return

    try:
        date_str = date.today().strftime("%Y-%m-%d")
        rows = []
        for _, row in df.iterrows():
            row_items = []
            for item in row:
                row_items.append({
                    "type": "text",
                    "text": str(item),
                    "size": "sm",
                    "wrap": True
                })
            rows.append({
                "type": "box",
                "layout": "horizontal",
                "contents": row_items,
                "spacing": "sm"
            })

        flex_message = {
            "type": "flex",
            "altText": title,
            "contents": {
                "type": "bubble",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": title, "weight": "bold", "size": "lg"},
                        {"type": "text", "text": f"ประจำวันที่ {date_str}", "size": "xs", "color": "#aaaaaa"}
                    ]
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": rows
                }
            }
        }

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
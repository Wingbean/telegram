import pandas as pd
from decimal import Decimal
from mysql.connector import Error
from database import get_connection, load_sql
from utils.logger import setup_logger

logger = setup_logger(__name__)

def fetch_pending_registration_patients():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = load_sql("noregisdate.sql")
        cursor.execute(query)
        results = cursor.fetchall()

        df = pd.DataFrame(results, columns=['HN', 'Regdate'])

        # แปลง Decimal เป็น string
        df = df.applymap(lambda x: str(x) if isinstance(x, Decimal) else x)

        logger.info(f"Fetched {len(df)} rows from DB.")
        return df

    except Error as e:
        logger.error(f"[DB ERROR] {e}")
        return pd.DataFrame()

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()

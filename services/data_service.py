#pip install pandas

import pandas as pd
from decimal import Decimal
from mysql.connector import Error
from database import get_connection, load_sql
from utils.logger import setup_logger

logger = setup_logger(__name__)

def _fetch_sql_to_df(sql_filename, columns):
    """โหลด SQL, ดึงข้อมูลจาก DB และแปลงเป็น DataFrame"""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = load_sql(sql_filename)
        cursor.execute(query)
        results = cursor.fetchall()

        df = pd.DataFrame(results, columns=columns)

        # แปลง Decimal เป็น string
        df = df.applymap(lambda x: str(x) if isinstance(x, Decimal) else x)

        logger.info(f"Fetched {len(df)} rows from DB from {sql_filename}")
        return df

    except Error as e:
        logger.error(f"[DB ERROR] {e}")
        return pd.DataFrame()

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()


def fetch_noregisdate():
    """ดึงข้อมูลผู้ป่วยที่ยังไม่มีวันลงทะเบียน"""
    return _fetch_sql_to_df("noregisdate.sql", ["HN"])


def fetch_count_pt_dep():
    """ดึงข้อมูลจำนวนผู้ใช้บริการแยกแผนก"""
    return _fetch_sql_to_df("count_pt_dep.sql", ["Code", "Dept", "Count"])

def fetch_count_admit():
    """ดึงข้อมูลจำนวนผู้ป่วย admit แยกวอร์ด"""
    return _fetch_sql_to_df("count_admit.sql", ["Ward", "Count"])

def fetch_ward_status():
    """สถานะเตียงในวอร์ด"""
    return _fetch_sql_to_df("ward_status.sql", ["Ward", "CountBed"])
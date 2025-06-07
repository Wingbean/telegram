# database/queries.py
"""
คลังเก็บ SQL queries ทั้งหมด
ใช้สำหรับจัดการ query ที่ใช้บ่อยหรือซับซ้อน
"""

# ===== Patient Queries =====
PATIENT_NO_REGIS_DATE = """
SELECT o.hn,
MAX(c.regdate)
FROM ovst o
LEFT OUTER JOIN clinicmember c ON o.hn = c.hn
WHERE o.vstdate = CURDATE() AND o.main_dep = '033' AND c.regdate IS NULL
GROUP BY o.hn
;
"""
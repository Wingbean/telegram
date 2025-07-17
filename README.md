# telegram
# Patient Report System

ระบบรายงานข้อมูลผู้ป่วยผ่าน Telegram

## การติดตั้ง

1. Clone repository
2. สร้าง virtual environment: `python -m venv venv`
3. เปิดใช้งาน: `source venv/bin/activate` (Linux/Mac) หรือ `.\venv\Scripts\activate` (Windows)
4. ติดตั้ง dependencies: `pip install -r requirements.txt`
5. คัดลอก `.env.example` เป็น `.env` และแก้ไข
6. สร้างโฟลเดอร์ `sql` และวางไฟล์ SQL
7. รันโปรแกรม: `python main.py`

## โครงสร้างโปรเจกต์

```
project/
├── main.py                 # ไฟล์หลัก
├── config/                 # การตั้งค่า
├── database/              # การจัดการฐานข้อมูล
├── services/              # Business logic
├── utils/                 # Helper functions
├── sql/                   # ไฟล์ SQL
├── logs/                  # ไฟล์ log (สร้างอัตโนมัติ)
└── .env                   # Environment variables
```
## NOTE
### pip install ทั้งหมด
pip install python-dotenv
pip install mysql-connector-python
pip install pandas
pip install requests
pip install tabulate
pip install dataframe-image

pip install playwright
playwright install

pip install matplotlib

pip freeze > requirements.txt

###
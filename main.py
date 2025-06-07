from services.data_service import fetch_pending_registration_patients
from services.telegram_service import send_report_to_telegram

def main():
    df = fetch_pending_registration_patients()
    send_report_to_telegram(df)

if __name__ == "__main__":
    main()

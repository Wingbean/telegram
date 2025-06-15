from services.data_service import fetch_noregisdate, fetch_count_pt_dep
from services.telegram_service import send_report_to_telegram
from services.telegram_service import send_dataframe_as_image

def main():
    df1 = fetch_noregisdate()
    #(df, title, chat_group_name)
    send_report_to_telegram(df1, "รายงาน HN ผู้ป่วยยังไม่มีวันลงทะเบียน", "test")

    df2 = fetch_count_pt_dep()
    #(df, title, chat_group_name)
    send_report_to_telegram(df2, "รายงาน ผู้มาใช้บริการแยกแผนก", "test")
    send_dataframe_as_image(df2, "รายงาน ผู้มาใช้บริการแยกแผนก", "test")

if __name__ == "__main__":
    main()

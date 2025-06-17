from services.data_service import fetch_noregisdate, fetch_count_pt_dep
from services.telegram_service import send_report_to_telegram
from services.telegram_service import send_dataframe_as_image
from services.line_service import send_report_to_line, send_dataframe_as_line_flex

def main():
    df1 = fetch_noregisdate()
    #(df, title, chat_group_name)
    send_report_to_telegram(df1, "รายงาน HN ผู้ป่วยยังไม่มีวันลงทะเบียน", "test")
    send_report_to_line(df1, "รายงาน HN ผู้ป่วยยังไม่มีวันลงทะเบียน", "me")
    send_dataframe_as_line_flex(df1, "รายงาน HN ผู้ป่วยยังไม่มีวันลงทะเบียน", "me")

    df2 = fetch_count_pt_dep()
    #(df, title, chat_group_name)
    send_report_to_telegram(df2, "รายงาน ผู้มาใช้บริการแยกแผนก", "test")
    send_dataframe_as_image(df2, "รายงาน ผู้มาใช้บริการแยกแผนก", "test")
    send_report_to_line(df2, "รายงาน HN ผู้ป่วยยังไม่มีวันลงทะเบียน", "me")
    send_dataframe_as_line_flex(df2, "รายงาน HN ผู้ป่วยยังไม่มีวันลงทะเบียน", "me")

if __name__ == "__main__":
    main()

from datetime import datetime
import time
import tts_client

weekday = [ "월" , "화", "수", "목", "금", "토", "일" ]

def play_date():
    today = datetime.today()
    date_info = "오늘은 {}년 {}월 {}일 {}요일 입니다.".format(
                    today.year,
                    today.month,
                    today.day,
                    weekday[today.weekday()])
    tts_client.pipe_speak(date_info)

def play_time():
    cur_time = time.localtime()
    time_info = "지금 시각은 {}시 {}분 입니다.".format(
                    cur_time.tm_hour,
                    cur_time.tm_min)
    tts_client.pipe_speak(time_info)

if __name__ == '__main__':
    play_date()
    play_time()

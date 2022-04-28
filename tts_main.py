import os
import time
import tts_client
import tts_datetime

menu_item = ["오늘 날짜",
                "현재 시간",
                "음악" ]

menu = None

pipe_path = "/tmp/tts_pipe"
mp3_path = "/home/parksejin/Music/LittleBusTayo4"

def play_mp3():
    filenames = os.listdir(mp3_path)
    for filename in filenames:
        print("filename :", filename)
        print("ext :", filename[-4:])
        if filename[-4:].lower() != ".mp3":
            continue
        full_filename = os.path.join(mp3_path, filename)
        print(full_filename)
        tts_client.pipe_speak(full_filename)

def parse_key(key):
    if key == "KEY_MENU" and not menu:
        tts_client.pipe_speak("메뉴")
        for i in range(len(menu_item)):
            tts_msg = "{}번 {}".format(i, menu_item[i])
            tts_client.pipe_speak(tts_msg)
    elif key == "KEY_0":
        tts_datetime.play_date()
    elif key == "KEY_1":
        tts_datetime.play_time()
    elif key == "KEY_2":
        pass
    elif key == "KEY_3":
        play_mp3()
    elif key == "KEY_STOP":
        tts_client.pipe_speak("clear")
    else:
        print("Cannot handle key : '{}'".format(key))

def main():
    while True:
        time.sleep(0.1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass

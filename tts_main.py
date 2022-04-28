import os
import time
import tts
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
        tts.play_sound(full_filename)

def parse_key(key):
    if key == "KEY_MENU" and not menu:
        tts.tts_speak("메뉴")
        for i in range(len(menu_item)):
            tts_msg = "{}번 {}".format(i, menu_item[i])
            tts.tts_speak(tts_msg)
    elif key == "KEY_0":
        tts_datetime.play_date()
    elif key == "KEY_1":
        tts_datetime.play_time()
    elif key == "KEY_2":
        pass
    elif key == "KEY_3":
        play_mp3()
    else:
        print("Cannot handle key : '{}'".format(key))

def open_pipe():
    if not os.path.exists(pipe_path):
        os.mkfifo(pipe_path)
    os.chmod(pipe_path, 0o666)
    pipe_fd = os.open(pipe_path, os.O_RDONLY | os.O_NONBLOCK)
    return os.fdopen(pipe_fd)

def handle_pipe(pipe):
    message = pipe.readline().strip()
    if message:
        print("Received :", message)
        parse_key(message)

def main():
    pipe = open_pipe()
    while True:
        handle_pipe(pipe)
        time.sleep(0.1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass

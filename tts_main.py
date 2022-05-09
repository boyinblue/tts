import os
import time
import tts_local
import tts_datetime

menu_item = ["오늘 날짜",
                "현재 시간",
                "음악" ]

menu = None
path = None

pipe_path = "/tmp/tts_pipe"
mp3_paths = [
    "/home/parksejin/Music/education/도래미곰뮤지컬/도레미곰-앙앙의턱받.mp3",
    "/home/parksejin/Music/animations/",
    "/home/parksejin/Music/education/",
    "/home/parksejin/Music/english/",
    "/home/parksejin/Music/dinosaur/",
    "/home/parksejin/Music/englishsong/",
    "/home/parksejin/Music/tiki/"
    ]

def list_mp3(path = mp3_paths[0]):
    global menu

    filenames = os.listdir(path)
    menu = filenames
    for idx in range(0, len(filenames)):
        msg = "{}번 {}".format(idx, filenames[idx])
        tts_local.tts_speak(msg)

def list_mp3_parser(key):
    if key == "KEY_0":
        path = path + "/" + menu[0]
    elif key == "KEY_1":
        path = path + "/" + menu[1]
    
    list_mp3(path)

def play_mp3_by_group(idx):
    if idx < len(mp3_paths):
        play_mp3(mp3_paths[idx])

def play_mp3(path = mp3_paths[0]):
    if os.path.isfile(path):
        print(path)
        tts_local.player_add(path)
        return
        
    filenames = os.listdir(path)
    for filename in filenames:
        if filename == "." or filename == "..":
            continue
        print("filename :", filename)
        full_filename = os.path.join(path, filename)
        if os.path.isdir(full_filename):
            play_mp3(full_filename)
            continue

        if filename[-4:].lower() == ".mp3":
            print(full_filename)
            tts_local.player_add(full_filename)
        elif filename[-4:].lower() == ".wav":
            print(full_filename)
            tts_local.player_add(full_filename)
#        elif filename[-4:].lower() == ".mp4":
#            print(full_filename)
#            tts_local.player_add(full_filename)

def parse_key(key):
    global menu, path
    if key == "KEY_MENU":
        menu = None
        path = None
        tts_local.tts_speak("메뉴")
        for i in range(len(menu_item)):
            tts_msg = "{}번 {}".format(i, menu_item[i])
            tts_local.tts_speak(tts_msg)
    elif key == "KEY_0":
        tts_datetime.play_date()
    elif key == "KEY_1":
        tts_datetime.play_time()
    elif key == "KEY_2":
        list_mp3(mp3_paths[0])
    elif key == "KEY_3":
        play_mp3_by_group(0)
    elif key == "KEY_4":
        play_mp3_by_group(1)
    elif key == "KEY_5":
        play_mp3_by_group(2)
    elif key == "KEY_6":
        play_mp3_by_group(3)
    elif key == "KEY_7":
        play_mp3_by_group(4)
    elif key == "KEY_8":
        play_mp3_by_group(5)
    elif key == "KEY_9":
        play_mp3_by_group(6)
    elif key == "KEY_STOP":
        tts_local.player_stop()
    elif key == "KEY_FASTFORWARD":
        tts_local.player_next()
    elif key == "KEY_REWIND":
        tts_local.player_prev()
    elif key == "KEY_PLAY":
        tts_local.player_play()
    elif key == "KEY_PAUSE":
        tts_local.player_pause()
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

import speech_recognition as sr
from gtts import gTTS
import os
import tempfile
import tts_main

def speak(text):
    print("play : ", text)
    fd, filename = tempfile.mkstemp()
    filename = "{}.mp3".format(filename)
    tts = gTTS(text=text, lang='ko')
    tts.save(filename)
    play_mp3(filename)

pipe_path = "/tmp/mp3_player"
pipe_fd = None

def open_pipe():
    global pipe_fd

    if not os.path.exists(pipe_path):
        os.mkfifo(pipe_path)
    os.chmod(pipe_path, 0o666)
    pipe_fd = os.open(pipe_path, os.O_RDWR | os.O_CREAT | os.O_NONBLOCK)
    return os.fdopen(pipe_fd)

def play_mp3(filename):
    global pipe_fd

    if not pipe_fd:
        open_pipe()

    print("fd :", pipe_fd)

    message = "{}\n".format(filename)
    arr = bytes(message, 'utf-8')
    os.write(pipe_fd, arr)
    return
    try:
        fp = open("/tmp/mp3_player", "w")
    except PermissionError:
        print("Permission Error")
        return

def main():
    tts_main.play_mp3()
    return

    speak("안녕하세요. 현업 SW 개발자입니다.")
    speak("안녕하세요. 저는 박선우입니다.")
    speak("안녕하세요. 박선우")
    speak("똥 나와요. 박세진")
    speak("똥 나왔어요. 박서준")
    speak("똥 나와요. 신미현")
    speak("똥 나와요. 아저씨")
    speak("너무 냄새나요 똥")
    speak("옛날 옛적에 응가 박사가 살았어요. 응가 박사는 한 번에 응가를 1톤씩은 싸곤 했어요. 그러던 어느 날, 다른 나라에서 방구 대장이 쳐들어 왔어요. 응가 박사는 방구 대장에 맞서서 열심히 싸웠어요.")
    play_mp3("next")

if __name__ == '__main__':
    main()


import speech_recognition as sr
from gtts import gTTS
import os
import playsound
import tempfile
import threading
import ctypes

play_thread = None
play_filename = None

def speak(text):
    print("play : ", text)
    fd, filename = tempfile.mkstemp()
    filename = "{}.mp3".format(filename)
    tts = gTTS(text=text, lang='ko')
    tts.save(filename)
    play_mp3_sync(filename)
#    os.unlink(filename)

def play_mp3_sync(filename):
    playsound.playsound(filename)

def play_mp3_async(filename):
    global play_thread
    global last_filename

    if play_thread:
        thread_id = None
        if hasattr(play_thread, '_thread_id'):
            thread_id = play_thread._thread_id
        else:
            for id, thread in threading._active.items(): 
                if thread is play_thread: 
                    thread_id = id
                    break

        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
              ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')

        os.unlink(last_filename)

    play_thread = threading.Thread(target=playsound.playsound, args=(filename,), daemon=True)
    play_thread.start()
    last_filename = filename

def main():
    speak("안녕하세요. 현업 SW 개발자입니다.")
    speak("안녕하세요. 저는 박선우입니다.")
    speak("안녕하세요. 박선우")
    speak("똥 나와요. 박세진")
    speak("똥 나왔어요. 박서준")
    speak("똥 나와요. 신미현")
    speak("똥 나와요. 아저씨")
    speak("너무 냄새나요 똥")
    speak("옛날 옛적에 응가 박사가 살았어요. 응가 박사는 한 번에 응가를 1톤씩은 싸곤 했어요. 그러던 어느 날, 다른 나라에서 방구 대장이 쳐들어 왔어요. 응가 박사는 방구 대장에 맞서서 열심히 싸웠어요.")

if __name__ == '__main__':
    main()


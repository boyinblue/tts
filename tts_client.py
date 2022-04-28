import os
import gi
import tempfile
import sys
import time

pipe_path = "/tmp/mp3_player"
pipe = None

def pipe_init():
    global pipe

    if not os.path.exists(pipe_path):
        os.mkfifo(pipe_path)
    os.chmod(pipe_path, 0o666)
    pipe_fd = os.open(pipe_path, os.O_RDWR | os.O_NONBLOCK)
    pipe = os.fdopen(pipe_fd, 'w')

def pipe_speak(message):
    if not pipe:
        pipe_init()

    pipe.write(message + "\n")
    pipe.flush()

def main():
    pipe_speak("반갑습니다.")
    pipe_speak("저는 빡세입니다.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        exit(0)
    
if __name__ == '__main__':
    main()

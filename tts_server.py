import speech_recognition as sr
from gtts import gTTS
import os
import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst
import tempfile
import sys
import threading
import time

playbin = None
loop = None
playlist = []

pipe_path = "/tmp/mp3_player"
pipe = None

def pipe_init():
    global pipe

    if not os.path.exists(pipe_path):
        os.mkfifo(pipe_path)
        os.chmod(pipe_path, 0o666)
    pipe_fd = os.open(pipe_path, os.O_RDONLY | os.O_NONBLOCK)
    pipe = os.fdopen(pipe_fd)

    pipe_thread = threading.Thread(target=pipe_main, 
                    args=(pipe,), daemon=True)
    pipe_thread.start()

def pipe_main(pipe):
    global playlist

    while True:
        try:
            message = pipe.readline().strip()
        except UnicodeDecodeError:
            continue

        if message:
            print("Received :", message)
            if message == "clear":
                print("Playlist cleared")
                playlist.clear()
                playbin.set_state(Gst.State.READY)
            elif os.path.exists(message):
                player_add(message)
            else:
                tts_speak(message)

        time.sleep(0.1)

def pipe_speak(message):
    if not pipe:
        pipe_init()

    pipe.write(message)

def player_main():
    while True:
        player_check_next()
        time.sleep(0.1)
#        print(".")

def player_check_next():
    global playlist

    state = playbin.get_state(Gst.State.NULL)
    if state.state == Gst.State.PLAYING:
        return

    if len(playlist) == 0:
        return

    filename = playlist[0]
    print("Play :", filename)
    del playlist[0]
    if Gst.uri_is_valid(filename):
        uri = filename
    else:
        uri = Gst.filename_to_uri(filename)
    playbin.set_property('uri', uri)

    playbin.set_state(Gst.State.PLAYING)

def player_bus_call(bus, message, loop):
    t = message.type
    if t == Gst.MessageType.EOS:
        playbin.set_state(Gst.State.READY)
        player_check_next()
    elif t == Gst.MessageType.ERROR:
        err, debug = message.parse_error()
        sys.stderr.write("Error: %s: %s\n" % (err, debug))
        loop.quit()
    return True

def player_check_state():
    state = playbin.get_state(Gst.State.NULL)
    if state.state == Gst.State.PLAYING:
        print("Playing")
    elif state.state == Gst.State.READY:
        print("Ready")
    elif state.state == Gst.State.PAUSED:
        print("Paused")
    elif state.state == Gst.State.NULL:
        print("Null")
    else:
        print("Unknown State")
        print(state)

def player_add(filename):
    global playlist

    if not playbin:
        init()

    print("Add :", filename)
    playlist.append(filename)

def player_init():
    global playbin

#    GObject.threads_init()
    Gst.init(None)

    playbin = Gst.ElementFactory.make("playbin", None)
    if not playbin:
        sys.stderr.write("'playbin' gstreamer plugin missing\n")
        sys.exit(1)

    # create and event loop and feed gstreamer bus mesages to it
    loop = GObject.MainLoop()

    bus = playbin.get_bus()
    bus.add_signal_watch()
    bus.connect ("message", player_bus_call, loop)

    play_thread = threading.Thread(target=loop.run, daemon=True)
    play_thread.start()

    play_thread_2 = threading.Thread(target=player_main, daemon=True)
    play_thread_2.start()

def tts_speak(text):
    fd, filename = tempfile.mkstemp()
    try:
        tts = gTTS(text=text, lang='ko')
    except ConnectionError:
        print("Connection Error")
        return
    tts.save(filename)
    player_add(filename)

def init():
    player_init()
    pipe_init()

def main():
    init()

    tts_speak("안녕하세요.")
    tts_speak("저는 뽁스입니다.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        exit(0)
    
if __name__ == '__main__':
    main()

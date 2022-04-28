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

def open_pipe():
    if not os.path.exists(pipe_path):
        os.mkfifo(pipe_path)
    os.chmod(pipe_path, 0o666)
    pipe_fd = os.open(pipe_path, os.O_RDONLY | os.O_NONBLOCK)
    return os.fdopen(pipe_fd)

def handle_pipe(pipe):
    global sensor_option

    message = pipe.readline().strip()
    if message:
        print("Received :", message)
        if message == "clear":
            print("Playlist cleared")
            playlist.clear()
        else:
            play_sound(message)

def check_next():
    if len(playlist):
        filename = playlist[0]
        state = playbin.get_state(Gst.State.NULL)
        if state.state == Gst.State.PLAYING:
            return
        del playlist[0]
        if Gst.uri_is_valid(filename):
            uri = filename
        else:
            uri = Gst.filename_to_uri(filename)
        playbin.set_property('uri', uri)

        playbin.set_state(Gst.State.PLAYING)

def bus_call(bus, message, loop):
    t = message.type
    if t == Gst.MessageType.EOS:
        playbin.set_state(Gst.State.READY)
        check_next()
    elif t == Gst.MessageType.ERROR:
        err, debug = message.parse_error()
        sys.stderr.write("Error: %s: %s\n" % (err, debug))
        loop.quit()
    return True

def check_play_state():
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

def play_sound(filename):
    print("Add :", filename)
    playlist.append(filename)

def speak(text):
    fd, filename = tempfile.mkstemp()
    try:
        tts = gTTS(text=text, lang='ko')
    except ConnectionError:
        print("Connection Error")
        return
    tts.save(filename)
    play_sound(filename)

def init():
    global pipe
    global playbin

    GObject.threads_init()
    Gst.init(None)

    playbin = Gst.ElementFactory.make("playbin", None)
    if not playbin:
        sys.stderr.write("'playbin' gstreamer plugin missing\n")
        sys.exit(1)

    # create and event loop and feed gstreamer bus mesages to it
    loop = GObject.MainLoop()

    bus = playbin.get_bus()
    bus.add_signal_watch()
    bus.connect ("message", bus_call, loop)

    play_thread = threading.Thread(target=loop.run, daemon=True)
    play_thread.start()

    # Create Pipe
    pipe = open_pipe()

def handle():
    handle_pipe(pipe)

def main():
    init()

#    speak("안녕하세요.")
#    speak("저는 뽁스입니다.")

    try:
        while True:
            handle()
            check_next()
            time.sleep(1)
    except KeyboardInterrupt:
        exit(0)
    
if __name__ == '__main__':
    main()


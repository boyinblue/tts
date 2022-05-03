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
stopped = False

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

def player_main():
    while True:
        player_check_next()
        time.sleep(0.1)
#        print(".")

def player_check_next():
    global playlist

    if stopped:
        return

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

def player_add(filename):
    global playlist

    if not playbin:
        player_init()

    print("Add :", filename)
    playlist.append(filename)
    stopped = False

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

def player_clear():
    playlist.clear()
    player_stop()

def player_play():
    if not playbin:
        return
    stopped = False
    playbin.set_state(Gst.State.PLAYING)

def player_stop():
    global stopped

    playbin.set_state(Gst.State.READY)
    stopped = True

def player_next():
    global stopped, playlist

    player_stop()

    stopped = False
    filename = playlist[0]
    print("Play :", filename)
    del playlist[0]
    if Gst.uri_is_valid(filename):
        uri = filename
    else:
        uri = Gst.filename_to_uri(filename)
    playbin.set_property('uri', uri)

    playbin.set_state(Gst.State.PLAYING)

def player_prev():
    stopped = False

def tts_speak(message):
    fd, filename = tempfile.mkstemp()
    try:
        tts = gTTS(text=message, lang='ko')
    except ConnectionError:
        print("Connection Error")
        return
    tts.save(filename)
    player_add(filename)

def main():
    player_init()
    tts_speak("반갑습니다.")
    tts_speak("저는 빡세입니다.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        exit(0)
    
if __name__ == '__main__':
    main()

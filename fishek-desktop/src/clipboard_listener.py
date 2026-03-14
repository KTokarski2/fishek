import pyperclip
import threading
import time

def watch_clipboard(callback):
    previous = pyperclip.paste()

    def loop():
        nonlocal previous
        while True:
            current = pyperclip.paste()
            if current != previous:
                previous = current
                callback(current)
            time.sleep(0.5)

    thread = threading.Thread(target=loop, daemon=True)
    thread.start()
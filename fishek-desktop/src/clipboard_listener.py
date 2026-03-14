import subprocess
import threading
import time
import sys

def get_clipboard():
    try:
        if sys.platform == "win32":
            import pyperclip
            return pyperclip.paste()
        else:
            result = subprocess.run(
                ["xclip", "-selection", "clipboard", "-o"],
                capture_output=True, text=True, timeout=1
            )
            return result.stdout
    except Exception:
        return None
    
def watch_clipboard(callback):
    previous = get_clipboard()
    print(f"[clipboard] start, previous: {repr(previous)}")

    def loop():
        nonlocal previous
        while True:
            try:
                current = get_clipboard()
                print(f"[clipboard] current: {repr(current)}, previous: {repr(previous)}")
                if current and current != previous:
                    previous = current
                    callback(current)
            except Exception as e:
                print(f"[clipboard] error: {e}")
            time.sleep(0.5)

    thread = threading.Thread(target=loop, daemon=True)
    thread.start()
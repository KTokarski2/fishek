import subprocess
import threading
import time
import sys

def get_clipboard():
    try:
        if sys.platform == "win32":
            import ctypes
            ctypes.windll.user32.OpenClipboard(0)
            handle = ctypes.windll.user32.GetClipboardData(13)
            text = ctypes.wstring_at(handle)
            ctypes.windll.user32.CloseClipboard()
            return text
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

    def loop():
        nonlocal previous
        while True:
            try:
                current = get_clipboard()
                if current and current != previous:
                    previous = current
                    callback(current)
            except Exception:
                pass
            time.sleep(0.5)

    thread = threading.Thread(target=loop, daemon=True)
    thread.start()
import subprocess
import threading
import time
import sys

def get_clipboard():
    try:
        if sys.platform == "win32":
            import ctypes
            if not ctypes.windll.user32.OpenClipboard(0):
                return None
            try:
                handle = ctypes.windll.user32.GetClipboardData(13)
                if not handle:
                    return None
                return ctypes.wstring_at(handle)
            finally:
                ctypes.windll.user32.CloseClipboard()
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
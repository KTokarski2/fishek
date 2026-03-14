import os
import sys
from dotenv import load_dotenv
from gui import run_gui

CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".config", "fishek")
ENV_PATH = os.path.join(CONFIG_DIR, ".env")

def is_dev():
    return not getattr(sys, 'frozen', False)

def main():
    if is_dev():
        load_dotenv()
    else:
        os.makedirs(CONFIG_DIR, exist_ok=True)
        load_dotenv(ENV_PATH)
    run_gui()

if __name__ == "__main__":
    main()
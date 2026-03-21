import os
import sys
from dotenv import load_dotenv

def get_config_dir():
    if sys.platform == "win32":
        return os.path.join(os.environ.get("APPDATA", ""), "fishek")
    return os.path.join(os.path.expanduser("~"), ".config", "fishek")

CONFIG_DIR = get_config_dir()
ENV_PATH = os.path.join(CONFIG_DIR, ".env")

def is_dev():
    return not getattr(sys, "frozen", False)

def main():
    if is_dev():
        load_dotenv()
    else:
        os.makedirs(CONFIG_DIR, exist_ok=True)
        load_dotenv(ENV_PATH)
    from gui import main_screen

    main_screen.main_screen()

if __name__ == "__main__":
    main()
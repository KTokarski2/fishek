import os
from dotenv import load_dotenv
from gui import run_gui

def get_config():
    api_key = os.getenv("API_KEY")
    return {
        "api_key": api_key
    }

def main():
    load_dotenv()
    print(get_config())
    run_gui()

if __name__ == "__main__":
    main()
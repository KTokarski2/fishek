import customtkinter as ctk
import clipboard_listener as cl
import os
import sys
from PIL import Image, ImageTk
from sheets_client import append_to_sheet

########### CONFIGURATION ############
THEME = "dark"
COLOR_THEME = "blue"
WIDGET_SCALING = 2.5
WINDOW_SCALING = 2.5
APP_TITLE = "FISHEK Desktop"
APP_SIZE = "400x300"
INPUT_WIDTH = 300
INPUT_HEIGHT = 60
COMBO_OPTIONS = ["ENGLISH", "RUSSIAN", "FRENCH"]
COMBO_WIDTH = 150
COMBO_HEIGHT = 30
BUTTON_TEXT = "Send to Fishek"
BUTTON_WIDTH = 150
BUTTON_HEIGHT = 30
ASSETS_DIR = "assets"
WINDOWS_ICON = "icon.ico"
LINUX_ICON = "icon.png"
######################################

def send_to_fishek(combobox, textbox):
    text = textbox.get("1.0", "end").strip()
    language = combobox.get()
    append_to_sheet(text, language)

def set_textbox_value(textbox, value):
    textbox.delete("1.0", "end")
    textbox.insert("1.0", value)

def set_icon(app):
    assets_dir = os.path.join(os.path.dirname(__file__), "..", ASSETS_DIR)
    if sys.platform == "win32":
        app.iconbitmap(os.path.join(assets_dir, WINDOWS_ICON))
    else:
        img = Image.open(os.path.join(assets_dir, LINUX_ICON))
        app.iconphoto(True, ImageTk.PhotoImage(img))

def run_gui():
    ctk.set_appearance_mode(THEME)
    ctk.set_default_color_theme(COLOR_THEME)
    ctk.set_widget_scaling(WIDGET_SCALING)
    ctk.set_window_scaling(WINDOW_SCALING)
    app = ctk.CTk()
    app.geometry(APP_SIZE)
    app.title(APP_TITLE)
    set_icon(app)
    clipboard_text = {"value": ""}

    textbox = ctk.CTkTextbox(app, width=INPUT_WIDTH, height=INPUT_HEIGHT)
    textbox.pack(pady=20)

    combobox = ctk.CTkComboBox(app, width=COMBO_WIDTH, height=COMBO_HEIGHT, values=COMBO_OPTIONS)
    combobox.pack(pady=20)

    button = ctk.CTkButton(app, text=BUTTON_TEXT, width=BUTTON_WIDTH, height=BUTTON_HEIGHT, command=lambda: send_to_fishek(combobox, textbox))
    button.pack(pady=20)

    def on_clipboard_change(text):
        clipboard_text["value"] = text
        app.after(0, lambda: set_textbox_value(textbox, text))
    cl.watch_clipboard(on_clipboard_change)

    app.mainloop()
    

import customtkinter as ctk
from gui.sheets_screen import show_sheets_screen

APP_GEOMETRY = "800x500"
APP_TITLE = "Fishek Flashcard Builder"
MAIN_SCREEN_HEADER = "Choose an option"
DOWNLOAD_BUTTON_TEXT = "Download from sheet"
GENERATE_BUTTON_TEXT = "Generate Flashcards"
OPTION_BUTTON_WIDTH = 250
OPTION_BUTTON_HEIGHT = 50
OPTION_BUTTON_BORDER_SPACING = 30
MAIN_SCREEN_FONT_SIZE = 48
COMPONENTS_PADDING = 20

def handle_download_button_click(main_frame, app):
    show_sheets_screen(main_frame, app)
    set_resizable(app, True)

def handle_generate_button_click():
    pass

def main_screen_header(parent):
    header = ctk.CTkLabel(
        parent, 
        text=MAIN_SCREEN_HEADER, 
        font=ctk.CTkFont(
            size=MAIN_SCREEN_FONT_SIZE, 
            weight="bold")
        )
    header.pack(side="top", pady=COMPONENTS_PADDING)

def options_buttons(parent):

    google_sheets_button = ctk.CTkButton(
        parent, 
        text=DOWNLOAD_BUTTON_TEXT, 
        font=ctk.CTkFont(size=MAIN_SCREEN_FONT_SIZE), 
        width=OPTION_BUTTON_WIDTH, 
        height=OPTION_BUTTON_HEIGHT,
        border_spacing=OPTION_BUTTON_BORDER_SPACING,
        command=lambda: handle_download_button_click(parent, parent.master))
    
    google_sheets_button.pack(pady=COMPONENTS_PADDING)

    generate_button = ctk.CTkButton(
        parent,
        text=GENERATE_BUTTON_TEXT,
        font=ctk.CTkFont(size=MAIN_SCREEN_FONT_SIZE),
        width=OPTION_BUTTON_WIDTH,
        height=OPTION_BUTTON_HEIGHT,
        border_spacing=OPTION_BUTTON_BORDER_SPACING,
        command=lambda: handle_generate_button_click())
    
    generate_button.pack(pady=COMPONENTS_PADDING)

def set_resizable(app, resizable):
    app.resizable(resizable, resizable)

def main_screen_reinit(app):
    for widget in app.winfo_children():
        widget.destroy()
    app.geometry(APP_GEOMETRY)
    app.attributes("-zoomed", False)
    set_resizable(app, False)
    main_screen_frame = ctk.CTkFrame(app)
    main_screen_header(main_screen_frame)
    options_buttons(main_screen_frame)
    main_screen_frame.pack(fill="both", expand=True)

def main_screen():
    app = ctk.CTk()
    app.title(APP_TITLE)
    app.geometry(APP_GEOMETRY)
    main_screen_frame = ctk.CTkFrame(app)
    set_resizable(app, False)
    main_screen_header(main_screen_frame)
    options_buttons(main_screen_frame)
    main_screen_frame.pack(fill="both", expand=True)
    app.mainloop()
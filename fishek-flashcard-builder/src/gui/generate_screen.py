import customtkinter as ctk
from gui import generation_flow_screen

LANGUAGES = ["English", "French", "Russian"]
DEFAULT_COUNT = 10
MIN_COUNT = 5
MAX_COUNT = 30

TITLE_FONT_SIZE = 52
LABEL_FONT_SIZE = 36
INPUT_FONT_SIZE = 32
ERROR_FONT_SIZE = 28
GENERATE_BTN_FONT_SIZE = 38
BACK_BTN_FONT_SIZE = 32

INPUT_WIDTH = 900
INPUT_HEIGHT = 72
LANGUAGE_MENU_WIDTH = 420
LANGUAGE_MENU_HEIGHT = 72
SLIDER_WIDTH = 900
COUNT_LABEL_WIDTH = 70
GENERATE_BTN_WIDTH = 440
GENERATE_BTN_HEIGHT = 90
BACK_BTN_WIDTH = 300
BACK_BTN_HEIGHT = 72

PRIMARY_COLOR = "#1a5276"
PRIMARY_HOVER = "#2980b9"
NEUTRAL_COLOR = "gray30"
NEUTRAL_HOVER = "gray40"
ERROR_COLOR = "#e74c3c"


def show_generate_screen(main_frame, app):
    for widget in main_frame.winfo_children():
        widget.destroy()

    app.resizable(True, True)

    content = ctk.CTkFrame(main_frame, fg_color="transparent")
    content.place(relx=0.5, rely=0.5, anchor="center")

    ctk.CTkLabel(
        content,
        text="Generate Flashcards",
        font=ctk.CTkFont(size=TITLE_FONT_SIZE, weight="bold"),
    ).pack(pady=(0, 48))

    ctk.CTkLabel(content, text="Topics / Tags", font=ctk.CTkFont(size=LABEL_FONT_SIZE)).pack(anchor="w")
    tags_entry = ctk.CTkEntry(
        content,
        width=INPUT_WIDTH,
        height=INPUT_HEIGHT,
        font=ctk.CTkFont(size=INPUT_FONT_SIZE),
        placeholder_text="e.g. IT vocabulary, business, food, travel",
    )
    tags_entry.pack(pady=(8, 36))

    ctk.CTkLabel(content, text="Source Language", font=ctk.CTkFont(size=LABEL_FONT_SIZE)).pack(anchor="w")
    language_var = ctk.StringVar(value="English")
    ctk.CTkOptionMenu(
        content,
        values=LANGUAGES,
        variable=language_var,
        width=LANGUAGE_MENU_WIDTH,
        height=LANGUAGE_MENU_HEIGHT,
        font=ctk.CTkFont(size=INPUT_FONT_SIZE),
    ).pack(pady=(8, 36), anchor="w")

    count_row = ctk.CTkFrame(content, fg_color="transparent")
    count_row.pack(fill="x", pady=(0, 8))
    ctk.CTkLabel(count_row, text="Number of words", font=ctk.CTkFont(size=LABEL_FONT_SIZE)).pack(side="left")
    count_label = ctk.CTkLabel(
        count_row,
        text=str(DEFAULT_COUNT),
        font=ctk.CTkFont(size=LABEL_FONT_SIZE, weight="bold"),
        width=COUNT_LABEL_WIDTH,
    )
    count_label.pack(side="right")

    count_slider = ctk.CTkSlider(
        content,
        from_=MIN_COUNT,
        to=MAX_COUNT,
        number_of_steps=MAX_COUNT - MIN_COUNT,
        width=SLIDER_WIDTH,
        command=lambda v: count_label.configure(text=str(int(v))),
    )
    count_slider.set(DEFAULT_COUNT)
    count_slider.pack(pady=(0, 48))

    error_label = ctk.CTkLabel(
        content,
        text="",
        text_color=ERROR_COLOR,
        font=ctk.CTkFont(size=ERROR_FONT_SIZE),
    )
    error_label.pack(pady=(0, 12))

    def on_generate():
        tags = tags_entry.get().strip()
        if not tags:
            error_label.configure(text="Please enter at least one topic or tag.")
            return
        error_label.configure(text="")
        count = int(count_slider.get())
        generation_flow_screen.show_generation_flow(main_frame, app, tags, language_var.get(), count)

    ctk.CTkButton(
        content,
        text="Generate  →",
        width=GENERATE_BTN_WIDTH,
        height=GENERATE_BTN_HEIGHT,
        font=ctk.CTkFont(size=GENERATE_BTN_FONT_SIZE, weight="bold"),
        fg_color=PRIMARY_COLOR,
        hover_color=PRIMARY_HOVER,
        command=on_generate,
    ).pack(pady=(0, 16))

    ctk.CTkButton(
        content,
        text="← Back",
        width=BACK_BTN_WIDTH,
        height=BACK_BTN_HEIGHT,
        font=ctk.CTkFont(size=BACK_BTN_FONT_SIZE),
        fg_color=NEUTRAL_COLOR,
        hover_color=NEUTRAL_HOVER,
        command=lambda: _back_to_main(app),
    ).pack()


def _back_to_main(app):
    from gui.main_screen import main_screen_reinit
    main_screen_reinit(app)

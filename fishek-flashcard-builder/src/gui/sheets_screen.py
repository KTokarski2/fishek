import customtkinter as ctk
from gui import main_screen
from services.sheets_client import get_sheet_data
import services.translation_service as ts

APP_PADDING = 20
APP_GEOMETRY = "1600x1000"
TABLE_FONT_SIZE = 35
HEADER_FONT_SIZE = 35
CELL_PAD_X = 12
CELL_PAD_Y = 10
CELL_CORNER_RADIUS = 6
CELL_BORDER_SPACING = 2
HEADER_COLOR = "gray25"
ROW_COLOR = "gray15"
ALT_ROW_COLOR = "gray18"
COLUMN_WEIGHTS = [6, 1, 1]
TABLE_HEADERS = ["Phrase/Word", "Language", "Created at"]
TRANSATE_BUTTON_TEXT = "Translate"
BACK_BUTTON_TEXT = "Back"
BUTTON_WIDTH = 250
BUTTON_HEIGHT = 50
BUTTON_FONT_SIZE = 30
BUTTON_BORDER_SPACING = 30

def handle_translate_button_click(parent):
    print("Translate button clicked")

def handle_back_button_click(main_frame, parent):
    parent.pack_forget()
    main_frame.pack(fill="both", expand=True, padx=APP_PADDING, pady=APP_PADDING)

def show_action_buttons(main_frame, parent):

    buttons_frame = ctk.CTkFrame(parent, fg_color="transparent")
    buttons_frame.pack(pady=APP_PADDING)

    translate_button = ctk.CTkButton(
        buttons_frame,
        text=TRANSATE_BUTTON_TEXT,
        font=ctk.CTkFont(size=BUTTON_FONT_SIZE),
        width=BUTTON_WIDTH,
        height=BUTTON_HEIGHT,
        border_spacing=BUTTON_BORDER_SPACING,
        command=lambda: handle_translate_button_click(parent)
    )

    translate_button.pack(side="left", padx=APP_PADDING)

    back_button = ctk.CTkButton(
        buttons_frame,
        text=BACK_BUTTON_TEXT,
        font=ctk.CTkFont(size=BUTTON_FONT_SIZE),
        width=BUTTON_WIDTH,
        height=BUTTON_HEIGHT,
        border_spacing=BUTTON_BORDER_SPACING,
        command=lambda: handle_back_button_click(main_frame, parent)
    )

    back_button.pack(side="left", padx=APP_PADDING)

def show_flashcards_table(parent, table_data):

    table_frame = ctk.CTkScrollableFrame(parent)
    table_frame.pack(fill="both", expand=True)

    data = [TABLE_HEADERS] + table_data

    for i, row in enumerate(data):
        for j, cell in enumerate(row):

            if i == 0:
                fg_color = HEADER_COLOR
            else:
                fg_color = ROW_COLOR if i % 2 == 0 else ALT_ROW_COLOR

            cell_frame = ctk.CTkFrame(
                table_frame,
                fg_color=fg_color,
                corner_radius=CELL_CORNER_RADIUS
            )
            cell_frame.grid(
                row=i,
                column=j,
                padx=CELL_BORDER_SPACING,
                pady=CELL_BORDER_SPACING,
                sticky="nsew"
            )

            anchor = "w" if j == 0 else "center"

            if i == 0:
                label = ctk.CTkLabel(
                    cell_frame,
                    text=cell,
                    font=ctk.CTkFont(size=HEADER_FONT_SIZE, weight="bold"),
                    anchor=anchor
                )
            else:
                label = ctk.CTkLabel(
                    cell_frame,
                    text=cell,
                    font=ctk.CTkFont(size=TABLE_FONT_SIZE),
                    anchor=anchor
                )

            if j == 0:
                label.pack(fill="x", padx=(20, 10), pady=CELL_PAD_Y)
            else:
                label.pack(fill="x", padx=CELL_PAD_X, pady=CELL_PAD_Y)
    for col, weight in enumerate(COLUMN_WEIGHTS):
        table_frame.grid_columnconfigure(col, weight=weight)


def show_sheets_screen(main_frame, app):
    sheets_screen_frame = ctk.CTkFrame(app)

    table_data = get_sheet_data()

    app.geometry(APP_GEOMETRY)

    main_frame.pack_forget()
    sheets_screen_frame.pack(
        fill="both",
        expand=True,
        padx=APP_PADDING,
        pady=APP_PADDING
    )

    show_flashcards_table(sheets_screen_frame, table_data)
    show_action_buttons(main_frame, sheets_screen_frame)

    print(ts.get_translation("deadline", "English"))
    print(ts.evaluate_translation("deadline", "termin limitowy"))
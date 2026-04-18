import threading
import customtkinter as ctk
import services.translation_service as ts
import services.flashcard_service as fs
import services.decision_service as ds
from gui import main_screen

APP_PADDING = 20

STATUS_FONT_SIZE = 28
HEADER_FONT_SIZE = 22
WORD_FONT_SIZE = 26
TRANSLATION_FONT_SIZE = 26
META_FONT_SIZE = 20
NOTES_FONT_SIZE = 22
FINAL_TITLE_FONT_SIZE = 52
FINAL_COUNT_FONT_SIZE = 28
ACCEPTED_LABEL_FONT_SIZE = 19
NAV_BTN_FONT_SIZE = 20
CONTINUE_BTN_FONT_SIZE = 22
ACTION_BTN_FONT_SIZE = 24
DECISION_BTN_FONT_SIZE = 18

NOTES_WRAPLENGTH = 600
CELL_PAD_Y = 12
CELL_CORNER_RADIUS = 8
CELL_BORDER_SPACING = 4

DECISION_BTN_WIDTH = 120
DECISION_BTN_HEIGHT = 36
NAV_BTN_WIDTH = 140
NAV_BTN_HEIGHT = 44
CONTINUE_BTN_WIDTH = 200
ACTION_BTN_WIDTH = 260
ACTION_BTN_HEIGHT = 54
PROGRESS_BAR_WIDTH = 700
PROGRESS_BAR_HEIGHT = 20
BOTTOM_BAR_HEIGHT = 70

BOTTOM_BAR_COLOR = "gray18"
HEADER_COLOR = "gray20"
ROW_COLOR = "gray13"
ALT_ROW_COLOR = "gray17"

PRIMARY_COLOR = "#1a5276"
PRIMARY_HOVER = "#2980b9"
NEUTRAL_COLOR = "gray30"
NEUTRAL_HOVER = "gray40"
ACCEPT_COLOR = "#1e8449"
ACCEPT_HOVER = "#27ae60"
REFINE_COLOR = "#784212"
REFINE_HOVER = "#a04000"
DROP_COLOR = "#6e2222"
DROP_HOVER = "#922b21"

SCORE_COLORS = {
    "high":   "#2ecc71",
    "medium": "#f39c12",
    "low":    "#e74c3c",
}

COLUMN_WEIGHTS = [3, 3, 2, 4, 1]
TABLE_HEADERS = ["Phrase / Word", "Polish Translation", "Scores", "Notes", "Decision"]


def score_color(val):
    try:
        v = int(val)
        if v >= 8:
            return SCORE_COLORS["high"]
        if v >= 5:
            return SCORE_COLORS["medium"]
        return SCORE_COLORS["low"]
    except (ValueError, TypeError):
        return "gray50"


def score_badge(parent, label_text, score):
    frame = ctk.CTkFrame(parent, fg_color="gray25", corner_radius=6)
    frame.pack(side="left", padx=(0, 6))
    ctk.CTkLabel(
        frame,
        text=label_text,
        font=ctk.CTkFont(size=META_FONT_SIZE),
        text_color="gray70",
    ).pack(side="left", padx=(6, 2))
    ctk.CTkLabel(
        frame,
        text=str(score),
        font=ctk.CTkFont(size=META_FONT_SIZE, weight="bold"),
        text_color=score_color(score),
    ).pack(side="left", padx=(0, 6))


def make_cell(parent, row, col, fg_color):
    cell = ctk.CTkFrame(parent, fg_color=fg_color, corner_radius=CELL_CORNER_RADIUS)
    cell.grid(row=row, column=col, padx=CELL_BORDER_SPACING, pady=CELL_BORDER_SPACING, sticky="nsew")
    return cell


def show_final_screen(frame, app, accepted_translations):
    for widget in frame.winfo_children():
        widget.destroy()

    center = ctk.CTkFrame(frame, fg_color="transparent")
    center.place(relx=0.5, rely=0.5, anchor="center")

    ctk.CTkLabel(
        center,
        text="✓  All done!",
        font=ctk.CTkFont(size=FINAL_TITLE_FONT_SIZE, weight="bold"),
        text_color=SCORE_COLORS["high"],
    ).pack(pady=(0, 8))

    ctk.CTkLabel(
        center,
        text=f"{len(accepted_translations)} translations accepted and ready.",
        font=ctk.CTkFont(size=FINAL_COUNT_FONT_SIZE),
        text_color="gray75",
    ).pack(pady=(0, 40))

    status_label = ctk.CTkLabel(center, text="", font=ctk.CTkFont(size=META_FONT_SIZE), text_color="gray60")
    status_label.pack(pady=(0, 16))

    btn_frame = ctk.CTkFrame(center, fg_color="transparent")
    btn_frame.pack()

    def on_create_flashcards():
        create_btn.configure(state="disabled")
        back_btn.configure(state="disabled")
        status_label.configure(text="Creating flashcards...", text_color="gray60")

        def run():
            failed = fs.create_flashcards(accepted_translations)
            if failed:
                msg = f"Done. {len(accepted_translations) - len(failed)} created. Failed: {', '.join(failed)}"
                color = SCORE_COLORS["medium"]
            else:
                msg = f"✓  {len(accepted_translations)} flashcards created successfully!"
                color = SCORE_COLORS["high"]
            app.after(0, lambda: status_label.configure(text=msg, text_color=color))
            app.after(0, lambda: back_btn.configure(state="normal"))

        threading.Thread(target=run, daemon=True).start()

    def on_back_to_main():
        frame.pack_forget()
        main_screen.main_screen_reinit(app)

    create_btn = ctk.CTkButton(
        btn_frame,
        text="Create Flashcards",
        width=ACTION_BTN_WIDTH,
        height=ACTION_BTN_HEIGHT,
        font=ctk.CTkFont(size=ACTION_BTN_FONT_SIZE, weight="bold"),
        fg_color=PRIMARY_COLOR,
        hover_color=PRIMARY_HOVER,
        command=on_create_flashcards,
    )
    create_btn.pack(side="left", padx=16)

    back_btn = ctk.CTkButton(
        btn_frame,
        text="Back to Main Menu",
        width=ACTION_BTN_WIDTH,
        height=ACTION_BTN_HEIGHT,
        font=ctk.CTkFont(size=ACTION_BTN_FONT_SIZE),
        fg_color=NEUTRAL_COLOR,
        hover_color=NEUTRAL_HOVER,
        command=on_back_to_main,
    )
    back_btn.pack(side="left", padx=16)


def make_decision_toggle(decisions, idx, accept_btn, refine_btn, drop_btn):
    def on_accept():
        decisions[idx] = "accept"
        accept_btn.configure(fg_color=ACCEPT_COLOR, hover_color=ACCEPT_HOVER)
        refine_btn.configure(fg_color=NEUTRAL_COLOR, hover_color=NEUTRAL_HOVER)
        drop_btn.configure(fg_color=NEUTRAL_COLOR, hover_color=NEUTRAL_HOVER)

    def on_refine():
        decisions[idx] = "refine"
        refine_btn.configure(fg_color=REFINE_COLOR, hover_color=REFINE_HOVER)
        accept_btn.configure(fg_color=NEUTRAL_COLOR, hover_color=NEUTRAL_HOVER)
        drop_btn.configure(fg_color=NEUTRAL_COLOR, hover_color=NEUTRAL_HOVER)

    def on_drop():
        decisions[idx] = "drop"
        drop_btn.configure(fg_color=DROP_COLOR, hover_color=DROP_HOVER)
        accept_btn.configure(fg_color=NEUTRAL_COLOR, hover_color=NEUTRAL_HOVER)
        refine_btn.configure(fg_color=NEUTRAL_COLOR, hover_color=NEUTRAL_HOVER)

    accept_btn.configure(command=on_accept)
    refine_btn.configure(command=on_refine)
    drop_btn.configure(command=on_drop)


def build_decision_cell(parent, decisions, idx):
    btn_frame = ctk.CTkFrame(parent, fg_color="transparent")
    btn_frame.pack(expand=True, fill="both", padx=8, pady=CELL_PAD_Y)

    accept_btn = ctk.CTkButton(
        btn_frame,
        text="✓  Accept",
        width=DECISION_BTN_WIDTH,
        height=DECISION_BTN_HEIGHT,
        font=ctk.CTkFont(size=DECISION_BTN_FONT_SIZE),
        fg_color=NEUTRAL_COLOR,
        hover_color=ACCEPT_HOVER,
    )
    accept_btn.pack(pady=(4, 2))

    refine_btn = ctk.CTkButton(
        btn_frame,
        text="↻  Refine",
        width=DECISION_BTN_WIDTH,
        height=DECISION_BTN_HEIGHT,
        font=ctk.CTkFont(size=DECISION_BTN_FONT_SIZE),
        fg_color=REFINE_COLOR,
        hover_color=REFINE_HOVER,
    )
    refine_btn.pack(pady=2)

    drop_btn = ctk.CTkButton(
        btn_frame,
        text="✕  Drop",
        width=DECISION_BTN_WIDTH,
        height=DECISION_BTN_HEIGHT,
        font=ctk.CTkFont(size=DECISION_BTN_FONT_SIZE),
        fg_color=NEUTRAL_COLOR,
        hover_color=DROP_HOVER,
    )
    drop_btn.pack(pady=(2, 4))

    make_decision_toggle(decisions, idx, accept_btn, refine_btn, drop_btn)


def build_results_row(table_frame, i, result):
    word, language, translation, accuracy, naturalness, fluency, notes = result
    row_num = i + 1
    fg = ROW_COLOR if i % 2 == 0 else ALT_ROW_COLOR

    cell = make_cell(table_frame, row_num, 0, fg)
    ctk.CTkLabel(cell, text=word, font=ctk.CTkFont(size=WORD_FONT_SIZE, weight="bold"), anchor="w").pack(fill="x", padx=16, pady=CELL_PAD_Y)

    cell = make_cell(table_frame, row_num, 1, fg)
    ctk.CTkLabel(cell, text=translation, font=ctk.CTkFont(size=TRANSLATION_FONT_SIZE), anchor="w").pack(fill="x", padx=16, pady=CELL_PAD_Y)

    cell = make_cell(table_frame, row_num, 2, fg)
    badges = ctk.CTkFrame(cell, fg_color="transparent")
    badges.pack(padx=12, pady=CELL_PAD_Y, anchor="w")
    score_badge(badges, "ACC", accuracy)
    score_badge(badges, "NAT", naturalness)
    score_badge(badges, "FLU", fluency)

    cell = make_cell(table_frame, row_num, 3, fg)
    ctk.CTkLabel(
        cell,
        text=notes,
        font=ctk.CTkFont(size=NOTES_FONT_SIZE),
        anchor="w",
        text_color="gray75",
        wraplength=NOTES_WRAPLENGTH,
    ).pack(fill="x", padx=16, pady=CELL_PAD_Y)

    return make_cell(table_frame, row_num, 4, fg)


def show_results_table(frame, results, app, accepted_translations, back_callback):
    for widget in frame.winfo_children():
        widget.destroy()

    app.attributes("-zoomed", True)

    decisions = ["refine"] * len(results)

    bottom = ctk.CTkFrame(frame, fg_color=BOTTOM_BAR_COLOR, height=BOTTOM_BAR_HEIGHT, corner_radius=0)
    bottom.pack(fill="x", side="bottom", padx=APP_PADDING, pady=(0, APP_PADDING))
    bottom.pack_propagate(False)

    ctk.CTkButton(
        bottom,
        text="← Back",
        width=NAV_BTN_WIDTH,
        height=NAV_BTN_HEIGHT,
        font=ctk.CTkFont(size=NAV_BTN_FONT_SIZE),
        fg_color=NEUTRAL_COLOR,
        hover_color=NEUTRAL_HOVER,
        command=back_callback,
    ).pack(side="left", padx=20, pady=13)

    ctk.CTkLabel(
        bottom,
        text=f"Accepted: {len(accepted_translations)}  ·  Select decisions then continue",
        font=ctk.CTkFont(size=ACCEPTED_LABEL_FONT_SIZE),
        text_color="gray60",
    ).pack(side="left", padx=10)

    def on_continue():
        accepted, to_refine, _ = ds.partition_decisions(results, decisions)
        accepted_translations.extend(accepted)

        if not to_refine:
            show_final_screen(frame, app, accepted_translations)
            return

        show_refine_progress(frame, app, to_refine, accepted_translations, back_callback)

    ctk.CTkButton(
        bottom,
        text="Continue  →",
        width=CONTINUE_BTN_WIDTH,
        height=NAV_BTN_HEIGHT,
        font=ctk.CTkFont(size=CONTINUE_BTN_FONT_SIZE, weight="bold"),
        fg_color=PRIMARY_COLOR,
        hover_color=PRIMARY_HOVER,
        command=on_continue,
    ).pack(side="right", padx=20, pady=13)

    table_frame = ctk.CTkScrollableFrame(frame, fg_color="transparent")
    table_frame.pack(fill="both", expand=True, padx=APP_PADDING, pady=(APP_PADDING, 0))

    for col, weight in enumerate(COLUMN_WEIGHTS):
        table_frame.grid_columnconfigure(col, weight=weight)

    for j, header in enumerate(TABLE_HEADERS):
        cell = make_cell(table_frame, 0, j, HEADER_COLOR)
        ctk.CTkLabel(
            cell,
            text=header,
            font=ctk.CTkFont(size=HEADER_FONT_SIZE, weight="bold"),
            anchor="w",
        ).pack(fill="x", padx=16, pady=CELL_PAD_Y)

    for i, result in enumerate(results):
        decision_cell = build_results_row(table_frame, i, result)
        build_decision_cell(decision_cell, decisions, i)


def show_refine_progress(frame, app, to_refine, accepted_translations, back_callback):
    for widget in frame.winfo_children():
        widget.destroy()

    center_frame = ctk.CTkFrame(frame, fg_color="transparent")
    center_frame.place(relx=0.5, rely=0.5, anchor="center")

    status_label = ctk.CTkLabel(
        center_frame,
        text=f"Refining 0/{len(to_refine)}...",
        font=ctk.CTkFont(size=STATUS_FONT_SIZE),
    )
    status_label.pack(pady=(0, 20))

    progress_bar = ctk.CTkProgressBar(center_frame, width=PROGRESS_BAR_WIDTH, height=PROGRESS_BAR_HEIGHT)
    progress_bar.set(0)
    progress_bar.pack()

    threading.Thread(
        target=run_refinements,
        args=(to_refine, progress_bar, status_label, frame, app, accepted_translations, back_callback),
        daemon=True,
    ).start()


def run_refinements(to_refine, progress_bar, status_label, frame, app, accepted_translations, back_callback):
    total = len(to_refine)
    new_results = []

    for i, item in enumerate(to_refine):
        word, language, prev_translation, accuracy, naturalness, fluency, notes = item

        new_translation = ts.get_refined_translation(
            word, language, prev_translation, accuracy, naturalness, fluency, notes
        )
        evaluation = ts.evaluate_translation(word, new_translation)
        new_results.append(ds.build_result_row(word, language, new_translation, evaluation))

        progress = (i + 1) / total
        text = f"Refining {i + 1}/{total}..."
        app.after(0, progress_bar.set, progress)
        app.after(0, lambda t=text: status_label.configure(text=t))

    app.after(0, lambda: show_results_table(frame, new_results, app, accepted_translations, back_callback))

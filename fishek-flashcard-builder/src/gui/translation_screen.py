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
CELL_PAD_Y = 12
CELL_CORNER_RADIUS = 8
CELL_BORDER_SPACING = 4
HEADER_COLOR = "gray20"
ROW_COLOR = "gray13"
ALT_ROW_COLOR = "gray17"

DECISION_BTN_WIDTH = 120
DECISION_BTN_HEIGHT = 36
DECISION_BTN_FONT_SIZE = 18

ACCEPT_COLOR = "#1e8449"
ACCEPT_HOVER = "#27ae60"
REFINE_COLOR = "#784212"
REFINE_HOVER = "#a04000"
DROP_COLOR = "#6e2222"
DROP_HOVER = "#922b21"
NEUTRAL_COLOR = "gray30"
NEUTRAL_HOVER = "gray40"

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
        font=ctk.CTkFont(size=52, weight="bold"),
        text_color="#2ecc71",
    ).pack(pady=(0, 8))

    count_label = ctk.CTkLabel(
        center,
        text=f"{len(accepted_translations)} translations accepted and ready.",
        font=ctk.CTkFont(size=28),
        text_color="gray75",
    )
    count_label.pack(pady=(0, 40))

    status_label = ctk.CTkLabel(center, text="", font=ctk.CTkFont(size=20), text_color="gray60")
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
                color = "#f39c12"
            else:
                msg = f"✓  {len(accepted_translations)} flashcards created successfully!"
                color = "#2ecc71"
            app.after(0, lambda: status_label.configure(text=msg, text_color=color))
            app.after(0, lambda: back_btn.configure(state="normal"))

        threading.Thread(target=run, daemon=True).start()

    def on_back_to_main():
        frame.pack_forget()
        main_screen.main_screen_reinit(app)

    create_btn = ctk.CTkButton(
        btn_frame,
        text="Create Flashcards",
        width=260,
        height=54,
        font=ctk.CTkFont(size=24, weight="bold"),
        fg_color="#1a5276",
        hover_color="#2980b9",
        command=on_create_flashcards,
    )
    create_btn.pack(side="left", padx=16)

    back_btn = ctk.CTkButton(
        btn_frame,
        text="Back to Main Menu",
        width=260,
        height=54,
        font=ctk.CTkFont(size=24),
        fg_color="gray30",
        hover_color="gray40",
        command=on_back_to_main,
    )
    back_btn.pack(side="left", padx=16)


def show_results_table(frame, results, app, accepted_translations, sheets_screen_frame):
    for widget in frame.winfo_children():
        widget.destroy()

    app.attributes("-zoomed", True)

    # decisions[i]: "accept" | "refine" | "drop"  — default refine for all
    decisions = ["refine"] * len(results)

    # Bottom action bar — pack BEFORE table so expand=True on table works correctly
    bottom = ctk.CTkFrame(frame, fg_color="gray18", height=70, corner_radius=0)
    bottom.pack(fill="x", side="bottom", padx=APP_PADDING, pady=(0, APP_PADDING))
    bottom.pack_propagate(False)

    def on_back():
        frame.pack_forget()
        sheets_screen_frame.pack(fill="both", expand=True)

    ctk.CTkButton(
        bottom,
        text="← Back",
        width=140,
        height=44,
        font=ctk.CTkFont(size=20),
        fg_color="gray30",
        hover_color="gray40",
        command=on_back,
    ).pack(side="left", padx=20, pady=13)

    total_accepted = len(accepted_translations)
    round_label = ctk.CTkLabel(
        bottom,
        text=f"Accepted: {total_accepted}  ·  Select decisions then continue",
        font=ctk.CTkFont(size=19),
        text_color="gray60",
    )
    round_label.pack(side="left", padx=10)

    def on_continue():
        accepted, to_refine, _ = ds.partition_decisions(results, decisions)
        accepted_translations.extend(accepted)

        if not to_refine:
            show_final_screen(frame, app, accepted_translations)
            return

        _show_progress_and_refine(frame, app, to_refine, accepted_translations, sheets_screen_frame)

    ctk.CTkButton(
        bottom,
        text="Continue  →",
        width=200,
        height=44,
        font=ctk.CTkFont(size=22, weight="bold"),
        fg_color="#1a5276",
        hover_color="#2980b9",
        command=on_continue,
    ).pack(side="right", padx=20, pady=13)

    # Scrollable table
    table_frame = ctk.CTkScrollableFrame(frame, fg_color="transparent")
    table_frame.pack(fill="both", expand=True, padx=APP_PADDING, pady=(APP_PADDING, 0))
    for col, weight in enumerate(COLUMN_WEIGHTS):
        table_frame.grid_columnconfigure(col, weight=weight)

    # Header row
    for j, header in enumerate(TABLE_HEADERS):
        cell = make_cell(table_frame, 0, j, HEADER_COLOR)
        ctk.CTkLabel(
            cell,
            text=header,
            font=ctk.CTkFont(size=HEADER_FONT_SIZE, weight="bold"),
            anchor="w",
        ).pack(fill="x", padx=16, pady=CELL_PAD_Y)

    # Data rows — results format: [word, language, translation, accuracy, naturalness, fluency, notes]
    for i, (word, language, translation, accuracy, naturalness, fluency, notes) in enumerate(results):
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
        ctk.CTkLabel(cell, text=notes, font=ctk.CTkFont(size=NOTES_FONT_SIZE), anchor="w", text_color="gray75", wraplength=600).pack(fill="x", padx=16, pady=CELL_PAD_Y)

        # Decision cell
        decision_cell = make_cell(table_frame, row_num, 4, fg)
        btn_frame = ctk.CTkFrame(decision_cell, fg_color="transparent")
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

        def make_toggle(idx, ab, rb, db):
            def on_accept():
                decisions[idx] = "accept"
                ab.configure(fg_color=ACCEPT_COLOR, hover_color=ACCEPT_HOVER)
                rb.configure(fg_color=NEUTRAL_COLOR, hover_color=NEUTRAL_HOVER)
                db.configure(fg_color=NEUTRAL_COLOR, hover_color=NEUTRAL_HOVER)

            def on_refine():
                decisions[idx] = "refine"
                rb.configure(fg_color=REFINE_COLOR, hover_color=REFINE_HOVER)
                ab.configure(fg_color=NEUTRAL_COLOR, hover_color=NEUTRAL_HOVER)
                db.configure(fg_color=NEUTRAL_COLOR, hover_color=NEUTRAL_HOVER)

            def on_drop():
                decisions[idx] = "drop"
                db.configure(fg_color=DROP_COLOR, hover_color=DROP_HOVER)
                ab.configure(fg_color=NEUTRAL_COLOR, hover_color=NEUTRAL_HOVER)
                rb.configure(fg_color=NEUTRAL_COLOR, hover_color=NEUTRAL_HOVER)

            ab.configure(command=on_accept)
            rb.configure(command=on_refine)
            db.configure(command=on_drop)

        make_toggle(i, accept_btn, refine_btn, drop_btn)


def _show_progress_and_refine(frame, app, to_refine, accepted_translations, sheets_screen_frame):
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

    progress_bar = ctk.CTkProgressBar(center_frame, width=700, height=20)
    progress_bar.set(0)
    progress_bar.pack()

    thread = threading.Thread(
        target=_run_refinements,
        args=(to_refine, progress_bar, status_label, frame, app, accepted_translations, sheets_screen_frame),
        daemon=True,
    )
    thread.start()


def _run_refinements(to_refine, progress_bar, status_label, frame, app, accepted_translations, sheets_screen_frame):
    total = len(to_refine)
    new_results = []

    for i, item in enumerate(to_refine):
        word, language, prev_translation, accuracy, naturalness, fluency, notes = item

        new_translation = ts.get_refined_translation(
            word, language, prev_translation, accuracy, naturalness, fluency, notes
        )
        evaluation = ts.evaluate_translation(word, new_translation)

        new_results.append(ds.build_result_row(
            word, language, new_translation, evaluation
        ))

        progress = (i + 1) / total
        text = f"Refining {i + 1}/{total}..."
        app.after(0, progress_bar.set, progress)
        app.after(0, lambda t=text: status_label.configure(text=t))

    app.after(0, lambda: show_results_table(frame, new_results, app, accepted_translations, sheets_screen_frame))


def run_translations(table_data, progress_bar, status_label, frame, app, accepted_translations, sheets_screen_frame):
    total = len(table_data)
    results = []

    for i, row in enumerate(table_data):
        word = row[0] if len(row) > 0 else ""
        language = row[1] if len(row) > 1 else ""

        translation = ts.get_translation(word, language)
        evaluation = ts.evaluate_translation(word, translation)

        results.append(ds.build_result_row(
            word, language, translation, evaluation
        ))

        progress = (i + 1) / total
        text = f"Translating {i + 1}/{total}..."
        app.after(0, progress_bar.set, progress)
        app.after(0, lambda t=text: status_label.configure(text=t))

    app.after(0, lambda: show_results_table(frame, results, app, accepted_translations, sheets_screen_frame))


def show_translation_screen(sheets_screen_frame, app, table_data):
    accepted_translations = []

    translation_screen_frame = ctk.CTkFrame(app)
    sheets_screen_frame.pack_forget()
    translation_screen_frame.pack(fill="both", expand=True)

    center_frame = ctk.CTkFrame(translation_screen_frame, fg_color="transparent")
    center_frame.place(relx=0.5, rely=0.5, anchor="center")

    status_label = ctk.CTkLabel(
        center_frame,
        text=f"Translating 0/{len(table_data)}...",
        font=ctk.CTkFont(size=STATUS_FONT_SIZE),
    )
    status_label.pack(pady=(0, 20))

    progress_bar = ctk.CTkProgressBar(center_frame, width=700, height=20)
    progress_bar.set(0)
    progress_bar.pack()

    thread = threading.Thread(
        target=run_translations,
        args=(table_data, progress_bar, status_label, translation_screen_frame, app, accepted_translations, sheets_screen_frame),
        daemon=True,
    )
    thread.start()

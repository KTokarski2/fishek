import threading
import customtkinter as ctk
import services.generation_service as gs
import services.translation_service as ts
import services.decision_service as ds
from gui import results_screen

NO_RESULTS_TITLE_FONT_SIZE = 32
NO_RESULTS_SUBTITLE_FONT_SIZE = 22


def show_no_results_screen(frame, back_callback):
    for widget in frame.winfo_children():
        widget.destroy()

    center = ctk.CTkFrame(frame, fg_color="transparent")
    center.place(relx=0.5, rely=0.5, anchor="center")

    ctk.CTkLabel(
        center,
        text="No valid words generated.",
        font=ctk.CTkFont(size=NO_RESULTS_TITLE_FONT_SIZE, weight="bold"),
        text_color=results_screen.SCORE_COLORS["low"],
    ).pack(pady=(0, 12))

    ctk.CTkLabel(
        center,
        text="Try different tags or a different language.",
        font=ctk.CTkFont(size=NO_RESULTS_SUBTITLE_FONT_SIZE),
        text_color="gray70",
    ).pack(pady=(0, 40))

    ctk.CTkButton(
        center,
        text="← Back",
        width=results_screen.NAV_BTN_WIDTH,
        height=results_screen.NAV_BTN_HEIGHT,
        font=ctk.CTkFont(size=results_screen.NAV_BTN_FONT_SIZE),
        fg_color=results_screen.NEUTRAL_COLOR,
        hover_color=results_screen.NEUTRAL_HOVER,
        command=back_callback,
    ).pack()


def run_generation(tags, language, count, progress_bar, status_label, frame, app, accepted_translations, back_callback):
    app.after(0, lambda: status_label.configure(text="Generating word list..."))
    words = gs.generate_word_list(tags, language, count)

    if not words:
        app.after(0, lambda: show_no_results_screen(frame, back_callback))
        return

    results = []
    total = len(words)

    for i, word in enumerate(words):
        text = f"Validating {i + 1}/{total}: {word}"
        app.after(0, lambda t=text: status_label.configure(text=t))

        valid, _ = gs.validate_word(word, language, tags)

        progress = (i + 1) / total
        app.after(0, progress_bar.set, progress)

        if not valid:
            continue

        translation = ts.get_translation(word, language)
        evaluation = ts.evaluate_translation(word, translation)
        results.append(ds.build_result_row(word, language, translation, evaluation))

        text = f"Processing {i + 1}/{total}: {word}"
        app.after(0, lambda t=text: status_label.configure(text=t))

    if not results:
        app.after(0, lambda: show_no_results_screen(frame, back_callback))
        return

    app.after(0, lambda: results_screen.show_results_table(frame, results, app, accepted_translations, back_callback))


def show_generation_flow(config_frame, app, tags, language, count=10):
    accepted_translations = []

    flow_frame = ctk.CTkFrame(app)
    config_frame.pack_forget()
    flow_frame.pack(fill="both", expand=True)

    def back_callback():
        flow_frame.pack_forget()
        config_frame.pack(fill="both", expand=True)

    center_frame = ctk.CTkFrame(flow_frame, fg_color="transparent")
    center_frame.place(relx=0.5, rely=0.5, anchor="center")

    status_label = ctk.CTkLabel(
        center_frame,
        text="Generating word list...",
        font=ctk.CTkFont(size=results_screen.STATUS_FONT_SIZE),
    )
    status_label.pack(pady=(0, 20))

    progress_bar = ctk.CTkProgressBar(center_frame, width=results_screen.PROGRESS_BAR_WIDTH, height=results_screen.PROGRESS_BAR_HEIGHT)
    progress_bar.set(0)
    progress_bar.pack()

    threading.Thread(
        target=run_generation,
        args=(tags, language, count, progress_bar, status_label, flow_frame, app, accepted_translations, back_callback),
        daemon=True,
    ).start()

import threading
import customtkinter as ctk
import services.translation_service as ts
import services.decision_service as ds
from gui import results_screen


def run_translations(table_data, progress_bar, status_label, frame, app, accepted_translations, back_callback):
    total = len(table_data)
    results = []

    for i, row in enumerate(table_data):
        word = row[0] if len(row) > 0 else ""
        language = row[1] if len(row) > 1 else ""

        translation = ts.get_translation(word, language)
        evaluation = ts.evaluate_translation(word, translation)

        results.append(ds.build_result_row(word, language, translation, evaluation))

        progress = (i + 1) / total
        text = f"Translating {i + 1}/{total}..."
        app.after(0, progress_bar.set, progress)
        app.after(0, lambda t=text: status_label.configure(text=t))

    app.after(0, lambda: results_screen.show_results_table(frame, results, app, accepted_translations, back_callback))


def show_translation_screen(sheets_screen_frame, app, table_data):
    accepted_translations = []

    translation_screen_frame = ctk.CTkFrame(app)
    sheets_screen_frame.pack_forget()
    translation_screen_frame.pack(fill="both", expand=True)

    def back_callback():
        translation_screen_frame.pack_forget()
        sheets_screen_frame.pack(fill="both", expand=True)

    center_frame = ctk.CTkFrame(translation_screen_frame, fg_color="transparent")
    center_frame.place(relx=0.5, rely=0.5, anchor="center")

    status_label = ctk.CTkLabel(
        center_frame,
        text=f"Translating 0/{len(table_data)}...",
        font=ctk.CTkFont(size=results_screen.STATUS_FONT_SIZE),
    )
    status_label.pack(pady=(0, 20))

    progress_bar = ctk.CTkProgressBar(center_frame, width=700, height=20)
    progress_bar.set(0)
    progress_bar.pack()

    threading.Thread(
        target=run_translations,
        args=(table_data, progress_bar, status_label, translation_screen_frame, app, accepted_translations, back_callback),
        daemon=True,
    ).start()

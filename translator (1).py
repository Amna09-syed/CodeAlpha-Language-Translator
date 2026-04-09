import tkinter as tk
from tkinter import ttk, messagebox
import threading

# ── dependency check ──────────────────────────────────────────────────────────
try:
    from deep_translator import GoogleTranslator
except ImportError:
    import subprocess, sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "deep-translator", "-q"])
    from deep_translator import GoogleTranslator

try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False

# ── language map ──────────────────────────────────────────────────────────────
LANGUAGES = {
    "Auto Detect":       "auto",
    "Arabic":            "ar",
    "Chinese (Simpl.)":  "zh-CN",
    "Chinese (Trad.)":   "zh-TW",
    "Czech":             "cs",
    "Danish":            "da",
    "Dutch":             "nl",
    "English":           "en",
    "Finnish":           "fi",
    "French":            "fr",
    "German":            "de",
    "Greek":             "el",
    "Hindi":             "hi",
    "Hungarian":         "hu",
    "Indonesian":        "id",
    "Italian":           "it",
    "Japanese":          "ja",
    "Korean":            "ko",
    "Malay":             "ms",
    "Norwegian":         "no",
    "Polish":            "pl",
    "Portuguese":        "pt",
    "Romanian":          "ro",
    "Russian":           "ru",
    "Spanish":           "es",
    "Swedish":           "sv",
    "Tagalog":           "tl",
    "Thai":              "th",
    "Turkish":           "tr",
    "Ukrainian":         "uk",
    "Urdu":              "ur",
    "Vietnamese":        "vi",
}

LANG_NAMES  = list(LANGUAGES.keys())
LANG_CODES  = list(LANGUAGES.values())


# ── helpers ───────────────────────────────────────────────────────────────────
def get_code(display_name: str) -> str:
    return LANGUAGES.get(display_name, "auto")


def speak(text: str, lang_code: str):
    if not TTS_AVAILABLE or not text.strip():
        return
    def _run():
        try:
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
        except Exception:
            pass
    threading.Thread(target=_run, daemon=True).start()


# ── main app ──────────────────────────────────────────────────────────────────
class TranslatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Language Translator")
        self.resizable(True, True)
        self.minsize(700, 460)
        self.configure(bg="#F8F8F6")

        self._build_styles()
        self._build_ui()
        self._auto_timer = None

    # ── styles ────────────────────────────────────────────────────────────────
    def _build_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        BG       = "#F8F8F6"
        CARD     = "#FFFFFF"
        BORDER   = "#D3D1C7"
        PRIMARY  = "#185FA5"
        PRI_TXT  = "#FFFFFF"
        MUTED    = "#888780"
        TEXT     = "#2C2C2A"

        style.configure("TFrame",       background=BG)
        style.configure("Card.TFrame",  background=CARD, relief="flat")
        style.configure("TLabel",       background=BG,   foreground=TEXT, font=("Segoe UI", 10))
        style.configure("Muted.TLabel", background=CARD, foreground=MUTED, font=("Segoe UI", 9))
        style.configure("Head.TLabel",  background=BG,   foreground=TEXT,  font=("Segoe UI", 15, "bold"))
        style.configure("Sub.TLabel",   background=BG,   foreground=MUTED, font=("Segoe UI", 9))
        style.configure("Status.TLabel",background=BG,   foreground=MUTED, font=("Segoe UI", 9, "italic"))

        style.configure("TCombobox",
            fieldbackground=CARD, background=CARD,
            foreground=TEXT, selectbackground=CARD, selectforeground=TEXT,
            font=("Segoe UI", 10), padding=4)
        style.map("TCombobox", fieldbackground=[("readonly", CARD)])

        style.configure("TButton",
            background=CARD, foreground=TEXT,
            font=("Segoe UI", 10), relief="flat",
            borderwidth=1, padding=(10, 6))
        style.map("TButton",
            background=[("active", "#F1EFE8"), ("pressed", "#D3D1C7")],
            relief=[("pressed", "flat")])

        style.configure("Primary.TButton",
            background=PRIMARY, foreground=PRI_TXT,
            font=("Segoe UI", 10, "bold"), relief="flat",
            borderwidth=0, padding=(14, 7))
        style.map("Primary.TButton",
            background=[("active", "#0C447C"), ("pressed", "#042C53")])

        style.configure("Small.TButton",
            background=CARD, foreground=MUTED,
            font=("Segoe UI", 9), relief="flat",
            borderwidth=1, padding=(6, 3))
        style.map("Small.TButton",
            background=[("active", "#F1EFE8")])

        self._colors = dict(BG=BG, CARD=CARD, BORDER=BORDER, TEXT=TEXT, MUTED=MUTED)

    # ── UI ────────────────────────────────────────────────────────────────────
    def _build_ui(self):
        C = self._colors
        root_pad = ttk.Frame(self, padding=20)
        root_pad.pack(fill="both", expand=True)

        # header
        ttk.Label(root_pad, text="Language Translator", style="Head.TLabel").pack(anchor="w")
        ttk.Label(root_pad, text="Translate text between 30+ languages",
                  style="Sub.TLabel").pack(anchor="w", pady=(2, 14))

        # language selector row
        sel_row = ttk.Frame(root_pad)
        sel_row.pack(fill="x", pady=(0, 10))
        sel_row.columnconfigure(0, weight=1)
        sel_row.columnconfigure(2, weight=1)

        self.src_var = tk.StringVar(value="Auto Detect")
        self.tgt_var = tk.StringVar(value="Urdu")

        src_cb = ttk.Combobox(sel_row, textvariable=self.src_var,
                               values=LANG_NAMES, state="readonly", width=22)
        src_cb.grid(row=0, column=0, sticky="ew")

        swap_btn = ttk.Button(sel_row, text="⇄", width=3,
                              command=self._swap_languages)
        swap_btn.grid(row=0, column=1, padx=8)

        tgt_cb = ttk.Combobox(sel_row, textvariable=self.tgt_var,
                               values=LANG_NAMES[1:], state="readonly", width=22)
        tgt_cb.grid(row=0, column=2, sticky="ew")

        # panels
        panels = ttk.Frame(root_pad)
        panels.pack(fill="both", expand=True)
        panels.columnconfigure(0, weight=1)
        panels.columnconfigure(1, weight=1)

        # source card
        src_card = tk.Frame(panels, bg=C["CARD"], bd=1,
                            relief="solid", highlightthickness=0)
        src_card.grid(row=0, column=0, sticky="nsew", padx=(0, 5))

        src_top = tk.Frame(src_card, bg=C["CARD"])
        src_top.pack(fill="x", padx=10, pady=(8, 0))
        tk.Label(src_top, text="SOURCE TEXT", bg=C["CARD"], fg=C["MUTED"],
                 font=("Segoe UI", 8, "bold")).pack(side="left")
        self.char_label = tk.Label(src_top, text="0 / 2000", bg=C["CARD"],
                                   fg=C["MUTED"], font=("Segoe UI", 8))
        self.char_label.pack(side="right")

        self.src_text = tk.Text(src_card, wrap="word", height=9, bd=0, relief="flat",
                                font=("Segoe UI", 11), bg=C["CARD"], fg=C["TEXT"],
                                insertbackground=C["TEXT"], padx=10, pady=8)
        self.src_text.pack(fill="both", expand=True)
        self.src_text.bind("<KeyRelease>", self._on_src_change)

        src_btns = tk.Frame(src_card, bg=C["CARD"])
        src_btns.pack(fill="x", padx=8, pady=6)
        ttk.Button(src_btns, text="✕ Clear",  style="Small.TButton",
                   command=self._clear).pack(side="left", padx=(0, 4))
        ttk.Button(src_btns, text="▶ Listen", style="Small.TButton",
                   command=self._speak_src).pack(side="left")

        # target card
        tgt_card = tk.Frame(panels, bg=C["CARD"], bd=1,
                            relief="solid", highlightthickness=0)
        tgt_card.grid(row=0, column=1, sticky="nsew", padx=(5, 0))

        tgt_top = tk.Frame(tgt_card, bg=C["CARD"])
        tgt_top.pack(fill="x", padx=10, pady=(8, 0))
        tk.Label(tgt_top, text="TRANSLATION", bg=C["CARD"], fg=C["MUTED"],
                 font=("Segoe UI", 8, "bold")).pack(side="left")
        self.status_label = tk.Label(tgt_top, text="", bg=C["CARD"],
                                     fg=C["MUTED"], font=("Segoe UI", 8, "italic"))
        self.status_label.pack(side="right")

        self.tgt_text = tk.Text(tgt_card, wrap="word", height=9, bd=0, relief="flat",
                                font=("Segoe UI", 11), bg=C["CARD"], fg=C["TEXT"],
                                padx=10, pady=8, state="disabled")
        self.tgt_text.pack(fill="both", expand=True)

        tgt_btns = tk.Frame(tgt_card, bg=C["CARD"])
        tgt_btns.pack(fill="x", padx=8, pady=6)
        ttk.Button(tgt_btns, text="⧉ Copy",   style="Small.TButton",
                   command=self._copy).pack(side="left", padx=(0, 4))
        ttk.Button(tgt_btns, text="▶ Listen", style="Small.TButton",
                   command=self._speak_tgt).pack(side="left")

        # footer row
        footer = ttk.Frame(root_pad)
        footer.pack(fill="x", pady=(12, 0))

        self.translate_btn = ttk.Button(footer, text="Translate",
                                        style="Primary.TButton",
                                        command=self._do_translate)
        self.translate_btn.pack(side="left", padx=(0, 8))

        self.auto_btn = ttk.Button(footer, text="⟳  Auto-translate: OFF",
                                   command=self._toggle_auto)
        self.auto_btn.pack(side="left")

        if not TTS_AVAILABLE:
            tk.Label(footer, text="(install pyttsx3 for text-to-speech)",
                     bg=C["BG"], fg=C["MUTED"], font=("Segoe UI", 8)).pack(
                     side="right")

    # ── event handlers ────────────────────────────────────────────────────────
    def _on_src_change(self, _event=None):
        txt = self.src_text.get("1.0", "end-1c")
        self.char_label.config(text=f"{len(txt)} / 2000")
        if len(txt) > 2000:
            self.src_text.delete("1.0 + 2000 chars", "end")
        if self._auto_timer:
            self.after_cancel(self._auto_timer)
        if self._auto_enabled and txt.strip():
            self._auto_timer = self.after(900, self._do_translate)

    def _swap_languages(self):
        src = self.src_var.get()
        tgt = self.tgt_var.get()
        if src == "Auto Detect":
            return
        self.src_var.set(tgt)
        self.tgt_var.set(src)

    def _clear(self):
        self.src_text.delete("1.0", "end")
        self._set_output("")
        self.char_label.config(text="0 / 2000")
        self.status_label.config(text="")

    def _copy(self):
        content = self.tgt_text.get("1.0", "end-1c").strip()
        if content:
            self.clipboard_clear()
            self.clipboard_append(content)
            self.status_label.config(text="Copied!")
            self.after(2000, lambda: self.status_label.config(text=""))

    def _speak_src(self):
        if not TTS_AVAILABLE:
            messagebox.showinfo("TTS unavailable",
                                "Install pyttsx3:\n  pip install pyttsx3")
            return
        speak(self.src_text.get("1.0", "end-1c"), get_code(self.src_var.get()))

    def _speak_tgt(self):
        if not TTS_AVAILABLE:
            messagebox.showinfo("TTS unavailable",
                                "Install pyttsx3:\n  pip install pyttsx3")
            return
        speak(self.tgt_text.get("1.0", "end-1c"), get_code(self.tgt_var.get()))

    _auto_enabled = False

    def _toggle_auto(self):
        self._auto_enabled = not self._auto_enabled
        label = "ON" if self._auto_enabled else "OFF"
        self.auto_btn.config(text=f"⟳  Auto-translate: {label}")

    # ── translation ───────────────────────────────────────────────────────────
    def _set_output(self, text: str):
        self.tgt_text.config(state="normal")
        self.tgt_text.delete("1.0", "end")
        if text:
            self.tgt_text.insert("1.0", text)
        self.tgt_text.config(state="disabled")

    def _do_translate(self):
        text = self.src_text.get("1.0", "end-1c").strip()
        if not text:
            return

        src_code = get_code(self.src_var.get())
        tgt_code = get_code(self.tgt_var.get())

        if src_code != "auto" and src_code == tgt_code:
            self._set_output(text)
            self.status_label.config(text="Same language")
            return

        self.status_label.config(text="Translating…")
        self.translate_btn.config(state="disabled")
        self._set_output("Translating…")

        def _worker():
            try:
                translator = GoogleTranslator(source=src_code, target=tgt_code)
                result = translator.translate(text)
                self.after(0, lambda: self._on_result(result))
            except Exception as exc:
                self.after(0, lambda: self._on_error(str(exc)))

        threading.Thread(target=_worker, daemon=True).start()

    def _on_result(self, result: str):
        self._set_output(result)
        self.status_label.config(text="✓ Done")
        self.translate_btn.config(state="normal")
        self.after(3000, lambda: self.status_label.config(text=""))

    def _on_error(self, msg: str):
        self._set_output("")
        self.status_label.config(text="Error")
        self.translate_btn.config(state="normal")
        messagebox.showerror("Translation error", msg)


# ── entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = TranslatorApp()
    app.mainloop()

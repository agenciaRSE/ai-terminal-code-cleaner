import re
import tkinter as tk
from tkinter import ttk


ZERO_WIDTH_CHARS = (
    "​",
    "‌",
    "‍",
    "⁠",
    "﻿",
    "᠎",
)

DOUBLE_QUOTES = "“”„‟"
SINGLE_QUOTES = "‘’‚‛"
EN_DASH = "–"
EM_DASH = "—"
ELLIPSIS = "…"
NBSP = " "

PROMPT_PATTERNS = [
    re.compile(r"^\$ "),
    re.compile(r"^> "),
    re.compile(r"^PS [^>\n]*> "),
    re.compile(r"^[A-Za-z]:\\[^>\n]*>\s*"),
]

FENCE_RE = re.compile(r"^\s*```[A-Za-z0-9_+\-]*\s*$")


def clean_text(text):
    stats = {
        "original_chars": len(text),
        "invisibles": 0,
        "nbsp": 0,
        "quotes": 0,
        "dashes": 0,
        "ellipsis": 0,
        "crlf": 0,
        "trailing_ws": 0,
        "fences": 0,
        "prompts": 0,
        "final_chars": 0,
    }

    for ch in ZERO_WIDTH_CHARS:
        n = text.count(ch)
        if n:
            stats["invisibles"] += n
            text = text.replace(ch, "")

    n = text.count(NBSP)
    if n:
        stats["nbsp"] = n
        text = text.replace(NBSP, " ")

    for ch in DOUBLE_QUOTES:
        n = text.count(ch)
        if n:
            stats["quotes"] += n
            text = text.replace(ch, '"')
    for ch in SINGLE_QUOTES:
        n = text.count(ch)
        if n:
            stats["quotes"] += n
            text = text.replace(ch, "'")

    n = text.count(EM_DASH)
    if n:
        stats["dashes"] += n
        text = text.replace(EM_DASH, "--")
    n = text.count(EN_DASH)
    if n:
        stats["dashes"] += n
        text = text.replace(EN_DASH, "-")

    n = text.count(ELLIPSIS)
    if n:
        stats["ellipsis"] = n
        text = text.replace(ELLIPSIS, "...")

    crlf = text.count("\r\n")
    text = text.replace("\r\n", "\n")
    lone_cr = text.count("\r")
    text = text.replace("\r", "\n")
    stats["crlf"] = crlf + lone_cr

    cleaned_lines = []
    for line in text.split("\n"):
        if FENCE_RE.match(line):
            stats["fences"] += 1
            continue
        for pat in PROMPT_PATTERNS:
            new_line = pat.sub("", line, count=1)
            if new_line != line:
                stats["prompts"] += 1
                line = new_line
                break
        stripped = line.rstrip(" \t")
        if stripped != line:
            stats["trailing_ws"] += 1
        cleaned_lines.append(stripped)

    while cleaned_lines and cleaned_lines[0] == "":
        cleaned_lines.pop(0)
    while cleaned_lines and cleaned_lines[-1] == "":
        cleaned_lines.pop()

    text = "\n".join(cleaned_lines)
    stats["final_chars"] = len(text)
    return text, stats


def format_status(stats):
    parts = [f"{stats['original_chars']} → {stats['final_chars']} chars"]
    labels = [
        ("invisibles", "invisibles"),
        ("nbsp", "nbsp"),
        ("quotes", "comillas"),
        ("dashes", "guiones"),
        ("ellipsis", "puntos suspensivos"),
        ("crlf", "saltos CR"),
        ("trailing_ws", "líneas con espacios al final"),
        ("fences", "bloques ```"),
        ("prompts", "prompts"),
    ]
    extras = [f"{stats[k]} {label}" for k, label in labels if stats.get(k)]
    if extras:
        parts.extend(extras)
    else:
        parts.append("sin cambios")
    return "  ·  ".join(parts)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Clean spaces 4 AI terminal code")
        self.geometry("780x580")
        self.minsize(540, 380)

        mono = ("Consolas", 10)

        main = ttk.Frame(self, padding=10)
        main.pack(fill="both", expand=True)
        main.columnconfigure(0, weight=1)
        main.rowconfigure(1, weight=1)
        main.rowconfigure(4, weight=1)

        ttk.Label(main, text="Pega aquí el código sucio:").grid(row=0, column=0, sticky="w")

        in_frame = ttk.Frame(main)
        in_frame.grid(row=1, column=0, sticky="nsew", pady=(2, 6))
        in_frame.columnconfigure(0, weight=1)
        in_frame.rowconfigure(0, weight=1)
        self.input = tk.Text(in_frame, font=mono, wrap="char", undo=True, height=10)
        in_scroll = ttk.Scrollbar(in_frame, orient="vertical", command=self.input.yview)
        self.input.configure(yscrollcommand=in_scroll.set)
        self.input.grid(row=0, column=0, sticky="nsew")
        in_scroll.grid(row=0, column=1, sticky="ns")

        in_btns = ttk.Frame(main)
        in_btns.grid(row=2, column=0, sticky="we", pady=(0, 8))
        ttk.Button(in_btns, text="Pegar y limpiar (Ctrl+Shift+V)", command=self.paste_and_clean).pack(side="left")
        ttk.Button(in_btns, text="Limpiar (Ctrl+L)", command=self.clean_now).pack(side="left", padx=(6, 0))
        ttk.Button(in_btns, text="Borrar todo", command=self.clear_all).pack(side="left", padx=(6, 0))

        ttk.Label(main, text="Resultado listo para terminal:").grid(row=3, column=0, sticky="w")

        out_frame = ttk.Frame(main)
        out_frame.grid(row=4, column=0, sticky="nsew", pady=(2, 6))
        out_frame.columnconfigure(0, weight=1)
        out_frame.rowconfigure(0, weight=1)
        self.output = tk.Text(out_frame, font=mono, wrap="char", height=10)
        out_scroll = ttk.Scrollbar(out_frame, orient="vertical", command=self.output.yview)
        self.output.configure(yscrollcommand=out_scroll.set)
        self.output.grid(row=0, column=0, sticky="nsew")
        out_scroll.grid(row=0, column=1, sticky="ns")
        self.output.configure(state="disabled")

        out_btns = ttk.Frame(main)
        out_btns.grid(row=5, column=0, sticky="we", pady=(0, 8))
        ttk.Button(out_btns, text="Copiar resultado (Ctrl+Shift+C)", command=self.copy_result).pack(side="left")

        self.status = tk.StringVar(value="Listo. Pega un comando y pulsa Limpiar (o usa Pegar y limpiar).")
        ttk.Label(main, textvariable=self.status, foreground="#555", anchor="w").grid(row=6, column=0, sticky="we")

        self.input.bind("<<Paste>>", self._on_paste_event, add="+")
        self.bind_all("<Control-l>", lambda e: self.clean_now())
        self.bind_all("<Control-L>", lambda e: self.clean_now())
        self.bind_all("<Control-Shift-V>", lambda e: self.paste_and_clean())
        self.bind_all("<Control-Shift-v>", lambda e: self.paste_and_clean())
        self.bind_all("<Control-Shift-C>", lambda e: self.copy_result())
        self.bind_all("<Control-Shift-c>", lambda e: self.copy_result())

        self.input.focus_set()

    def _set_output(self, text):
        self.output.configure(state="normal")
        self.output.delete("1.0", "end")
        self.output.insert("1.0", text)
        self.output.configure(state="disabled")

    def _on_paste_event(self, _event):
        self.after(10, self.clean_now)

    def clean_now(self):
        raw = self.input.get("1.0", "end-1c")
        cleaned, stats = clean_text(raw)
        self._set_output(cleaned)
        self.status.set(format_status(stats))

    def paste_and_clean(self):
        try:
            clip = self.clipboard_get()
        except tk.TclError:
            self.status.set("Portapapeles vacío o no contiene texto.")
            return
        self.input.delete("1.0", "end")
        self.input.insert("1.0", clip)
        self.clean_now()
        self.copy_result(silent=True)
        self.status.set(self.status.get() + "  ·  Copiado al portapapeles.")

    def copy_result(self, silent=False):
        text = self.output.get("1.0", "end-1c")
        if not text:
            if not silent:
                self.status.set("No hay resultado que copiar.")
            return
        self.clipboard_clear()
        self.clipboard_append(text)
        self.update()
        if not silent:
            self.status.set(f"Copiado al portapapeles ({len(text)} caracteres).")

    def clear_all(self):
        self.input.delete("1.0", "end")
        self._set_output("")
        self.status.set("Listo.")
        self.input.focus_set()


if __name__ == "__main__":
    App().mainloop()

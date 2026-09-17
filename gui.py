import tkinter as tk
from tkinter import ttk
import wordle as wd

COLS = 5
CONTENT_ROWS = 5  # content rows
# Row titles for the content rows
ROW_TITLES = [
    "Green\n(correct position)",
    "Can it appear again\nat another position?",
    "Yellow\n(wrong position)",
    "How often in the word?\n1 = exactly 1x  |  1+ = at least 1x",
    "Grey (not in word)\nclick to exclude",
]
# Wordle colors per row title: (background, foreground)
ROW_COLORS = [("#6aaa64", "white"), ("#6aaa64", "white"), ("#c9b458", "white"), ("#c9b458", "white"), ("#787c7e", "white")]
# Combobox label -> code expected by wordle.COUNT_CHECKS
AMOUNT_OPTIONS = {"1+": ">0", "1": "=1", "2+": ">1", "2": "=2", "3+": ">2", "3": "=3"}
COL_TITLES = ["1st letter", "2nd letter", "3rd letter", "4th letter", "5th letter"]

FONT = ("Segoe UI", 10)
LETTER_FONT = ("Segoe UI", 12, "bold")
BG = "#f5f5f5"
BORDER = "#d3d6da"
GREY = "#787c7e"

root = tk.Tk()
root.title("Wordle-Cheater")
root.configure(bg=BG, padx=10, pady=10)
root.option_add("*Font", FONT)

multi_text_vars = {}    # (content_row, col, i) -> StringVar   i=0..4
text_vars = {}   # (content_row, col) -> StringVar  (content_row: 0..3)
radio_vars = {}  # content_row -> list[StringVar]   (radio rows only)

letter_selected = {}    # 'a'..'z' -> bool
letter_buttons = {}     # 'a'..'z' -> Button
QWERTY_ROWS = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]
ALL_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# only allow a single letter per entry
single_letter = (root.register(lambda p: p == "" or (len(p) == 1 and p.isalpha())), "%P")

def selected_letters_string() -> str:
    # returns the letters that are still available (not clicked/grey)
    return "".join(ch.lower() for ch in ALL_LETTERS if not letter_selected.get(ch, False))

def toggle_letter(ch: str):
    # ch is uppercase
    letter_selected[ch] = not letter_selected.get(ch, False)
    btn = letter_buttons[ch]
    if letter_selected[ch]:
        btn.configure(bg=GREY, fg="white", activebackground=GREY, activeforeground="white")
    else:
        btn.configure(bg=BORDER, fg="black", activebackground=BORDER, activeforeground="black")

def cell_frame(ui_row: int, col: int) -> tk.Frame:
    cell = tk.Frame(root, bg="white", highlightthickness=1, highlightbackground=BORDER)
    cell.grid(row=ui_row, column=col, padx=3, pady=3, sticky="nsew")
    return cell

def letter_entry(parent, var: tk.StringVar, width: int) -> tk.Entry:
    return tk.Entry(parent, textvariable=var, width=width, justify="center", font=LETTER_FONT,
                    relief="flat", highlightthickness=1, highlightbackground=BORDER,
                    validate="key", validatecommand=single_letter)


# Layout:
# row 0: column titles
# rows 1..5: content rows
# row 6: button
# col 0: row titles
# cols 1..5: cells
for r in range(CONTENT_ROWS + 2):  # + header row + button row
    root.grid_rowconfigure(r, weight=1)
for c in range(1, COLS + 1):  # row title column keeps its size
    root.grid_columnconfigure(c, weight=1, uniform="cols")

# Header row: top left empty, then column titles
for c, title in enumerate(COL_TITLES, start=1):
    tk.Label(root, text=title, bg=BG, font=(FONT[0], FONT[1], "bold")).grid(row=0, column=c, pady=(0, 2))

def add_row_title(content_row: int):
    ui_row = content_row + 1
    bg, fg = ROW_COLORS[content_row]
    tk.Label(root, text=ROW_TITLES[content_row], bg=bg, fg=fg, padx=8, pady=6).grid(
        row=ui_row, column=0, padx=3, pady=3, sticky="nsew"
    )

def make_text_row(content_row: int):
    ui_row = content_row + 1
    for c in range(COLS):
        v = tk.StringVar()
        letter_entry(root, v, width=3).grid(row=ui_row, column=c + 1, padx=3, pady=3, sticky="nsew")
        text_vars[(content_row, c)] = v

def make_multi_text_row(content_row: int, per_col: int = 5, options=None):
    """
    One frame per column, containing 'per_col' fields side by side.
    Without options: text fields, with options: read-only comboboxes.
    """
    ui_row = content_row + 1
    for c in range(COLS):
        cell = cell_frame(ui_row, c + 1)

        for i in range(per_col):
            cell.grid_columnconfigure(i, weight=1, uniform="fields")
            if options:
                v = tk.StringVar(value=options[0])
                e = ttk.Combobox(cell, textvariable=v, values=options, width=3, state="readonly", justify="center")
            else:
                v = tk.StringVar()
                e = letter_entry(cell, v, width=2)
            e.grid(row=0, column=i, padx=2, pady=4, sticky="nsew")
            multi_text_vars[(content_row, c, i)] = v

def make_radio_row(content_row: int):
    ui_row = content_row + 1
    radio_vars[content_row] = []
    for c in range(COLS):
        v = tk.IntVar(value=1)  # Default
        radio_vars[content_row].append(v)

        cell = cell_frame(ui_row, c + 1)
        inner = tk.Frame(cell, bg="white")
        inner.place(relx=0.5, rely=0.5, anchor="center")
        tk.Radiobutton(inner, text="Yes", variable=v, value=1, bg="white").pack(side="left")
        tk.Radiobutton(inner, text="No", variable=v, value=0, bg="white").pack(side="left")

def make_available_letters_row(content_row: int):
    # button keyboard instead of an entry
    ui_row = content_row + 1

    cell = tk.Frame(root, bg="white", highlightthickness=1, highlightbackground=BORDER)
    cell.grid(row=ui_row, column=1, columnspan=COLS, padx=3, pady=3, sticky="nsew")

    # centered keyboard
    kb = tk.Frame(cell, bg="white")
    kb.place(relx=0.5, rely=0.5, anchor="center")

    # initialise buttons
    for ch in ALL_LETTERS:
        letter_selected[ch] = False

    for r, row_letters in enumerate(QWERTY_ROWS):
        row_frame = tk.Frame(kb, bg="white")
        row_frame.grid(row=r, column=0, pady=2)

        for i, ch in enumerate(row_letters):
            b = tk.Button(
                row_frame,
                text=ch,
                width=4,
                font=(FONT[0], FONT[1], "bold"),
                relief="flat",
                bg=BORDER,
                activebackground=BORDER,
                cursor="hand2",
                command=lambda x=ch: toggle_letter(x)
            )
            b.grid(row=0, column=i, padx=2)
            letter_buttons[ch] = b

    # the keyboard is placed, so reserve its height in the grid row
    kb.update_idletasks()
    cell.configure(height=kb.winfo_reqheight() + 12)

def extract():
    green = [text_vars[(0, c)].get().strip().lower() for c in range(COLS)]
    green_more_than_once = [radio_vars[1][c].get() for c in range(COLS)]

    # Yellow as 5x5 (columns x fields):
    yellow = []
    yellow_more_than_once = []

    for c in range(COLS):
        y_col = []
        y_mto_col = []
        for i in range(5):
            y_val = multi_text_vars[(2, c, i)].get().strip().lower()
            mto_val = AMOUNT_OPTIONS[multi_text_vars[(3, c, i)].get()]

            y_col.append(y_val)
            y_mto_col.append(mto_val)

        yellow.append(y_col)
        yellow_more_than_once.append(y_mto_col)

    available_letters = selected_letters_string()

    result = {
        "green": green,
        "green_more_than_once": green_more_than_once,
        "yellow": yellow,
        "yellow_more_than_once": yellow_more_than_once,
        "available_letters": available_letters,
    }

    show_results(*wd.extract(result))


def limit_size(win, min_w, min_h, factor):
    """Minimum size, and at most 'factor' times that - never larger than the screen."""
    max_w = min(int(min_w * factor), win.winfo_screenwidth() - 20)
    max_h = min(int(min_h * factor), win.winfo_screenheight() - 80)  # room for the taskbar
    max_w, max_h = max(max_w, min_w), max(max_h, min_h)
    win.minsize(min_w, min_h)
    win.maxsize(max_w, max_h)

    # some window managers (WSLg for example) ignore the limits above, so enforce them here.
    # only once the resizing has settled, otherwise the window flickers while dragging
    job = None

    def clamp(event):
        nonlocal job
        if event.widget is not win:
            return
        w = min(max(event.width, min_w), max_w)
        h = min(max(event.height, min_h), max_h)
        if (w, h) == (event.width, event.height):
            return
        if job:
            win.after_cancel(job)
        job = win.after(200, lambda: win.geometry(f"{w}x{h}"))

    win.bind("<Configure>", clamp)
    return max_w, max_h


def word_list(parent, title, words, color):
    """One column of the result window: heading, count and the words."""
    frame = tk.Frame(parent, bg=BG)
    tk.Label(frame, text=f"{title}  ({len(words)})", bg=color, fg="white",
             font=(FONT[0], 11, "bold"), pady=6).pack(fill="x")

    box = tk.Frame(frame, bg="white", highlightthickness=1, highlightbackground=BORDER)
    box.pack(fill="both", expand=True)
    bar = tk.Scrollbar(box)
    bar.pack(side="right", fill="y")
    # width/height 1: the size comes from the window, not from the text
    text = tk.Text(box, width=1, height=1, wrap="word", relief="flat", padx=10, pady=10,
                   bg="white", font=("Consolas", 11), yscrollcommand=bar.set)
    text.pack(side="left", fill="both", expand=True)
    bar.configure(command=text.yview)

    text.insert("1.0", "   ".join(words) if words else "none")
    text.configure(state="disabled")  # read only, but still selectable for copying
    return frame


def show_results(answers, guesses):
    win = tk.Toplevel(root, bg=BG, padx=10, pady=10)
    win.title("Results")
    win.transient(root)
    win.bind("<Escape>", lambda e: win.destroy())

    # the button first, so it keeps its space at the bottom
    tk.Button(win, text="Close", command=win.destroy, relief="flat", bg=BORDER,
              activebackground=BORDER, cursor="hand2", pady=4).pack(side="bottom", fill="x", pady=(10, 0))

    if not answers and not guesses:
        tk.Label(win, text="No matching words found.", bg=BG, pady=20).pack()
    else:
        panes = tk.Frame(win, bg=BG)
        panes.pack(fill="both", expand=True)
        word_list(panes, "Possible solutions", answers, "#6aaa64").pack(side="left", fill="both", expand=True, padx=(0, 5))
        word_list(panes, "Other allowed guesses", guesses, GREY).pack(side="left", fill="both", expand=True, padx=(5, 0))

    # word lists may be long, so this window may grow more than the main window
    max_w, max_h = limit_size(win, 600, 320, 2.2)
    win.geometry(f"{min(900, max_w)}x{min(560, max_h)}+{root.winfo_rootx() + 40}+{root.winfo_rooty() + 40}")


# Row 1: Green (text)
add_row_title(0)
make_text_row(0)

# Row 2: Can the green letter appear again? (radio)
add_row_title(1)
make_radio_row(1)

# Row 3: Yellow (5 text fields per column, side by side)
add_row_title(2)
make_multi_text_row(2, per_col=5)

# Row 4: How often in the word? (5 comboboxes per column, side by side)
add_row_title(3)
make_multi_text_row(3, per_col=5, options=list(AMOUNT_OPTIONS))

add_row_title(4)
make_available_letters_row(4)

# Button at the bottom
tk.Button(root, text="Find words", command=extract, bg="#6aaa64", fg="white",
          activebackground="#538d4e", activeforeground="white", relief="flat",
          font=(FONT[0], 11, "bold"), cursor="hand2", pady=6).grid(
    row=CONTENT_ROWS + 1, column=0, columnspan=COLS + 1, padx=3, pady=(10, 0), sticky="nsew"
)

# the natural size is the minimum: smaller than this and elements get cut off
root.update_idletasks()
limit_size(root, root.winfo_reqwidth(), root.winfo_reqheight(), 1.25)

root.mainloop()

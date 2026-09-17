import tkinter as tk
from tkinter import messagebox, ttk
import wordle as wd

COLS = 5
CONTENT_ROWS = 5  # content rows
# Row titles for the content rows
ROW_TITLES = ["Green", "More than once?", "Yellow", "How often in the word?\n1 = exactly 1x  |  1+ = at least 1x", "Grey (Not used)"]
# Combobox label -> code expected by consts.create_yellow_dict
AMOUNT_OPTIONS = {"1+": ">0", "1": "=1", "2+": ">1", "2": "=2", "3+": ">2", "3": "=3"}
COL_TITLES = ["1st letter", "2nd letter", "3rd letter", "4th letter", "5th letter"]

root = tk.Tk()
root.title("Wordle-Cheater")

multi_text_vars = {}    # (content_row, col, i) -> StringVar   i=0..4
text_vars = {}   # (content_row, col) -> StringVar  (content_row: 0..3)
available_letters_var = tk.StringVar()  # for row 5 (single field)
radio_vars = {}  # content_row -> list[StringVar]   (radio rows only)

letter_selected = {}    # 'a'..'z' -> bool
letter_buttons = {}     # 'a'..'z' -> Button
QWERTY_ROWS = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]
ALL_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def selected_letters_string() -> str:
    # returns the letters that are still available (not clicked/grey)
    return "".join(ch.lower() for ch in ALL_LETTERS if not letter_selected.get(ch, False))

def toggle_letter(ch: str):
    # ch is uppercase
    letter_selected[ch] = not letter_selected.get(ch, False)
    btn = letter_buttons[ch]
    if letter_selected[ch]:
        btn.configure(bg="#c0c0c0", activebackground="#c0c0c0")  # grey
    else:
        btn.configure(bg="white", activebackground="white")      # white


# Layout:
# row 0: column titles
# rows 1..5: content rows
# row 6: button
# col 0: row titles
# cols 1..5: cells
for r in range(CONTENT_ROWS + 2):  # + header row + button row
    root.grid_rowconfigure(r, weight=1)
for c in range(COLS + 1):  # + row title column
    root.grid_columnconfigure(c, weight=1)

# Header row: top left empty, then column titles
tk.Label(root, text="", padx=6, pady=6).grid(row=0, column=0, padx=4, pady=(4, 2), sticky="nsew")
for c, title in enumerate(COL_TITLES, start=1):
    tk.Label(root, text=title, bd=1, relief="solid", padx=6, pady=6).grid(
        row=0, column=c, padx=4, pady=(4, 2), sticky="nsew"
    )

def add_row_title(content_row: int):
    ui_row = content_row + 1
    tk.Label(root, text=ROW_TITLES[content_row], bd=1, relief="solid", padx=6, pady=6).grid(
        row=ui_row, column=0, padx=4, pady=4, sticky="nsew"
    )

def make_text_row(content_row: int):
    ui_row = content_row + 1
    for c in range(COLS):
        v = tk.StringVar()
        e = tk.Entry(root, textvariable=v, width=12, justify="center")
        e.grid(row=ui_row, column=c + 1, padx=4, pady=4, sticky="nsew")
        text_vars[(content_row, c)] = v

def make_multi_text_row(content_row: int, per_col: int = 5, options=None):
    """
    One frame per column, containing 'per_col' fields side by side.
    Without options: text fields, with options: read-only comboboxes.
    """
    ui_row = content_row + 1
    for c in range(COLS):
        cell = tk.Frame(root, bd=1, relief="solid")
        cell.grid(row=ui_row, column=c + 1, padx=4, pady=4, sticky="nsew")

        for i in range(per_col):
            cell.grid_columnconfigure(i, weight=1)
            if options:
                v = tk.StringVar(value=options[0])
                e = ttk.Combobox(cell, textvariable=v, values=options, width=3, state="readonly", justify="center")
            else:
                v = tk.StringVar()
                e = tk.Entry(cell, textvariable=v, width=3, justify="center")
            e.grid(row=0, column=i, padx=2, pady=2, sticky="nsew")
            multi_text_vars[(content_row, c, i)] = v

def make_radio_row(content_row: int):
    ui_row = content_row + 1
    radio_vars[content_row] = []
    for c in range(COLS):
        v = tk.IntVar(value=1)  # Default
        radio_vars[content_row].append(v)

        frame = tk.Frame(root, bd=1, relief="solid")
        frame.grid(row=ui_row, column=c + 1, padx=4, pady=4, sticky="nsew")

        tk.Radiobutton(frame, text="Yes", variable=v, value=1).pack(anchor="w")
        tk.Radiobutton(frame, text="No", variable=v, value=0).pack(anchor="w")

def make_available_letters_row(content_row: int):
    # button keyboard instead of an entry
    ui_row = content_row + 1

    wrap = tk.Frame(root)
    wrap.grid(row=ui_row, column=1, columnspan=COLS, padx=4, pady=4, sticky="nsew")

    # expand cleanly
    wrap.grid_columnconfigure(0, weight=1)
    wrap.grid_rowconfigure(0, weight=1)

    kb = tk.Frame(wrap, bd=1, relief="solid")
    kb.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

    # initialise buttons
    for ch in ALL_LETTERS:
        letter_selected[ch] = False

    for r, row_letters in enumerate(QWERTY_ROWS):
        row_frame = tk.Frame(kb)
        row_frame.grid(row=r, column=0, pady=2, sticky="nsew")
        row_frame.grid_columnconfigure(tuple(range(10)), weight=1, uniform="kbcol")

       

        for i, ch in enumerate(row_letters):
            b = tk.Button(
                row_frame,
                text=ch,
                width=5,
                bg="white",
                activebackground="white",
                command=lambda x=ch: toggle_letter(x)
            )
            b.grid(row=0, column=i, padx=2, pady=2, sticky="nsew")
            letter_buttons[ch] = b

                
def extract():
    green = [text_vars[(0, c)].get() for c in range(COLS)]
    green_more_than_once = [radio_vars[1][c].get() for c in range(COLS)]
    
    # Yellow as 5x5 (columns x fields):
    yellow = []
    yellow_more_than_once = []

    for c in range(COLS):
        y_col = []
        y_mto_col = []
        for i in range(5):
            y_val = multi_text_vars[(2, c, i)].get().strip()
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

    words = wd.extract(result)
    messagebox.showinfo("Extracted", str(words))


# Row 1: Green (text)
add_row_title(0)
make_text_row(0)

# Row 2: More than once? (radio)
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
tk.Button(root, text="Extract", command=extract).grid(
    row=CONTENT_ROWS + 1, column=0, columnspan=COLS + 1, padx=6, pady=(8, 6), sticky="nsew"
)


root.mainloop()

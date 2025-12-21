import tkinter as tk
from tkinter import messagebox
import wordle as wd

COLS = 5
CONTENT_ROWS = 5  # 4 Inhaltszeilen
# Zeilen-Titel für Inhaltszeilen 1..4
ROW_TITLES = ["Green", "More than once?", "Yellow", "More than once?", "Grey (Not used)"]
COL_TITLES = ["1. Buchstabe", "2. Buchstabe", "3. Buchstabe", "4. Buchstabe", "5. Buchstabe"]

root = tk.Tk()
root.title("Wordle-Cheater")

text_vars = {}   # (content_row, col) -> StringVar  (content_row: 0..3)
available_letters_var = tk.StringVar()  # für Zeile 5 (ein Feld)
radio_vars = {}  # content_row -> list[StringVar]   (nur für Radio-Zeilen)

# Layout:
# row 0: Spaltentitel
# rows 1..4: Inhaltszeilen
# row 5: Button
# col 0: Zeilentitel
# cols 1..5: Zellen
for r in range(CONTENT_ROWS + 2):  # + Kopfzeile + Buttonzeile
    root.grid_rowconfigure(r, weight=1)
for c in range(COLS + 1):  # + Zeilentitelspalte
    root.grid_columnconfigure(c, weight=1)

# Kopfzeile: oben links leer, dann Spaltentitel
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
    ui_row = content_row + 1
    e = tk.Entry(root, textvariable=available_letters_var, justify="left")
    e.grid(row=ui_row, column=1, columnspan=COLS, padx=4, pady=4, sticky="nsew")
    
def extract():
    green = [text_vars[(0, c)].get() for c in range(COLS)]
    green_more_than_once = [radio_vars[1][c].get() for c in range(COLS)]
    yellow = [text_vars[(2, c)].get() for c in range(COLS)]
    yellow_more_than_once = [text_vars[(3, c)].get() for c in range(COLS)]
    available_letters = available_letters_var.get()

    result = {
        "green": green,
        "green_more_than_once": green_more_than_once,
        "yellow": yellow,
        "yellow_more_than_once": yellow_more_than_once,
        "available_letters": available_letters,
    }

    print("\n\n", result,"\n\n")
    words = wd.extract(result)
    messagebox.showinfo("Extrahiert", str(words))


# Zeile 1: Green (Text)
add_row_title(0)
make_text_row(0)

# Zeile 2: More than once? (Radio)
add_row_title(1)
make_radio_row(1)

# Zeile 3: Yellow (Text)
add_row_title(2)
make_text_row(2)

# Zeile 4: More than once? (Radio)
add_row_title(3)
make_text_row(3)

add_row_title(4)
make_available_letters_row(4)

# Button unten
tk.Button(root, text="Extrahieren", command=extract).grid(
    row=CONTENT_ROWS + 1, column=0, columnspan=COLS + 1, padx=6, pady=(8, 6), sticky="nsew"
)


root.mainloop()

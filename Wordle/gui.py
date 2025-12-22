import tkinter as tk
from tkinter import messagebox
import wordle as wd

COLS = 5
CONTENT_ROWS = 5  # 4 Inhaltszeilen
# Zeilen-Titel für Inhaltszeilen 1..4
ROW_TITLES = ["Green", "More than once?", "Yellow", ">0  |  =1  |  >1\n=2  |  >2  |  =3", "Grey (Not used)"]
COL_TITLES = ["1. Buchstabe", "2. Buchstabe", "3. Buchstabe", "4. Buchstabe", "5. Buchstabe"]

root = tk.Tk()
root.title("Wordle-Cheater")

multi_text_vars = {}    # (content_row, col, i) -> StringVar   i=0..4
text_vars = {}   # (content_row, col) -> StringVar  (content_row: 0..3)
available_letters_var = tk.StringVar()  # für Zeile 5 (ein Feld)
radio_vars = {}  # content_row -> list[StringVar]   (nur für Radio-Zeilen)

letter_selected = {}    # 'a'..'z' -> bool
letter_buttons = {}     # 'a'..'z' -> Button
QWERTY_ROWS = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]
ALL_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def selected_letters_string() -> str:
    # liefert die Buchstaben, die "noch verfügbar" sind (nicht angeklickt/grau)
    return "".join(ch.lower() for ch in ALL_LETTERS if not letter_selected.get(ch, False))

def toggle_letter(ch: str):
    # ch ist Großbuchstabe
    letter_selected[ch] = not letter_selected.get(ch, False)
    btn = letter_buttons[ch]
    if letter_selected[ch]:
        btn.configure(bg="#c0c0c0", activebackground="#c0c0c0")  # grau
    else:
        btn.configure(bg="white", activebackground="white")      # weiß


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

def make_multi_text_row(content_row: int, per_col: int = 5):
    """
    Pro Spalte ein Frame, darin 'per_col' Entry-Felder NEBENEINANDER.
    Ergebnis: 5 Textfelder pro Spalte (also 25 Felder in der Zeile).
    """
    ui_row = content_row + 1
    for c in range(COLS):
        cell = tk.Frame(root, bd=1, relief="solid")
        cell.grid(row=ui_row, column=c + 1, padx=4, pady=4, sticky="nsew")

        for i in range(per_col):
            cell.grid_columnconfigure(i, weight=1)
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
    # ersetzt Entry durch Button-Keyboard
    ui_row = content_row + 1

    wrap = tk.Frame(root)
    wrap.grid(row=ui_row, column=1, columnspan=COLS, padx=4, pady=4, sticky="nsew")

    # für sauberes Expand
    wrap.grid_columnconfigure(0, weight=1)
    wrap.grid_rowconfigure(0, weight=1)

    kb = tk.Frame(wrap, bd=1, relief="solid")
    kb.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

    # Buttons initialisieren
    for ch in ALL_LETTERS:
        letter_selected[ch] = False

    for r, row_letters in enumerate(QWERTY_ROWS):
        row_frame = tk.Frame(kb)
        row_frame.grid(row=r, column=0, pady=2, sticky="nsew")
        # gleichmäßige Verteilung in der Zeile
        for i in range(len(row_letters)):
            row_frame.grid_columnconfigure(i, weight=1)

        for i, ch in enumerate(row_letters):
            b = tk.Button(
                row_frame,
                text=ch,
                width=2,
                bg="white",
                activebackground="white",
                command=lambda x=ch: toggle_letter(x)
            )
            b.grid(row=0, column=i, padx=2, pady=2, sticky="nsew")
            letter_buttons[ch] = b
                
def extract():
    green = [text_vars[(0, c)].get() for c in range(COLS)]
    green_more_than_once = [radio_vars[1][c].get() for c in range(COLS)]
    
    # Yellow als 5x5 (Spalten x Felder):
    yellow = []
    yellow_more_than_once = []

    for c in range(COLS):
        y_col = []
        y_mto_col = []
        for i in range(5):
            y_val = multi_text_vars[(2, c, i)].get().strip()
            mto_val = multi_text_vars[(3, c, i)].get().strip()

            # Regel: wenn oben (yellow) befüllt ist und unten leer -> unten als "0" lesen
            if y_val != "" and mto_val == "":
                mto_val = "0"

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

    #print("\n\n", result,"\n\n")
    words = wd.extract(result)
    messagebox.showinfo("Extrahiert", str(words))


# Zeile 1: Green (Text)
add_row_title(0)
make_text_row(0)

# Zeile 2: More than once? (Radio)
add_row_title(1)
make_radio_row(1)

# Zeile 3: Yellow (JETZT: 5 Textfelder pro Spalte nebeneinander)
add_row_title(2)
make_multi_text_row(2, per_col=5)

# Zeile 4: More than once? (JETZT: 5 Textfelder pro Spalte nebeneinander)
add_row_title(3)
make_multi_text_row(3, per_col=5)

add_row_title(4)
make_available_letters_row(4)

# Button unten
tk.Button(root, text="Extrahieren", command=extract).grid(
    row=CONTENT_ROWS + 1, column=0, columnspan=COLS + 1, padx=6, pady=(8, 6), sticky="nsew"
)


root.mainloop()

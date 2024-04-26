from tkinter import Text, END, Button, Toplevel, DISABLED
import webbrowser
from colors import *

def pop_up(root):
    win = Toplevel(root)
    win.geometry("250x150")
    win.configure(bg=BLACK)
    message=(
            "created by parham-mehrabi"
            "\n\r-----------\n\r"
            "- you can find the source code at github,"
            "\n\r- "
            "create issue if you found a bug or have enhancement ideas"
            )
    pop_up_message = Text(
        win,
        fg=LIGHT_GREEN_1,
        bg=BLACK,
        border=0,
        wrap="word"
        )
    Button(
        win,
        text="go to github",
        background=BLUE_2,
        fg=ORANGE_1,
        border=0,
        command=lambda: webbrowser.open("https://github.com/parham-mehrabi/PENcrypt")
        ).grid(column=0, row=0, sticky="s")
    
    pop_up_message.insert(END, message)
    win.columnconfigure(0, weight=1)
    pop_up_message.config(state=DISABLED)
    pop_up_message.grid(column=0, row=1, sticky="n")  
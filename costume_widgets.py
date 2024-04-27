from tkinter import Entry, Button, Label
from colors import *


class CoolEntry(Entry):
        def __init__(self, master=None, **kwargs):
            kwargs.setdefault('background', DARK_GREEN_1)
            kwargs.setdefault('fg', LIGHT_GREEN_1)
            kwargs.setdefault('insertbackground', CYAN_1)
            super().__init__(master=master, **kwargs)

class MenuButton(Button):
    def __init__(self, master=None, **kwargs):
        kwargs.setdefault("background", BLUE_1)
        kwargs.setdefault("border", 0)
        kwargs.setdefault("activebackground", CYAN_1)
        kwargs.setdefault("font", ("Monospace", 15, "bold"))
        kwargs.setdefault("width", 20)
        super().__init__(master=master, **kwargs)

class CoolLabel(Label):
    def __init__(self, master=None, **kwargs):
        kwargs.setdefault('font', ("Monospace", 20))
        kwargs.setdefault('background', BLACK)
        kwargs.setdefault('fg', ORANGE_1)
        super().__init__(master=master, **kwargs)

from tkinter import Tk, Entry, Label, Text

BLACK = "black"
ORANGE = "#c43b00"
DARK_GREEN = "#004011"
LIGHT_GREEN = "#00ff5e"
CYAN_1 = "#00ffc3"

class CoolLabel(Label):
    def __init__(self, master=None, **kwargs):
        kwargs.setdefault('font', ("Monospace", 20))
        kwargs.setdefault('background', BLACK)
        kwargs.setdefault('fg', ORANGE)
        super().__init__(master=master, **kwargs)

class CoolEntry(Entry):
        def __init__(self, master=None, **kwargs):
            kwargs.setdefault('background', DARK_GREEN)
            kwargs.setdefault('fg', LIGHT_GREEN)
            kwargs.setdefault('insertbackground', CYAN_1)
            super().__init__(master=master, **kwargs)

class EncryptUI():
    """ UI """
    def __init__(self) -> None:
        self.main_window:Tk = None
        self.__seed_entry:Entry= None
        self.__input_text:Text = None
    @property
    def screen_size(self):
        return self.main_window.winfo_screenwidth(), self.main_window.winfo_screenheight()
    
    @property
    def __get_seed(self):
        return self.__seed_entry.get() if self.__seed_entry else ""

    def input_on_change(self, _event):
        self.__input_text.edit_modified(False)
        pass
        

    def main(self):
        self.main_window = Tk()
        root = self.main_window
        root.title("PENcrypt")
        root.geometry("1200x700+50+50")
        root.configure(bg=BLACK)
        
        lbl_seed = CoolLabel(root, text="Enter the Password: ")
        entry_seed = CoolEntry(root, width=50)

        txt_input = Text(root, bg=DARK_GREEN, border=0, fg=LIGHT_GREEN, insertbackground=CYAN_1, font=("Monospace"))
        txt_input.bind("<<Modified>>", self.input_on_change)
        

        lbl_seed.grid(row=1, column=0)
        entry_seed.grid(row=1, column=1)
        txt_input.grid(row=2, column=0, columnspan=2, padx=50)

        self.__seed_entry = entry_seed
        self.__input_text = txt_input
        root.mainloop()

main = EncryptUI()
main.main()

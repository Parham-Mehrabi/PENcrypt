from tkinter import Tk, Entry, Label

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
        self.__seed_entry = None
    @property
    def screen_size(self):
        return self.main_window.winfo_screenwidth(), self.main_window.winfo_screenheight()
    
    @property
    def __get_seed(self):
        return self.__seed_entry.get()


    def main(self):
        self.main_window = Tk()
        root = self.main_window
        root.title("PENcrypt")
        root.geometry("1200x700+0+0")
        root.configure(bg="black")
        
        lbl_seed = CoolLabel(root, text="Enter the Password: ")
        entry_seed = CoolEntry(root)


        lbl_seed.grid(row=1, column=0)
        entry_seed.grid(row=1, column=1, rowspan=4, columnspan=4)

        self.__seed_entry = entry_seed
        root.mainloop()

main = EncryptUI()
main.main()

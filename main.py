from tkinter import Tk, Entry, Label, Text, END

BLACK = "black"
ORANGE_1 = "#c43b00"
DARK_GREEN_1 = "#004011"
DARK_GREEN_2 = "#0d5718"
LIGHT_GREEN_1 = "#00ff5e"
CYAN_1 = "#00ffc3"

class CoolLabel(Label):
    def __init__(self, master=None, **kwargs):
        kwargs.setdefault('font', ("Monospace", 20))
        kwargs.setdefault('background', BLACK)
        kwargs.setdefault('fg', ORANGE_1)
        super().__init__(master=master, **kwargs)

class CoolEntry(Entry):
        def __init__(self, master=None, **kwargs):
            kwargs.setdefault('background', DARK_GREEN_1)
            kwargs.setdefault('fg', LIGHT_GREEN_1)
            kwargs.setdefault('insertbackground', CYAN_1)
            super().__init__(master=master, **kwargs)

class EncryptUI():
    """ UI """
    def __init__(self) -> None:
        self.main_window:Tk = None
        self.__seed_entry:Entry= None
        self.__input_text:Text = None
        self.__output:Text = None
    @property
    def screen_size(self):
        return self.main_window.winfo_screenwidth(), self.main_window.winfo_screenheight()
    
    @property
    def __get_seed(self):
        return self.__seed_entry.get() if self.__seed_entry else ""

    def input_on_change(self, _event):
        self.__input_text.edit_modified(False)
        #FIXME
        self.__output.insert(END, "ENCRYPTED TEXT")
        

    def main(self):
        self.main_window = Tk()
        root = self.main_window
        root.title("PENcrypt")
        root.geometry("1200x700+50+50")
        root.configure(bg=BLACK)
        
        lbl_seed = CoolLabel(root, text="Enter the Password: ")
        entry_seed = CoolEntry(root, width=50)

        txt_input = Text(
                        root,
                        bg=DARK_GREEN_1,
                        border=0,
                        fg=LIGHT_GREEN_1,
                        insertbackground=CYAN_1,
                        font=("Monospace"),
                    )
        txt_input.bind("<<Modified>>", self.input_on_change,)
        
        lbl_output = Text (root,
                           background=BLACK,
                           foreground=DARK_GREEN_2,
                           border=0
                        )

        lbl_seed.grid(row=1, column=0)
        entry_seed.grid(row=1, column=1)
        txt_input.grid(row=2, column=0, columnspan=2, padx=50)
        lbl_output.grid(row=1, column=2, rowspan=3)

        self.__seed_entry = entry_seed
        self.__input_text = txt_input
        self.__output = lbl_output
        root.mainloop()

main = EncryptUI()
main.main()

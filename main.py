from tkinter import Tk, Entry, Label, Text, END, Button
from encryptions import create_key, encrypt_data
import base64

BLACK = "black"
ORANGE_1 = "#c43b00"
DARK_GREEN_1 = "#004011"
DARK_GREEN_2 = "#0d5718"
LIGHT_GREEN_1 = "#00ff5e"
BLUE_1 = "#003f52"
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
        self.key = None
        self.salt = None
        self.round = None
        self.salt_round = None

    @property
    def screen_size(self):
        return self.main_window.winfo_screenwidth(), self.main_window.winfo_screenheight()
    
    @property
    def __get_seed(self):
        return self.__seed_entry.get() if self.__seed_entry else ""
    
    def input_on_change(self, _event):
        if self.key:
            encrypted_data = encrypt_data(key=self.key, raw_data=self.__input_text.get("1.0", "end-1c"))
            self.__output.delete("1.0", "end-1c")
            self.__output.insert(END, encrypted_data.decode())
            self.__output.insert(END, self.salt_round)
        self.__input_text.edit_modified(False)
    
    def process_salt_rounds(self) -> None:
        """ process salt_round to collect salt and round """
        self.salt, self.round = (base64.b64decode(self.salt_round)).decode().split(":")

    def process_seed(self):
        if not self.__get_seed:
            print("empty seed ")
            return
        key, self.salt_round = create_key(password=self.__get_seed)
        self.key = key
        self.process_salt_rounds()
        
    def main(self):
        self.main_window = Tk()
        root = self.main_window
        root.title("PENcrypt")
        root.geometry("1200x700+50+50")
        root.configure(bg=BLACK)
        
        lbl_seed = CoolLabel(root, text="Enter the Password: ")
        entry_seed = CoolEntry(root, width=50)
        btn_submit_seed = Button(
            root,
            bg=LIGHT_GREEN_1,
            text="submit password",
            border=0,
            activebackground=BLUE_1,
            font=("Aryal", 12, "bold"),
            command=self.process_seed
        )

        txt_input = Text(
                        root,
                        bg=DARK_GREEN_1,
                        border=0,
                        fg=LIGHT_GREEN_1,
                        insertbackground=CYAN_1,
                        font=("Monospace"),
                    )

        lbl_output = Text(
                        root,
                        background=BLACK,
                        foreground=CYAN_1,
                        border=0,
                        width=40,
                          )

        lbl_seed.grid(row=1, column=0)
        entry_seed.grid(row=1, column=1)
        btn_submit_seed.grid(row=1, column=2)
        txt_input.grid(row=2, column=0, columnspan=4, padx=50)
        lbl_output.grid(row=1, column=4, rowspan=3)

        txt_input.bind("<<Modified>>", self.input_on_change)
        self.__seed_entry = entry_seed
        self.__input_text = txt_input
        self.__output = lbl_output
        root.mainloop()

main = EncryptUI()
main.main()

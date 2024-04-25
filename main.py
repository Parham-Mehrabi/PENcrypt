from tkinter import Tk, Entry, Label, Text, END, Button, Toplevel, DISABLED
from encryptions import create_key, encrypt_data
import base64
import webbrowser

BLACK = "black"
ORANGE_1 = "#c43b00"
DARK_GREEN_1 = "#004011"
DARK_GREEN_2 = "#0d5718"
LIGHT_GREEN_1 = "#00ff5e"
RED_1 = "#cc001f"
BLUE_1 = "#003f52"
BLUE_2 = "#001e52"
CYAN_1 = "#00ffc3"

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

class MenuButton(Button):
    def __init__(self, master=None, **kwargs):
        kwargs.setdefault("background", BLUE_1)
        kwargs.setdefault("border", 0)
        kwargs.setdefault("activebackground", CYAN_1)
        kwargs.setdefault("font", ("Monospace", 15, "bold"))
        kwargs.setdefault("width", 20)
        super().__init__(master=master, **kwargs)

class EncryptUI():
    """ UI """
    def __init__(self) -> None:
        self.main_window:Tk = None
        self.encrypt_window:Tk = None
        self.__seed_entry:Entry= None
        self.__input_text:Text = None
        self.__output:Text = None
        self.key = None
        self.salt = None
        self.round = None
        self.salt_round = None
        self.encrypted_data = None
        self.encrypt_logs = None

    @property
    def screen_size(self):
        return self.main_window.winfo_screenwidth(), self.main_window.winfo_screenheight()
    
    @property
    def __get_seed(self):
        return self.__seed_entry.get() if self.__seed_entry else ""
    
    def input_on_change(self, _event):
        if self.key:
            self.encrypted_data = encrypt_data(key=self.key, raw_data=self.__input_text.get("1.0", "end-1c"))
            self.__output.delete("1.0", "end-1c")
            self.__output.insert(END, self.encrypted_data.decode())
            self.__output.insert(END, self.salt_round)
        self.__input_text.edit_modified(False)
    
    def process_salt_rounds(self) -> None:
        """ process salt_round to collect salt and round """
        self.salt, self.round = (base64.b64decode(self.salt_round)).decode().split(":")

    def process_seed(self):
        if not self.__get_seed:
            self.encrypt_logs.delete("1.0", "end-1c")
            self.encrypt_logs.insert(END, "empty seed\n")
            return
        self.key, self.salt_round = create_key(password=self.__get_seed)
        self.encrypt_logs.insert(END, f"key: {base64.urlsafe_b64decode(self.key)}\n")
        self.encrypt_logs.insert(END, f"salt: {base64.urlsafe_b64decode(self.salt_round).decode()}\n")
        self.process_salt_rounds()
        return
    
    def save_encrypted_data(self):
        pass

    def encrypt_win(self):
        self.main_window.destroy()
        self.encrypt_window = Tk()
        root = self.encrypt_window
        root.title("PENcrypt")
        root.geometry("1200x600+50+50")
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
        btn_save = Button(
            root,
            text="save",
            fg=RED_1,
            bg=LIGHT_GREEN_1,
            font=("Monospace", 15),
            command=self.save_encrypted_data
        )
        logs = Text(root, background=BLACK, foreground=RED_1, border=0, height=10)
        lbl_seed.grid(row=1, column=0)
        entry_seed.grid(row=1, column=1)
        btn_submit_seed.grid(row=1, column=2)
        txt_input.grid(row=2, column=0, columnspan=4, padx=50)
        lbl_output.grid(row=1, column=4, rowspan=3)
        btn_save.grid(row=3, column=4)
        logs.grid(row=3, column=0, columnspan=4)
        txt_input.bind("<<Modified>>", self.input_on_change)
        self.__seed_entry = entry_seed
        self.encrypt_logs = logs
        self.__input_text = txt_input
        self.__output = lbl_output

    def main(self):
        self.main_window = Tk()
        root = self.main_window
        root.title("PENcrypt")
        root.geometry("600x350+50+50")
        root.configure(bg=BLACK)
        CoolLabel(root, text="PENcrypt", fg=CYAN_1, font=("Arial", 20, "bold")).grid(column=0, row=0)
        MenuButton(root, text="Encrypt", command=self.encrypt_win).grid(column=0, row=1, padx=10, pady=5)
        MenuButton(root, text="Decrypt").grid(column=0, row=2, padx=10, pady=5)
        MenuButton(root, text="Source Code", command=lambda: pop_up(root=root)).grid(column=0, row=3, padx=10, pady=5)
        MenuButton(root, text="Exit", command=root.destroy).grid(column=0, row=4, padx=10, pady=5)
        
        root.columnconfigure(0, weight=1)
        root.mainloop()
main = EncryptUI()
main.main()

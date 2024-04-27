from tkinter import Tk, Entry, Text, END, Button, DISABLED, NORMAL, filedialog
from cryptography.fernet import InvalidToken
import pickle
import os
from colors import *
from encryptions import create_key, encrypt_data, decrypt_data, recreate_key
from costume_widgets import CoolEntry, MenuButton, CoolLabel
from popup import pop_up
from utils import unique_pickle_path


class EncryptUI():
    """ UI """
    def __init__(self) -> None:
        self.main_window:Tk = None
        self.encrypt_window:Tk = None
        self.decrypt_window:Tk = None
        self.__seed_entry:Entry= None
        self.__input_text:Text = None
        self.__output:Text = None
        self.key = None
        self.salt = None
        self.round = None
        self.salt_round = None
        self.encrypted_data = None
        self.encrypt_logs:Text = None
        self.decrypt_logs:Text = None
        self.encrypted_file_path:str = None
        self.unlocked_data = None

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
            self.__output.insert(END, self.encrypted_data)
            self.__output.insert(END, self.salt_round)
        self.__input_text.edit_modified(False)
    
    def process_salt_rounds(self) -> None:
        """ process salt_round to collect salt and round """
        self.salt, self.round = self.salt_round

    def process_seed(self):
        self.__output.delete("1.0", "end-1c")
        if not self.__get_seed:
            self.encrypt_logs.config(foreground=RED_1)
            self.encrypt_logs.delete("1.0", "end-1c")
            self.encrypt_logs.insert(END, "empty seed\n")
            return
        self.key, self.salt_round = create_key(password=self.__get_seed)
        self.encrypt_logs.delete("1.0", "end-1c")
        self.encrypt_logs.config(foreground=LIGHT_GREEN_1)
        self.encrypt_logs.insert(END, f"key: {self.key}\n")
        self.encrypt_logs.insert(END, f"salt: {self.salt_round}\n")
        self.process_salt_rounds()
        self.__input_text.config(state=NORMAL, bg=DARK_GREEN_3)
        return
    
    def save_encrypted_data(self):
        if not self.encrypted_data:
            self.encrypt_logs.config(foreground=RED_1)
            self.encrypt_logs.delete("1.0", "end-1c")
            self.encrypt_logs.insert(END, "There is nothing to save yet")
            return
        file_data = {
            "data": self.encrypted_data,
            "salt": self.salt,
            "rounds": self.round
            }
        path = unique_pickle_path(f'./secrets/secret')
        with open(path, "wb") as f:
            pickle.dump(file_data, f)
        self.encrypt_logs.config(foreground=CYAN_1)
        self.encrypt_logs.delete("1.0", "end-1c")
        self.encrypt_logs.insert(END, f"secret saved in {path}")
        return 

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
                        foreground=BLUE_1,
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
        txt_input.config(state=DISABLED)
        logs.insert(END, "submit your password first")
        self.__seed_entry = entry_seed
        self.encrypt_logs = logs
        self.__input_text = txt_input
        self.__output = lbl_output
    def decrypt_file(self):
        if not self.encrypted_file_path:
            self.decrypt_logs.config(fg=RED_1)
            self.decrypt_logs.delete("1.0", "end-1c")
            self.decrypt_logs.insert(END, "choose the file first\n")
            return
        with open(self.encrypted_file_path, "rb") as f:
            try:
                file = pickle.load(f)
            except Exception as e:
                print(e)
                self.decrypt_logs.config(fg=RED_1)
                self.decrypt_logs.delete("1.0", "end-1c")
                self.decrypt_logs.insert(END, "FILE IS BROKEN (bad pickle)\n")
                return
        password = self.__get_seed
        if not password:
            self.decrypt_logs.config(fg=RED_1)
            self.decrypt_logs.delete("1.0", "end-1c")
            self.decrypt_logs.insert(END, "empty password\n")
            return
        salt = file["salt"]
        rounds = file["rounds"]
        data  = file["data"]
        if not salt or not rounds or not data:
            self.decrypt_logs.config(fg=RED_1)
            self.decrypt_logs.delete("1.0", "end-1c")
            self.decrypt_logs.insert(END, "FILE IS BROKEN (salt, token or data is missing)\n")
            return
        key = recreate_key(password=password, salt=salt, round=rounds)
        try:
            self.unlocked_data = decrypt_data(key=key, encrypted_data=data).decode()
            self.decrypt_logs.config(fg=LIGHT_GREEN_1)
            self.decrypt_logs.delete("1.0", "end-1c")
            self.decrypt_logs.insert(END, "File decrypted successfully.\n")
        except InvalidToken:
            self.decrypt_logs.config(fg=RED_1)
            self.decrypt_logs.delete("1.0", "end-1c")
            self.decrypt_logs.insert(END, f"Wrong Password ({password})\n")
            self.decrypt_logs.insert(END, f"key created with given password is \"{key}\" which does NOT match the file \n")


    def get_file(self):
        path = filedialog.askopenfilename(filetypes=[("Locked Files", "*.pickle")])
        if not os.path.exists(path):
            self.decrypt_logs.config(fg=RED_1)
            self.decrypt_logs.delete("1.0", "end-1c")
            self.decrypt_logs.insert(END, "File Not Found. \n")
            return 
        self.encrypted_file_path = path
        self.decrypt_logs.config(fg=LIGHT_GREEN_1)
        self.decrypt_logs.delete("1.0", "end-1c")
        self.decrypt_logs.insert(END, "Success.\n")
        self.decrypt_logs.insert(END, f"File: {path}\n")
    
    def save_to_file(self):
        if not self.unlocked_data:
            self.decrypt_logs.config(fg=RED_1)
            self.decrypt_logs.delete("1.0", "end-1c")
            self.decrypt_logs.insert(END, "Nothing unlocked to save yet.\n")
            self.decrypt_logs.insert(END, "Decrypt your data first.\n")
            return
        path = filedialog.asksaveasfilename(
                    initialfile="unlocked",
                    defaultextension="PENcrypt.txt",
                    title="choose where to save unlocked file"
          )
        with open(path, "w") as f:
            f.write(self.unlocked_data)
        self.decrypt_logs.config(fg=LIGHT_GREEN_1)
        self.decrypt_logs.delete("1.0", "end-1c")
        self.decrypt_logs.insert(END, "Success.\n")
        self.decrypt_logs.insert(END, f"saved in {path}\n")
    def decrypt_win(self):
        root = Tk()
        self.decrypt_window = root
        self.main_window.destroy()
        root.title("PENcrypt")
        root.geometry("330x300+300+100")
        root.config(bg=BLACK)
        
        CoolLabel(master=root, text="Decrypt file").grid(column=0, row=0, columnspan=3, sticky="ew")

        lbl_seed = CoolLabel(root, text="Enter your password", font=("Monospace", 12), fg=LIGHT_GREEN_1)
        ent_seed = CoolEntry(root)
        btn_choose_file = Button(
            root,
            border=0,
            fg=CYAN_1,
            background=GRAY_1,
            text="Choose file",
            activebackground=BLACK,
            activeforeground=RED_1,
            command=self.get_file
        )
        btn_decrypt = Button(
            root,
            border=0,
            fg=CYAN_1,
            background=GRAY_1,
            text="Unlock",
            activebackground=BLACK,
            activeforeground=RED_1,
            command=self.decrypt_file
        )
        btn_save_file = Button(
            root,
            border=0,
            fg=CYAN_1,
            background=GRAY_1,
            text="Save",
            activebackground=BLACK,
            activeforeground=RED_1,
            command=self.save_to_file
        )
        self.decrypt_logs = Text(
                        root,
                        background=BLACK,
                        foreground=BLUE_1,
                        border=0,
                        width=40,
                          )
        lbl_seed.grid(column=0, row=1)
        ent_seed.grid(column=1, row=1, columnspan=2)
        btn_choose_file.grid(column=0, row=3, columnspan=3, pady=20, ipady=10, ipadx=10)
        btn_decrypt.grid(column=0,columnspan=2, row=4, ipady=10, ipadx=10, sticky="ew")
        btn_save_file.grid(column=1,columnspan=2, row=4, ipady=10, ipadx=10, sticky="e")
        self.decrypt_logs.grid(column=0, columnspan=3, row=5)
        self.__seed_entry = ent_seed




    def main(self):
        self.main_window = Tk()
        root = self.main_window
        root.title("PENcrypt")
        root.geometry("600x350+50+50")
        root.configure(bg=BLACK)
        CoolLabel(root, text="PENcrypt", fg=CYAN_1, font=("Arial", 20, "bold")).grid(column=0, row=0)
        MenuButton(root, text="Encrypt", command=self.encrypt_win).grid(column=0, row=1, padx=10, pady=5)
        MenuButton(root, text="Decrypt", command=self.decrypt_win).grid(column=0, row=2, padx=10, pady=5)
        MenuButton(root, text="Source Code", command=lambda: pop_up(root=root)).grid(column=0, row=3, padx=10, pady=5)
        MenuButton(root, text="Exit", command=root.destroy).grid(column=0, row=4, padx=10, pady=5)
        
        root.columnconfigure(0, weight=1)
        root.mainloop()


if __name__ == "__main__":
    main = EncryptUI()
    main.main()

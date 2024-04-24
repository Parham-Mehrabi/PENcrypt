from tkinter import Tk, Button


class EncryptUI():
    """ UI """
    def __init__(self) -> None:
        self.main_window:Tk = None

    @property
    def screen_size(self):
        return self.main_window.winfo_screenwidth(), self.main_window.winfo_screenheight()
    
    def main(self):
        self.main_window = Tk()
        self.main_window.title("PENcrypt")
        self.main_window.geometry("750x750")
        self.main_window.mainloop()


main = EncryptUI()

main.main()
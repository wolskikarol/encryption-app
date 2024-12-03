import tkinter as tk
from tkinter import ttk
from Windows.aes_ctr_window import AesCtrWindow
from Windows.aes_window import AesWindow
from Windows.des_obf_window import DesOfbWindow
from Windows.mono_window import MonoWindow
from Windows.poli_window import PoliWindow
from Windows.trans_window import TransWindow
from Windows.des_window import DesWindow
from Windows.rsa_window import RsaWindow
from Windows.diffie_hellman_window import DiffieHellmanWindow 
from Windows.rsa_stream import RsaStream
from Windows.signature import SignatureWindow

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Programy szyfrujące")
        self.geometry("1450x600")

        self.menu_frame = tk.Frame(self, width=100, bg="lightgray")
        self.menu_frame.pack(side="left", fill="y")

        self.container = tk.Frame(self)
        self.container.pack(side="right", fill="both", expand=True)

        self.frames = {}

        for F in (MonoWindow, PoliWindow, TransWindow, DesWindow, AesWindow, DesOfbWindow, AesCtrWindow, RsaWindow, DiffieHellmanWindow, RsaStream, SignatureWindow):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.create_menu()
        self.show_frame("MonoWindow")

    def create_menu(self):
        button1 = ttk.Button(self.menu_frame, text="Szyfr Monoalfabetyczny",
                             command=lambda: self.show_frame("MonoWindow"))
        button1.pack(fill='x', pady=5)

        button2 = ttk.Button(self.menu_frame, text="Szyfr Polialfabetyczny",
                             command=lambda: self.show_frame("PoliWindow"))
        button2.pack(fill='x', pady=5)

        button3 = ttk.Button(self.menu_frame, text="Szyfr Transpozycyjny",
                             command=lambda: self.show_frame("TransWindow"))
        button3.pack(fill='x', pady=5)
        
        button4 = ttk.Button(self.menu_frame, text="Szyfr DES",
                             command=lambda: self.show_frame("DesWindow"))
        button4.pack(fill='x', pady=5)

        button5 = ttk.Button(self.menu_frame, text="Szyfr AES",
                             command=lambda: self.show_frame("AesWindow"))
        button5.pack(fill='x', pady=5)
        
        button6 = ttk.Button(self.menu_frame, text="Szyfr Output Feedback DES",
                             command=lambda: self.show_frame("DesOfbWindow"))
        button6.pack(fill='x', pady=5)

        button7 = ttk.Button(self.menu_frame, text="Szyfr Counter Mode AES",
                             command=lambda: self.show_frame("AesCtrWindow"))
        button7.pack(fill='x', pady=5)

        button8 = ttk.Button(self.menu_frame, text="Szyfr RSA",
                             command=lambda: self.show_frame("RsaWindow"))
        button8.pack(fill='x', pady=5)

        button9 = ttk.Button(self.menu_frame, text="Szyfr RSA - Stream ",
                             command=lambda: self.show_frame("AudioProcessingApp"))
        button9.pack(fill='x', pady=5)

        button10 = ttk.Button(self.menu_frame, text="Algorytm Diffie-Hellman",
                             command=lambda: self.show_frame("DiffieHellmanWindow"))
        button10.pack(fill='x', pady=5)

        button11 = ttk.Button(self.menu_frame, text="Funkcja podpisu cyfrowego",
                             command=lambda: self.show_frame("DigitalSignatureFrame"))
        button11.pack(fill='x', pady=5)

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


if __name__ == "__main__":
    app = Application()
    app.mainloop()

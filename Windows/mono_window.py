import tkinter as tk
from tkinter import ttk
from Algorithms.mono import mono_encrypt, mono_decrypt

class MonoWindow(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = ttk.Label(self, text="Szyfr monoalfabetyczny")
        label.pack(pady=10, padx=10)

        self.input_text = tk.Text(self, height=5, width=40)
        self.input_text.pack(pady=5)

        self.key = tk.StringVar()
        ttk.Label(self, text="Podaj klucz (pusty = QWERTY):").pack(pady=5)
        self.key_entry = ttk.Entry(self, textvariable=self.key)
        self.key_entry.pack(pady=5)

        encrypt_button = ttk.Button(self, text="Szyfruj", command=self.encrypt_text)
        encrypt_button.pack(pady=5)

        decrypt_button = ttk.Button(self, text="Deszyfruj", command=self.decrypt_text)
        decrypt_button.pack(pady=5)

        ttk.Label(self, text="Zaszyfrowany tekst:").pack(pady=5)
        self.result_text = tk.Text(self, height=5, width=40, wrap=tk.WORD)
        self.result_text.pack(pady=10)

    def encrypt_text(self):
        text = self.input_text.get("1.0", tk.END).strip()
        key = self.key.get()
        encrypted_text = mono_encrypt(text, key)
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, encrypted_text)

    def decrypt_text(self):
        text = self.input_text.get("1.0", tk.END).strip()
        key = self.key.get()
        encrypted_text = mono_decrypt(text, key)
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, encrypted_text)
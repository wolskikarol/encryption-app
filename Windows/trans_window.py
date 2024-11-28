import tkinter as tk
from tkinter import ttk
from Algorithms.trans import trans_encrypt, trans_decrypt

class TransWindow(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = ttk.Label(self, text="Szyfr transpozycyjny")
        label.pack(pady=10, padx=10)

        self.input_text = tk.Text(self, height=5, width=40)
        self.input_text.pack(pady=5)

        self.rows = tk.IntVar()
        self.columns = tk.IntVar()
        self.order = tk.StringVar()

        ttk.Label(self, text="Podaj liczbę wierszy:").pack(pady=5)
        self.rows_entry = ttk.Entry(self, textvariable=self.rows)
        self.rows_entry.pack(pady=5)

        ttk.Label(self, text="Podaj liczbę kolumn:").pack(pady=5)
        self.columns_entry = ttk.Entry(self, textvariable=self.columns)
        self.columns_entry.pack(pady=5)

        ttk.Label(self, text="Podaj kolejność przestawienia kolumn (np. 3,1,2):").pack(pady=5)
        self.order_entry = ttk.Entry(self, textvariable=self.order)
        self.order_entry.pack(pady=5)

        encrypt_button = ttk.Button(self, text="Szyfruj", command=self.encrypt_text)
        encrypt_button.pack(pady=5)

        encrypt_button = ttk.Button(self, text="Deszyfruj", command=self.decrypt_text)
        encrypt_button.pack(pady=5)

        ttk.Label(self, text="Zaszyfrowany tekst:").pack(pady=5)
        self.result_text = tk.Text(self, height=5, width=40, wrap=tk.WORD)
        self.result_text.pack(pady=10)

    def encrypt_text(self):
        # Pobieranie danych z pól
        text = self.input_text.get("1.0", tk.END).strip().upper()
        rows = self.rows.get()
        columns = self.columns.get()
        order = list(map(int, self.order.get().split(',')))

        max_size = rows * columns
        text_length = len(text)

        if text_length > max_size:
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, f"Tekst jest zbyt długi! Max: {max_size} znaków, podano: {text_length}.")
        else:
            
            if text_length < max_size:
                text += 'X' * (max_size - text_length)

            # Wywołanie funkcji szyfrującej
            encrypted_text = trans_encrypt(text, rows, columns, order)

            # Wyświetlanie wyniku
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, encrypted_text)

    def decrypt_text(self):
        # Pobieranie danych z pól
        text = self.input_text.get("1.0", tk.END).strip().replace(" ", "").upper()
        rows = self.rows.get()
        columns = self.columns.get()
        order = list(map(int, self.order.get().split(',')))

        max_size = rows * columns
        text_length = len(text)

        if text_length > max_size:
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, f"Tekst jest zbyt długi! Max: {max_size} znaków, podano: {text_length}.")
        else:
            if text_length < max_size:
                text += 'X' * (max_size - text_length)

            # Wywołanie funkcji szyfrującej
            encrypted_text = trans_decrypt(text, rows, columns, order)

            # Wyświetlanie wyniku
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, encrypted_text)

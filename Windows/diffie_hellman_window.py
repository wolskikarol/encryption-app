import tkinter as tk
from tkinter import messagebox
import random

class DiffieHellmanWindow(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.controller = controller

        self.label_p = tk.Label(self, text="Wprowadź p (moduł):")
        self.label_p.grid(row=0, column=0, padx=10, pady=10)

        self.entry_p = tk.Entry(self, width=50)
        self.entry_p.grid(row=0, column=1, padx=10, pady=10)

        self.label_g = tk.Label(self, text="Wprowadź g (podstawa):")
        self.label_g.grid(row=1, column=0, padx=10, pady=10)

        self.entry_g = tk.Entry(self, width=50)
        self.entry_g.grid(row=1, column=1, padx=10, pady=10)

        self.run_button = tk.Button(self, text="Uruchom algorytm", command=self.on_run)
        self.run_button.grid(row=2, column=1, padx=10, pady=20)

        self.result_label = tk.Label(self, text="Wyniki:")
        self.result_label.grid(row=3, column=0, padx=10, pady=10)

        self.result_text = tk.Text(self, width=60, height=15)
        self.result_text.grid(row=3, column=1, padx=10, pady=10)

    def diffie_hellman(self, p, g):
        a = random.randint(2, p - 2)
        b = random.randint(2, p - 2)

        # Obliczamy klucze publiczne
        A = pow(g, a, p)
        B = pow(g, b, p)

        # Obliczamy wspólny sekret
        shared_secret_A = pow(B, a, p)
        shared_secret_B = pow(A, b, p)

        # Sprawdzamy, czy uzyskany sekret jest zgodny
        assert shared_secret_A == shared_secret_B, "Sekrety nie są zgodne!"

        return a, b, A, B, shared_secret_A

    def on_run(self):
        try:
            p_value = int(self.entry_p.get())
            g_value = int(self.entry_g.get())

            a, b, A, B, shared_secret = self.diffie_hellman(p_value, g_value)

            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Tajna liczba A: {a}\n")
            self.result_text.insert(tk.END, f"Tajna liczba B: {b}\n")
            self.result_text.insert(tk.END, f"Klucz publiczny A: {A}\n")
            self.result_text.insert(tk.END, f"Klucz publiczny B: {B}\n")
            self.result_text.insert(tk.END, f"Wspólny sekret: {shared_secret}\n")
        except ValueError:
            messagebox.showerror("Błąd", "Wprowadź poprawne wartości liczbowe dla p i g.")

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from Algorithms.des_ofb import des_ofb_encrypt, des_ofb_decrypt
from Crypto.Random import get_random_bytes

class DesOfbWindow(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = ttk.Label(self, text="Szyfr Output Feedback DES")
        label.pack(pady=10, padx=10)

        self.input_text = tk.Text(self, height=5, width=40)
        self.input_text.pack(pady=5)

        self.key = tk.StringVar()

        generate_key_button = ttk.Button(self, text="Generuj klucz", command=self.generate_key)
        generate_key_button.pack(pady=5)

        ttk.Label(self, text="Klucz:").pack(pady=5)
        self.key_entry = ttk.Entry(self, textvariable=self.key)
        self.key_entry.pack(pady=5)

        self.iv = tk.StringVar()

        generate_iv_button = ttk.Button(self, text="Generuj IV", command=self.generate_iv)
        generate_iv_button.pack(pady=5)

        ttk.Label(self, text="IV:").pack(pady=5)
        self.iv_entry = ttk.Entry(self, textvariable=self.iv)
        self.iv_entry.pack(pady=5)

        encrypt_button = ttk.Button(self, text="Szyfruj tekst", command=self.encrypt_text)
        encrypt_button.pack(pady=5)

        decrypt_button = ttk.Button(self, text="Deszyfruj tekst", command=self.decrypt_text)
        decrypt_button.pack(pady=5)

        ttk.Label(self, text="Zaszyfrowany tekst:").pack(pady=5)
        self.result_text = tk.Text(self, height=5, width=40, wrap=tk.WORD)
        self.result_text.pack(pady=10)

        encrypt_file_button = ttk.Button(self, text="Szyfruj plik", command=self.encrypt_file)
        encrypt_file_button.pack(pady=5)

        decrypt_file_button = ttk.Button(self, text="Deszyfruj plik", command=self.decrypt_file)
        decrypt_file_button.pack(pady=5)

    def generate_key(self):
        key = get_random_bytes(8)
        self.key.set(key.hex())

    def generate_iv(self):
        iv = get_random_bytes(8)
        self.iv.set(iv.hex())

    def encrypt_text(self):
        text = self.input_text.get("1.0", tk.END).strip()
        key_hex = self.key.get()
        iv_hex = self.iv.get()

        if len(key_hex) != 16:
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, "Klucz musi mieć długość 8 bajtów (16 znaków hex).")
            return
        if len(iv_hex) != 16:
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, "IV musi mieć długość 8 bajtów (16 znaków hex).")
            return

        key = bytes.fromhex(key_hex)
        iv = bytes.fromhex(iv_hex)
        
        encrypted_text = des_ofb_encrypt(text.encode('utf-8'), key, iv)
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, encrypted_text.hex())

    def decrypt_text(self):
        text = self.input_text.get("1.0", tk.END).strip()
        key_hex = self.key.get()
        iv_hex = self.iv.get()

        if len(key_hex) != 16:
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, "Klucz musi mieć długość 8 bajtów (16 znaków hex).")
            return
        if len(iv_hex) != 16:
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, "IV musi mieć długość 8 bajtów (16 znaków hex).")
            return
        key = bytes.fromhex(key_hex)
        iv = bytes.fromhex(iv_hex)

        try:
            encrypted_text = bytes.fromhex(text)
            decrypted_text = des_ofb_decrypt(encrypted_text, key, iv)
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, decrypted_text.decode('utf-8'))
        except ValueError:
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, "Nieprawidłowe dane do deszyfrowania.")

    def encrypt_file(self):
        key_hex = self.key.get()
        iv_hex = self.iv.get()

        if len(key_hex) != 16:
            messagebox.showerror("Błąd", "Klucz musi mieć długość 8 bajtów (16 znaków hex).")
            return
        if len(iv_hex) != 16:
            messagebox.showerror("Błąd", "IV musi mieć długość 8 bajtów (16 znaków hex).")
            return

        key = bytes.fromhex(key_hex)
        iv = bytes.fromhex(iv_hex)

        filepath = filedialog.askopenfilename(title="Wybierz plik do zaszyfrowania")

        if filepath:
            try:
                with open(filepath, 'rb') as file:
                    data = file.read()

                encrypted_data = des_ofb_encrypt(data, key, iv)

                save_path = filedialog.asksaveasfilename(title="Zapisz zaszyfrowany plik", defaultextension=".des", filetypes=[("Pliki DES", "*.des")])

                if save_path:
                    with open(save_path, 'wb') as file:
                        file.write(encrypted_data)
                    messagebox.showinfo("Sukces", "Plik został zaszyfrowany i zapisany.")
            except Exception as e:
                messagebox.showerror("Błąd", f"Wystąpił błąd podczas szyfrowania pliku: {e}")

    def decrypt_file(self):
        key_hex = self.key.get()
        iv_hex = self.iv.get()

        if len(key_hex) != 16:
            messagebox.showerror("Błąd", "Klucz musi mieć długość 8 bajtów (16 znaków hex).")
            return
        if len(iv_hex) != 16:
            messagebox.showerror("Błąd", "IV musi mieć długość 8 bajtów (16 znaków hex).")
            return

        key = bytes.fromhex(key_hex)
        iv = bytes.fromhex(iv_hex)

        filepath = filedialog.askopenfilename(title="Wybierz plik do deszyfrowania", filetypes=[("Pliki DES", "*.des")])

        if filepath:
            try:
                with open(filepath, 'rb') as file:
                    encrypted_data = file.read()

                decrypted_data = des_ofb_decrypt(encrypted_data, key, iv)

                save_path = filedialog.asksaveasfilename(title="Zapisz odszyfrowany plik")

                if save_path:
                    with open(save_path, 'wb') as file:
                        file.write(decrypted_data)
                    messagebox.showinfo("Sukces", "Plik został odszyfrowany i zapisany.")
            except ValueError as e:
                if "Padding is incorrect" in str(e):
                    messagebox.showerror("Błąd", "Nieprawidłowy klucz lub dane są uszkodzone.")
                else:
                    messagebox.showerror("Błąd", f"Wystąpił błąd podczas deszyfrowania pliku: {e}")
            except Exception as e:
                messagebox.showerror("Błąd", f"Wystąpił błąd podczas deszyfrowania pliku: {e}")


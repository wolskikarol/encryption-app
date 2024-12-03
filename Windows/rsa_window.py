import tkinter as tk
from tkinter import ttk, filedialog
from Algorithms.rsa import generate_rsa_keys, encrypt_data_rsa, decrypt_data_rsa
import os
from tkinter import messagebox
import base64
from Crypto.Cipher import PKCS1_OAEP




class RsaWindow(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.public_key = None
        self.private_key = None

        label = ttk.Label(self, text="Szyfr RSA", font=("Arial", 14))
        label.pack(pady=10)

        key_group = ttk.LabelFrame(self, text="Generowanie kluczy", padding=(10, 10))
        key_group.pack(fill="x", padx=10, pady=5)

        ttk.Button(key_group, text="Generuj klucze", command=self.generate_keys).pack(side="left", padx=5)

        ttk.Label(key_group, text="Klucz publiczny:").pack(side="left", padx=5)
        self.public_key_text = tk.Text(key_group, height=5, width=50, wrap="word")
        self.public_key_text.pack(side="left", padx=5)

        ttk.Label(key_group, text="Klucz prywatny:").pack(side="left", padx=5)
        self.private_key_text = tk.Text(key_group, height=5, width=50, wrap="word")
        self.private_key_text.pack(side="left", padx=5)

        encrypt_group = ttk.LabelFrame(self, text="Szyfrowanie tekstu", padding=(10, 10))
        encrypt_group.pack(fill="x", padx=10, pady=5)

        ttk.Label(encrypt_group, text="Wprowadź tekst do zaszyfrowania:").pack(side="left", padx=5)
        self.input_text = tk.Text(encrypt_group, height=5, width=50, wrap="word")
        self.input_text.pack(side="left", padx=5)

        ttk.Button(encrypt_group, text="Szyfruj tekst", command=self.encrypt_text).pack(side="left", padx=5)

        ttk.Label(encrypt_group, text="Zaszyfrowany tekst:").pack(side="left", padx=5)
        self.encrypted_text = tk.Text(encrypt_group, height=5, width=50, wrap="word")
        self.encrypted_text.pack(side="left", padx=5)

        decrypt_group = ttk.LabelFrame(self, text="Deszyfrowanie tekstu", padding=(10, 10))
        decrypt_group.pack(fill="x", padx=10, pady=5)

        ttk.Label(decrypt_group, text="Wprowadź zaszyfrowany tekst:").pack(side="left", padx=5)
        self.encrypted_input = tk.Text(decrypt_group, height=5, width=50, wrap="word")
        self.encrypted_input.pack(side="left", padx=5)

        ttk.Button(decrypt_group, text="Deszyfruj tekst", command=self.decrypt_text).pack(side="left", padx=5)

        ttk.Label(decrypt_group, text="Odszyfrowany tekst:").pack(side="left", padx=5)
        self.decrypted_text = tk.Text(decrypt_group, height=5, width=50, wrap="word")
        self.decrypted_text.pack(side="left", padx=5)

        file_group = ttk.LabelFrame(self, text="Szyfrowanie i deszyfrowanie plików", padding=(10, 10))
        file_group.pack(fill="x", padx=10, pady=5)

        ttk.Button(file_group, text="Szyfruj plik", command=self.encrypt_file).pack(side="left", padx=5)
        ttk.Button(file_group, text="Deszyfruj plik", command=self.decrypt_file).pack(side="left", padx=5)

    def generate_keys(self):
        try:
            self.public_key, self.private_key = generate_rsa_keys()
            self.public_key_text.delete(1.0, tk.END)
            self.public_key_text.insert(tk.END, self.public_key.export_key().decode('utf-8'))
            self.private_key_text.delete(1.0, tk.END)
            self.private_key_text.insert(tk.END, self.private_key.export_key().decode('utf-8'))
            messagebox.showinfo("Sukces", "Klucze RSA zostały wygenerowane!")
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się wygenerować kluczy: {e}")


    def encrypt_text(self):
        plaintext = self.input_text.get(1.0, tk.END).strip()
        if not self.public_key:
            messagebox.showwarning("Brak klucza", "Brak klucza publicznego do szyfrowania!")
            return
        if not plaintext:
            messagebox.showwarning("Brak tekstu", "Proszę wprowadzić tekst do zaszyfrowania.")
            return
        try:
            data = plaintext.encode('utf-8')

            max_chunk_size = self.public_key.size_in_bytes() - 42

            chunks = [data[i:i + max_chunk_size] for i in range(0, len(data), max_chunk_size)]

            cipher_rsa = PKCS1_OAEP.new(self.public_key)
            encrypted_chunks = [cipher_rsa.encrypt(chunk) for chunk in chunks]

            encrypted_base64 = base64.b64encode(b"".join(encrypted_chunks)).decode('utf-8')

            self.encrypted_text.delete(1.0, tk.END)
            self.encrypted_text.insert(tk.END, encrypted_base64)
            messagebox.showinfo("Sukces", "Tekst został zaszyfrowany!")
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się zaszyfrować tekstu: {e}")



    def decrypt_text(self):
        encrypted_data = self.encrypted_input.get(1.0, tk.END).strip()
        if not self.private_key:
            messagebox.showwarning("Brak klucza", "Brak klucza prywatnego do deszyfrowania!")
            return
        if not encrypted_data:
            messagebox.showwarning("Brak tekstu", "Proszę wprowadzić zaszyfrowany tekst.")
            return
        try:
            encrypted_chunks = base64.b64decode(encrypted_data)

            max_chunk_size = self.private_key.size_in_bytes()

            chunks = [encrypted_chunks[i:i + max_chunk_size] for i in range(0, len(encrypted_chunks), max_chunk_size)]

            cipher_rsa = PKCS1_OAEP.new(self.private_key)
            decrypted_data = b"".join([cipher_rsa.decrypt(chunk) for chunk in chunks])

            decrypted_text = decrypted_data.decode('utf-8')

            self.decrypted_text.delete(1.0, tk.END)
            self.decrypted_text.insert(tk.END, decrypted_text)
            messagebox.showinfo("Sukces", "Tekst został odszyfrowany!")
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się odszyfrować tekstu: {e}")


    def encrypt_file(self):
        file_path = filedialog.askopenfilename()
        if not file_path:
            messagebox.showwarning("Brak pliku", "Nie wybrano pliku do zaszyfrowania.")
            return
        if not self.public_key:
            messagebox.showwarning("Brak klucza", "Brak klucza publicznego do szyfrowania pliku!")
            return
        try:
            output_file = filedialog.asksaveasfilename(defaultextension=".enc")
            if not output_file:
                messagebox.showwarning("Brak miejsca docelowego", "Nie wybrano miejsca docelowego dla zaszyfrowanego pliku.")
                return
            encrypt_data_rsa(file_path, self.public_key, is_file=True, output_file=output_file)
            messagebox.showinfo("Sukces", "Plik został zaszyfrowany!")
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się zaszyfrować pliku: {e}")

    def decrypt_file(self):
        file_path = filedialog.askopenfilename()
        if not file_path:
            messagebox.showwarning("Brak pliku", "Nie wybrano pliku do deszyfrowania.")
            return
        if not self.private_key:
            messagebox.showwarning("Brak klucza", "Brak klucza prywatnego do deszyfrowania pliku!")
            return
        try:
            output_file = filedialog.asksaveasfilename()
            if not output_file:
                messagebox.showwarning("Brak miejsca docelowego", "Nie wybrano miejsca docelowego dla odszyfrowanego pliku.")
                return
            with open(file_path, 'rb') as f:
                encrypted_chunks = [f.read(256) for _ in range(int(os.path.getsize(file_path) / 256))]
            decrypt_data_rsa(encrypted_chunks, self.private_key, is_file=True, output_file=output_file)
            messagebox.showinfo("Sukces", "Plik został odszyfrowany!")
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się odszyfrować pliku: {e}")


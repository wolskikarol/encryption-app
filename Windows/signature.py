import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization


class SignatureWindow(ttk.Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.private_key = None
        self.public_key = None

        self.create_widgets()
        self.layout_widgets()

    def create_widgets(self):
        self.message_label = ttk.Label(self, text="Wiadomość:")
        self.message_entry = ttk.Entry(self, width=50)

        self.sign_button = ttk.Button(self, text="Podpisz", command=self.sign_message)
        self.verify_button = ttk.Button(self, text="Zweryfikuj podpis", command=self.verify_signature)
        
        self.load_key_button = ttk.Button(self, text="Wczytaj klucz prywatny", command=self.load_private_key)
        self.load_pubkey_button = ttk.Button(self, text="Wczytaj klucz publiczny", command=self.load_public_key)
        self.generate_keys_button = ttk.Button(self, text="Wygeneruj klucze", command=self.generate_keys)
        
        self.sign_file_button = ttk.Button(self, text="Podpisz plik", command=self.sign_file)
        self.verify_file_button = ttk.Button(self, text="Zweryfikuj podpis pliku", command=self.verify_file)

    def layout_widgets(self):
        message_frame = ttk.LabelFrame(self, text="Wiadomość")
        keys_frame = ttk.LabelFrame(self, text="Zarządzanie kluczami")
        actions_frame = ttk.LabelFrame(self, text="Operacje")
        files_frame = ttk.LabelFrame(self, text="Pliki")

        message_frame.pack(fill="x", padx=10, pady=5)
        keys_frame.pack(fill="x", padx=10, pady=5)
        actions_frame.pack(fill="x", padx=10, pady=5)
        files_frame.pack(fill="x", padx=10, pady=5)

        self.message_label.pack(anchor="w", padx=5, pady=5)
        self.message_entry.pack(fill="x", padx=5, pady=5)

        self.generate_keys_button.pack(anchor="w", padx=5, pady=5)
        self.load_key_button.pack(anchor="w", padx=5, pady=5)
        self.load_pubkey_button.pack(anchor="w", padx=5, pady=5)

        self.sign_button.pack(anchor="w", padx=5, pady=5)
        self.verify_button.pack(anchor="w", padx=5, pady=5)

        self.sign_file_button.pack(anchor="w", padx=5, pady=5)
        self.verify_file_button.pack(anchor="w", padx=5, pady=5)

    def sign_message(self):
        if not self.private_key:
            messagebox.showerror("Błąd", "Najpierw wczytaj klucz prywatny.")
            return

        message = self.message_entry.get().encode()

        signature_path = filedialog.asksaveasfilename(defaultextension=".sig", filetypes=[("Pliki podpisu", "*.sig")], title="Zapisz podpis")
        
        if not signature_path:
            return

        try:
            signature = self.private_key.sign(
                message,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )

            with open(signature_path, "wb") as sig_file:
                sig_file.write(signature)

            messagebox.showinfo("Sukces", f"Podpis zapisano w pliku: {signature_path}")
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się podpisać wiadomości: {e}")


    def verify_signature(self):
        if not self.public_key:
            messagebox.showerror("Błąd", "Najpierw wczytaj klucz publiczny.")
            return

        message = self.message_entry.get().encode()

        signature_path = filedialog.askopenfilename(filetypes=[("Pliki podpisu", "*.sig")], title="Wybierz plik podpisu")
        
        if not signature_path:
            return

        try:
            with open(signature_path, "rb") as sig_file:
                signature = sig_file.read()

            self.public_key.verify(
                signature,
                message,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )

            messagebox.showinfo("Sukces", "Podpis jest prawidłowy.")
        except Exception as e:
            messagebox.showerror("Błąd", f"Weryfikacja nie powiodła się: {e}")


    def load_private_key(self):
        filepath = filedialog.askopenfilename(filetypes=[("Klucze prywatne", "*.pem")])
        if filepath:
            try:
                with open(filepath, "rb") as key_file:
                    self.private_key = serialization.load_pem_private_key(
                        key_file.read(),
                        password=None
                    )
                messagebox.showinfo("Sukces", "Wczytano klucz prywatny.")
            except Exception as e:
                messagebox.showerror("Błąd", f"Nie udało się wczytać klucza prywatnego: {e}")

    def load_public_key(self):
        filepath = filedialog.askopenfilename(filetypes=[("Klucze publiczne", "*.pem")])
        if filepath:
            try:
                with open(filepath, "rb") as key_file:
                    self.public_key = serialization.load_pem_public_key(key_file.read())
                messagebox.showinfo("Sukces", "Wczytano klucz publiczny.")
            except Exception as e:
                messagebox.showerror("Błąd", f"Nie udało się wczytać klucza publicznego: {e}")

    def generate_keys(self):
        private_key_path = filedialog.asksaveasfilename(defaultextension=".pem", filetypes=[("Pliki PEM", "*.pem")], title="Zapisz klucz prywatny")
        if not private_key_path:
            return

        public_key_path = private_key_path.replace("private_key", "public_key")

        if not public_key_path.endswith("_public.pem"):
            public_key_path = public_key_path.replace(".pem", "_public.pem")

        try:
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
            )
            public_key = private_key.public_key()

            with open(private_key_path, "wb") as priv_file:
                priv_file.write(
                    private_key.private_bytes(
                        encoding=serialization.Encoding.PEM,
                        format=serialization.PrivateFormat.PKCS8,
                        encryption_algorithm=serialization.NoEncryption()
                    )
                )

            with open(public_key_path, "wb") as pub_file:
                pub_file.write(
                    public_key.public_bytes(
                        encoding=serialization.Encoding.PEM,
                        format=serialization.PublicFormat.SubjectPublicKeyInfo
                    )
                )
            
            messagebox.showinfo("Sukces", f"Wygenerowano klucze:\n{private_key_path}\n{public_key_path}")
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się wygenerować kluczy: {e}")

    def sign_file(self):
        if not self.private_key:
            messagebox.showerror("Błąd", "Najpierw wczytaj klucz prywatny.")
            return

        file_path = filedialog.askopenfilename(title="Wybierz plik do podpisania")
        if not file_path:
            return

        signature_path = filedialog.asksaveasfilename(defaultextension=".sig", filetypes=[("Pliki podpisu", "*.sig")], title="Zapisz podpis")
        if not signature_path:
            return

        try:
            with open(file_path, "rb") as file:
                file_data = file.read()

            signature = self.private_key.sign(
                file_data,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )

            with open(signature_path, "wb") as sig_file:
                sig_file.write(signature)

            messagebox.showinfo("Sukces", f"Podpis zapisano w pliku: {signature_path}")
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się podpisać pliku: {e}")


    def verify_file(self):
        if not self.public_key:
            messagebox.showerror("Błąd", "Najpierw wczytaj klucz publiczny.")
            return

        file_path = filedialog.askopenfilename(title="Wybierz plik do weryfikacji")
        if not file_path:
            return

        signature_path = filedialog.askopenfilename(filetypes=[("Pliki podpisu", "*.sig")], title="Wybierz plik podpisu")
        if not signature_path:
            return

        try:
            with open(file_path, "rb") as file:
                file_data = file.read()

            with open(signature_path, "rb") as sig_file:
                signature = sig_file.read()

            self.public_key.verify(
                signature,
                file_data,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )

            messagebox.showinfo("Sukces", "Podpis jest prawidłowy.")
        except Exception as e:
            messagebox.showerror("Błąd", f"Weryfikacja nie powiodła się: {e}")

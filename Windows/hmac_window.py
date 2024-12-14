import hmac
import hashlib
import tkinter as tk
from tkinter import filedialog, messagebox

class HmacWindow(tk.Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.generated_hmac = ""
        self.create_widgets()

    def create_widgets(self):
        self.secret_label = tk.Label(self, text="Klucz tajny:")
        self.secret_label.grid(row=0, column=0, sticky="e", padx=5, pady=5)
        
        self.secret_entry = tk.Entry(self, width=40)
        self.secret_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5)

        self.message_label = tk.Label(self, text="Wiadomość:")
        self.message_label.grid(row=1, column=0, sticky="e", padx=5, pady=5)

        self.message_entry = tk.Entry(self, width=40)
        self.message_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5)

        self.generate_message_button = tk.Button(self, text="Generuj HMAC Wiadomości", command=self.generate_message_hmac)
        self.generate_message_button.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="ew")

        self.file_label = tk.Label(self, text="Plik:")
        self.file_label.grid(row=3, column=0, sticky="e", padx=5, pady=5)

        self.file_entry = tk.Entry(self, width=40)
        self.file_entry.grid(row=3, column=1, padx=5, pady=5)

        self.browse_button = tk.Button(self, text="Przeglądaj", command=self.browse_file)
        self.browse_button.grid(row=3, column=2, padx=5, pady=5)

        self.generate_file_button = tk.Button(self, text="Generuj HMAC Pliku", command=self.generate_file_hmac)
        self.generate_file_button.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky="ew")

        self.hmac_label = tk.Label(self, text="Wygenerowany HMAC:")
        self.hmac_label.grid(row=5, column=0, sticky="e", padx=5, pady=5)

        self.hmac_text = tk.Entry(self, width=40)
        self.hmac_text.grid(row=5, column=1, columnspan=2, padx=5, pady=5)

        self.verify_button = tk.Button(self, text="Weryfikuj HMAC", command=self.verify_hmac)
        self.verify_button.grid(row=6, column=0, columnspan=3, padx=5, pady=5, sticky="ew")

    def browse_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, file_path)

    def generate_message_hmac(self):
        secret_key = self.secret_entry.get().encode()
        message = self.message_entry.get().encode()

        if message:
            self.generated_hmac = generate_hmac(secret_key, message)
            self.hmac_text.delete(0, tk.END)
            self.hmac_text.insert(0, self.generated_hmac)
            messagebox.showinfo("HMAC Wygenerowany", f"HMAC Wiadomości: {self.generated_hmac}")
        else:
            messagebox.showerror("Błąd", "Proszę podać wiadomość.")

    def generate_file_hmac(self):
        secret_key = self.secret_entry.get().encode()
        file_path = self.file_entry.get()

        if file_path:
            try:
                self.generated_hmac = generate_file_hmac(secret_key, file_path)
                self.hmac_text.delete(0, tk.END)
                self.hmac_text.insert(0, self.generated_hmac)
                messagebox.showinfo("HMAC Wygenerowany", f"HMAC Pliku: {self.generated_hmac}")
            except Exception as e:
                messagebox.showerror("Błąd", f"Wystąpił błąd: {e}")
        else:
            messagebox.showerror("Błąd", "Proszę wybrać plik.")

    def verify_hmac(self):
        secret_key = self.secret_entry.get().encode()
        received_hmac = self.hmac_text.get().strip()
        message = self.message_entry.get().encode()
        file_path = self.file_entry.get()

        if received_hmac:
            try:
                if message:
                    is_valid = verify_hmac(secret_key, message, received_hmac)
                    msg_type = "Wiadomości"
                elif file_path:
                    is_valid = verify_file_hmac(secret_key, file_path, received_hmac)
                    msg_type = "Pliku"
                else:
                    raise ValueError("Brak danych do weryfikacji.")
                messagebox.showinfo("Weryfikacja", f"HMAC {msg_type} jest {'poprawny' if is_valid else 'niepoprawny'}.")
            except Exception as e:
                messagebox.showerror("Błąd", f"Wystąpił błąd: {e}")
        else:
            messagebox.showerror("Błąd", "Proszę podać HMAC.")

def generate_hmac(secret_key: bytes, message: bytes) -> str:
    hmac_instance = hmac.new(secret_key, message, hashlib.sha256)
    return hmac_instance.hexdigest()


def verify_hmac(secret_key: bytes, message: bytes, received_hmac: str) -> bool:
    expected_hmac = generate_hmac(secret_key, message)
    return hmac.compare_digest(expected_hmac, received_hmac)


def generate_file_hmac(secret_key: bytes, file_path: str) -> str:
    hmac_instance = hmac.new(secret_key, b"", hashlib.sha256)
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hmac_instance.update(chunk)
    return hmac_instance.hexdigest()


def verify_file_hmac(secret_key: bytes, file_path: str, received_hmac: str) -> bool:
    expected_hmac = generate_file_hmac(secret_key, file_path)
    return hmac.compare_digest(expected_hmac, received_hmac)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Generator i Weryfikator HMAC")
    app = HmacWindow(master=root)
    app.mainloop()

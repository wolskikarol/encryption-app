import os
import tkinter as tk
from tkinter import filedialog, messagebox

def calculate_parity(bits, positions):
    parity = 0
    for pos in positions:
        parity ^= bits[pos - 1]
    return parity


def hamming_encode(data):
    data_bits = list(map(int, data))
    n = len(data_bits)

    m = 0
    while (2**m) < (n + m + 1):
        m += 1

    hamming_code = [0] * (n + m)

    j = 0
    for i in range(1, len(hamming_code) + 1):
        if (i & (i - 1)) == 0:
            continue
        hamming_code[i - 1] = data_bits[j]
        j += 1

    for i in range(m):
        parity_pos = 2**i
        positions = [x for x in range(1, len(hamming_code) + 1) if x & parity_pos]
        hamming_code[parity_pos - 1] = calculate_parity(hamming_code, positions)

    return ''.join(map(str, hamming_code))


def hamming_decode(encoded_data):
    try:
        bits = list(map(int, filter(str.isdigit, encoded_data)))
    except ValueError:
        messagebox.showerror("Błąd", "Nieprawidłowy format danych. Dekodowanie nie powiodło się.")
        return ""

    n = len(bits)
    m = 0
    while (2**m) < n:
        m += 1

    error_position = 0

    for i in range(m):
        parity_pos = 2**i
        positions = [x for x in range(1, n + 1) if x & parity_pos]
        expected_parity = calculate_parity(bits, positions)
        if expected_parity != 0:
            error_position += parity_pos

    if error_position != 0:
        messagebox.showwarning("Błąd wykryty", f"Wykryto błąd bitu na pozycji {error_position}. Korekta...")
        bits[error_position - 1] ^= 1

    original_data = []
    for i in range(1, n + 1):
        if (i & (i - 1)) != 0:
            original_data.append(str(bits[i - 1]))

    return ''.join(original_data)


def save_to_file(data, filename):
    with open(filename, 'wb') as file:
        file.write(data)
    messagebox.showinfo("Zapisano plik", f"Dane zapisano do {filename}")


def process_file(file_path, mode):
    if not os.path.isfile(file_path):
        messagebox.showerror("Błąd", "Nie znaleziono pliku.")
        return

    with open(file_path, 'rb') as file:
        data = file.read()

    if mode == "encode":
        binary_data = ''.join(f'{byte:08b}' for byte in data)
        encoded = hamming_encode(binary_data).encode('utf-8')
        save_to_file(encoded, "encoded_data.bin")
    elif mode == "decode":
        decoded_binary = hamming_decode(data.decode('utf-8', errors='ignore'))
        if decoded_binary:
            decoded_length = len(decoded_binary)
            if decoded_length % 8 != 0:
                messagebox.showerror("Błąd", "Dekodowane dane nie są wielokrotnością 8 bitów.")
                return
            decoded_bytes = int(decoded_binary, 2).to_bytes(decoded_length // 8, byteorder='big')
            output_file = filedialog.asksaveasfilename(defaultextension=".bin", filetypes=[("Wszystkie pliki", "*.*")])
            if output_file:
                save_to_file(decoded_bytes, output_file)
    else:
        messagebox.showerror("Błąd", "Nieprawidłowy tryb.")


class HammingWindow(tk.Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()
        self.file_path = None

    def create_widgets(self):
        self.mode_label = tk.Label(self, text="Wybierz tryb:")
        self.mode_label.pack()
        self.mode_var = tk.StringVar(value="encode")
        self.encode_button = tk.Radiobutton(self, text="Kodowanie", variable=self.mode_var, value="encode")
        self.decode_button = tk.Radiobutton(self, text="Dekodowanie", variable=self.mode_var, value="decode")
        self.encode_button.pack()
        self.decode_button.pack()

        self.file_button = tk.Button(self, text="Wybierz plik", command=self.select_file)
        self.file_button.pack()

        self.selected_file_label = tk.Label(self, text="Nie wybrano pliku.", fg="blue")
        self.selected_file_label.pack()

        self.process_button = tk.Button(self, text="Przetwórz", command=self.process_data)
        self.process_button.pack()

    def select_file(self):
        self.file_path = filedialog.askopenfilename()
        if self.file_path:
            self.selected_file_label.config(text=f"Wybrano plik: {os.path.basename(self.file_path)}")
        else:
            self.selected_file_label.config(text="Nie wybrano pliku.")

    def process_data(self):
        mode = self.mode_var.get()
        if self.file_path:
            process_file(self.file_path, mode)
        else:
            messagebox.showerror("Błąd", "Brak pliku do przetworzenia.")


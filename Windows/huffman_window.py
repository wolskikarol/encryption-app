import heapq
from collections import defaultdict
import os
import tkinter as tk
from tkinter import filedialog, messagebox

def read_file(file_path):
    with open(file_path, "rb") as file:
        return list(file.read())

def write_file(file_path, data):
    with open(file_path, "wb") as file:
        file.write(bytes(data))

class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def calculate_frequencies(data):
    frequencies = defaultdict(int)
    for item in data:
        frequencies[item] += 1
    return frequencies

def build_huffman_tree(frequencies):
    heap = [Node(char, freq) for char, freq in frequencies.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)

    return heap[0]

def build_codes(node, current_code="", codes={}):
    if not node:
        return

    if node.char is not None:
        codes[node.char] = current_code

    build_codes(node.left, current_code + "0", codes)
    build_codes(node.right, current_code + "1", codes)

    return codes

def huffman_encode(data):
    if not data:
        return "", {}

    frequencies = calculate_frequencies(data)
    root = build_huffman_tree(frequencies)
    codes = build_codes(root)

    encoded_data = ''.join(codes[item] for item in data)
    return encoded_data, codes

def huffman_decode(encoded_data, codes):
    reverse_codes = {value: key for key, value in codes.items()}
    decoded_data = []
    current_code = ""

    for bit in encoded_data:
        current_code += bit
        if current_code in reverse_codes:
            decoded_data.append(reverse_codes[current_code])
            current_code = ""

    return decoded_data

class HuffmanWindow(tk.Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        self.encode_file_button = tk.Button(self, text="Zakoduj plik", command=self.encode_file)
        self.encode_file_button.pack(pady=5)

        self.decode_file_button = tk.Button(self, text="Odkoduj plik", command=self.decode_file)
        self.decode_file_button.pack(pady=5)

        self.text_area = tk.Text(self, width=60, height=15)
        self.text_area.pack(pady=10)

        self.encode_text_button = tk.Button(self, text="Zakoduj tekst", command=self.encode_text)
        self.encode_text_button.pack(pady=5)

    def encode_file(self):
        file_path = filedialog.askopenfilename(title="Wybierz plik do zakodowania")
        if not file_path:
            return

        file_data = read_file(file_path)
        encoded_data, codes = huffman_encode(file_data)

        encoded_file = file_path + ".huffman"
        codes_file = file_path + ".codes"

        write_file(encoded_file, map(int, encoded_data))
        with open(codes_file, "w") as f:
            f.write(str(codes))

        messagebox.showinfo("Sukces", f"Pliki zapisane: {encoded_file}, {codes_file}")

    def decode_file(self):
        encoded_file = filedialog.askopenfilename(title="Wybierz plik zakodowany")
        codes_file = filedialog.askopenfilename(title="Wybierz plik z kodami")

        if not encoded_file or not codes_file:
            return

        with open(codes_file, "r") as f:
            codes = eval(f.read())

        encoded_data = read_file(encoded_file)
        decoded_data = huffman_decode(''.join(map(str, encoded_data)), codes)

        output_file = encoded_file + ".decoded"
        write_file(output_file, decoded_data)
        messagebox.showinfo("Sukces", f"Dane zostały zapisane do pliku: {output_file}")

    def encode_text(self):
        text = self.text_area.get("1.0", "end-1c")
        if not text:
            messagebox.showwarning("Błąd", "Pole tekstowe jest puste!")
            return

        encoded_data, codes = huffman_encode(list(text.encode('utf-8')))
        output_file = filedialog.asksaveasfilename(defaultextension=".huffman", title="Zapisz zakodowany tekst")
        codes_file = output_file + ".codes"

        write_file(output_file, map(int, encoded_data))
        with open(codes_file, "w") as f:
            f.write(str(codes))

        messagebox.showinfo("Sukces", f"Tekst zakodowany zapisany w: {output_file}, {codes_file}")

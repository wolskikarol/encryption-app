import tkinter as tk
from tkinter import ttk
import sounddevice as sd
import numpy as np
import queue
import threading
import time
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from scipy.io.wavfile import write

SAMPLE_RATE = 44100
CHANNELS = 1
DURATION = 1
THRESHOLD = 500

recorded_audio = queue.Queue()
encrypted_audio = queue.Queue()
decrypted_audio = queue.Queue()

key = RSA.generate(2048)
public_key = key.publickey()
cipher_encrypt = PKCS1_OAEP.new(public_key)
cipher_decrypt = PKCS1_OAEP.new(key)

class RsaStreamWindow(tk.Frame):
    def __init__(self, parent=None, controller=None):
        super().__init__(parent)
        self.master = parent
        self.controller = controller
        self.create_widgets()

        self.running = False
        self.recording_thread = None
        self.encrypt_thread = None
        self.decrypt_thread = None
        self.play_thread = None

    def create_widgets(self):
        self.start_button = tk.Button(self, text="Start", command=self.start_processing)
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(self, text="Stop", command=self.stop_processing)
        self.stop_button.pack(pady=5)

        self.sound_indicator = tk.Label(self, text="Dźwięk: Nie wykryto", bg="red", fg="white", width=20)
        self.sound_indicator.pack(pady=5)

        self.encrypt_progress = ttk.Progressbar(self, orient="horizontal", mode="indeterminate", length=200)
        self.encrypt_progress.pack(pady=5)

        self.decrypt_progress = ttk.Progressbar(self, orient="horizontal", mode="indeterminate", length=200)
        self.decrypt_progress.pack(pady=5)
        
        self.convert_button = tk.Button(self, text="Konwertuj na WAV", command=self.convert_pcm_to_wav)
        self.convert_button.pack(pady=5)


    def start_processing(self):
        if not self.running:
            self.running = True
            self.recording_thread = threading.Thread(target=self.record_audio, daemon=True)
            self.encrypt_thread = threading.Thread(target=self.encrypt_audio, daemon=True)
            self.decrypt_thread = threading.Thread(target=self.decrypt_audio, daemon=True)
            self.play_thread = threading.Thread(target=self.play_audio, daemon=True)

            self.recording_thread.start()
            self.encrypt_thread.start()
            self.decrypt_thread.start()
            self.play_thread.start()

    def stop_processing(self):
        self.running = False

    def record_audio(self):
        with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, dtype='int16') as stream:
            while self.running:
                audio_chunk = stream.read(int(SAMPLE_RATE * DURATION))[0].flatten()
                amplitude = np.max(np.abs(audio_chunk))
                if amplitude > THRESHOLD:
                    self.sound_indicator.config(text="Dźwięk: Wykryto", bg="green")
                    recorded_audio.put(audio_chunk)
                else:
                    self.sound_indicator.config(text="Dźwięk: Nie wykryto", bg="red")
                time.sleep(0.1)

    def encrypt_audio(self):
        while self.running:
            if not recorded_audio.empty():
                self.encrypt_progress.start()
                chunk = recorded_audio.get()
                encrypted_chunks = []
                chunk_bytes = chunk.tobytes()
                for i in range(0, len(chunk_bytes), 200):
                    block = chunk_bytes[i:i + 200]
                    encrypted_chunks.append(cipher_encrypt.encrypt(block))
                encrypted_audio.put(encrypted_chunks)
                self.save_encrypted_audio(encrypted_chunks)
                self.encrypt_progress.stop()

    def decrypt_audio(self):
        while self.running:
            if not encrypted_audio.empty():
                self.decrypt_progress.start()
                encrypted_chunks = encrypted_audio.get()
                decrypted_data = bytearray()
                for block in encrypted_chunks:
                    decrypted_data.extend(cipher_decrypt.decrypt(block))
                audio_chunk = np.frombuffer(decrypted_data, dtype='int16')
                decrypted_audio.put(audio_chunk)
                self.save_decrypted_audio(audio_chunk)
                self.decrypt_progress.stop()

    def save_encrypted_audio(self, encrypted_chunks):
        encrypted_data = b''.join(encrypted_chunks)
        with open("encrypted_audio.bin", "ab") as f:
            f.write(encrypted_data)
        print("Zapisano zaszyfrowane audio do pliku 'encrypted_audio.bin'.")

    def save_decrypted_audio(self, audio_chunk):
        with open("decrypted_audio.pcm", "ab") as f:
            f.write(audio_chunk.tobytes())
        print("Dodano odszyfrowane audio do pliku 'decrypted_audio.pcm'.")

    def convert_pcm_to_wav(self):
        try:
            with open("decrypted_audio.pcm", "rb") as pcm_file:
                pcm_data = pcm_file.read()
                audio_chunk = np.frombuffer(pcm_data, dtype='int16')
                write("decrypted_audio.wav", SAMPLE_RATE, audio_chunk)
            print("Plik PCM został przekonwertowany na 'decrypted_audio.wav'.")
        except FileNotFoundError:
            print("Brak pliku 'decrypted_audio.pcm' do konwersji.")

    def play_audio(self):
        while self.running:
            if not decrypted_audio.empty():
                chunk = decrypted_audio.get()
                sd.play(chunk, samplerate=SAMPLE_RATE)
                sd.wait()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Audio Processing App")
    app = RsaStreamWindow(master=root)
    app.pack()
    root.mainloop()

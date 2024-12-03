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

def record_audio():
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, dtype='int16') as stream:
        while True:
            audio_chunk = stream.read(int(SAMPLE_RATE * DURATION))[0].flatten()
            amplitude = np.max(np.abs(audio_chunk))
            if amplitude > THRESHOLD:
                print(f"Wykryto dźwięk! Maksymalna amplituda: {amplitude}")
                recorded_audio.put(audio_chunk)

def encrypt_audio():
    while True:
        if not recorded_audio.empty():
            chunk = recorded_audio.get()
            encrypted_chunks = []

            chunk_bytes = chunk.tobytes()
            remaining_bytes = len(chunk_bytes)
            print(f"Długość danych do szyfrowania: {remaining_bytes} bajtów")

            for i in range(0, len(chunk_bytes), 200):
                block = chunk_bytes[i:i + 200]
                print(f"Długość fragmentu przed szyfrowaniem: {len(block)} bajtów")

                if len(block) <= 200:
                    encrypted_block = cipher_encrypt.encrypt(block)
                    encrypted_chunks.append(encrypted_block)
                else:
                    print(f"Błąd: Blok przekracza dozwolony rozmiar: {len(block)} bajtów")

                remaining_bytes -= len(block)
                print(f"Pozostało {remaining_bytes} bajtów do zaszyfrowania.")

            encrypted_audio.put(encrypted_chunks)
            print(f"Szyfrowanie zakończone: {len(encrypted_chunks)} bloków")

            save_encrypted_audio(encrypted_chunks)

def decrypt_audio():
    while True:
        if not encrypted_audio.empty():
            encrypted_chunks = encrypted_audio.get()
            decrypted_data = bytearray()
            remaining_bytes = sum(len(chunk) for chunk in encrypted_chunks)
            print(f"Długość danych do odszyfrowania: {remaining_bytes} bajtów")

            for i, block in enumerate(encrypted_chunks):
                print(f"Odszyfrowywanie bloku {i + 1}/{len(encrypted_chunks)} o długości {len(block)} bajtów...")
                
                decrypted_block = cipher_decrypt.decrypt(block)
                decrypted_data.extend(decrypted_block)
                
                remaining_bytes -= len(block)
                print(f"Pozostało {remaining_bytes} bajtów do odszyfrowania.")

            audio_chunk = np.frombuffer(decrypted_data, dtype='int16')
            decrypted_audio.put(audio_chunk)
            print(f"Odszyfrowano fragment o długości: {len(audio_chunk)} próbek")

            save_decrypted_audio(audio_chunk)

def play_audio():
    while True:
        if not decrypted_audio.empty():
            chunk = decrypted_audio.get()
            print(f"Odtwarzanie fragmentu o długości: {len(chunk)} próbek")
            if len(chunk) > 0:
                sd.play(chunk, samplerate=SAMPLE_RATE)
                sd.wait()

def save_encrypted_audio(encrypted_chunks):
    encrypted_data = b''.join(encrypted_chunks)
    with open("encrypted_audio.bin", "wb") as f:
        f.write(encrypted_data)
    print("Zapisano zaszyfrowane audio do pliku 'encrypted_audio.bin'.")

def save_decrypted_audio(audio_chunk):
    with open("decrypted_audio.pcm", "ab") as f:
        f.write(audio_chunk.tobytes())
    print("Dodano odszyfrowane audio do pliku 'decrypted_audio.pcm'.")

def convert_pcm_to_wav():
    try:
        with open("decrypted_audio.pcm", "rb") as pcm_file:
            pcm_data = pcm_file.read()
            audio_chunk = np.frombuffer(pcm_data, dtype='int16')
            write("decrypted_audio.wav", SAMPLE_RATE, audio_chunk)
        print("Plik PCM został przekonwertowany na 'decrypted_audio.wav'.")
    except FileNotFoundError:
        print("Brak pliku 'decrypted_audio.pcm' do konwersji.")


def main():
    threads = [
        threading.Thread(target=record_audio, daemon=True),
        threading.Thread(target=encrypt_audio, daemon=True),
        threading.Thread(target=decrypt_audio, daemon=True),
        threading.Thread(target=play_audio, daemon=True),
    ]
    for thread in threads:
        thread.start()

    print("Program działa. Mów do mikrofonu...")
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nProgram zakończony.")
        convert_pcm_to_wav()

if __name__ == "__main__":
    main()
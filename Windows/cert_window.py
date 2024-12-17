import socket
from OpenSSL import SSL
from OpenSSL import crypto
from datetime import datetime
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class CertificateWindow(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = ttk.Label(self, text="Weryfikacja certyfikatu")
        label.pack(pady=10, padx=10)

        self.hostname_label = ttk.Label(self, text="Podaj nazwę domeny:")
        self.hostname_label.pack(anchor="w", padx=5, pady=5)
        
        self.hostname_entry = ttk.Entry(self, width=40)
        self.hostname_entry.pack(padx=5, pady=5)
        
        self.check_button = ttk.Button(self, text="Sprawdź certyfikaty", command=self.check_certificates)
        self.check_button.pack(padx=5, pady=5)
        
        self.text_display = tk.Text(self, wrap="word", width=80, height=20)
        self.text_display.pack(padx=5, pady=5, fill="both", expand=True)
        
        self.save_button = ttk.Button(self, text="Zapisz certyfikaty", command=self.save_certificates)
        self.save_button.pack(pady=5)

    def check_certificates(self):
        hostname = self.hostname_entry.get().strip()
        self.text_display.delete(1.0, tk.END)
        
        if not hostname:
            messagebox.showerror("Błąd", "Nazwa domeny nie może być pusta.")
            return

        try:
            cert_chain = get_certificate_chain(hostname)

            if not cert_chain:
                self.text_display.insert(tk.END, "Nie znaleziono żadnych certyfikatów.\n")
                return

            for i, cert in enumerate(cert_chain):
                self.text_display.insert(tk.END, f"\nCertyfikat {i+1}:\n{'-'*40}\n")
                self.text_display.insert(tk.END, f"Subject: {cert.subject.rfc4514_string()}\n")
                self.text_display.insert(tk.END, f"Issuer: {cert.issuer.rfc4514_string()}\n")
                self.text_display.insert(tk.END, f"Serial Number: {cert.serial_number}\n")
                self.text_display.insert(tk.END, f"Valid From: {cert.not_valid_before_utc.strftime('%Y-%m-%d %H:%M:%S %Z')}\n")
                self.text_display.insert(tk.END, f"Valid Until: {cert.not_valid_after_utc.strftime('%Y-%m-%d %H:%M:%S %Z')}\n")
                self.text_display.insert(tk.END, f"Signature Algorithm: {cert.signature_algorithm_oid._name}\n")

            valid, message = verify_certificate_chain(cert_chain)
            self.text_display.insert(tk.END, f"\nWeryfikacja łańcucha certyfikatów: {message}\n")
        except Exception as e:
            messagebox.showerror("Błąd", f"Wystąpił nieoczekiwany błąd: {e}")

    def save_certificates(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Pliki tekstowe", "*.txt"), ("Wszystkie pliki", "*.*")]
        )
        
        if not file_path:
            return

        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(self.text_display.get(1.0, tk.END))
            messagebox.showinfo("Sukces", "Certyfikaty zapisane pomyślnie.")
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się zapisać certyfikatów: {e}")

def get_certificate_chain(hostname, port=443):
    try:
        context = SSL.Context(SSL.TLS_CLIENT_METHOD)
        context.load_verify_locations(cafile="/etc/ssl/certs/ca-certificates.crt")
        conn = SSL.Connection(context, socket.create_connection((hostname, port)))
        conn.set_tlsext_host_name(hostname.encode())
        conn.set_connect_state()
        conn.do_handshake()

        cert_chain = conn.get_peer_cert_chain()
        if not cert_chain:
            raise RuntimeError("Brak łańcucha certyfikatów.")
        
        parsed_chain = [x509.load_pem_x509_certificate(
            crypto.dump_certificate(crypto.FILETYPE_PEM, cert).decode().encode(), 
            default_backend()) for cert in cert_chain]
        
        conn.close()
        return parsed_chain
    except Exception as e:
        raise RuntimeError(f"Błąd pobierania łańcucha certyfikatów: {e}")

def verify_certificate_chain(cert_chain):
    for i in range(len(cert_chain) - 1):
        issuer = cert_chain[i].issuer
        subject = cert_chain[i + 1].subject
        if issuer != subject:
            return False, f"Certyfikat {i+1} nie został wystawiony przez następny certyfikat."
    return True, "Łańcuch certyfikatów jest prawidłowy."

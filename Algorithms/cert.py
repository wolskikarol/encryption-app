import ssl
import socket
from OpenSSL import SSL
from OpenSSL import crypto
from datetime import datetime
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

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

def main():
    try:
        hostname = input("Podaj nazwę domeny (np. example.com): ").strip()
        if not hostname:
            raise ValueError("Nazwa domeny nie może być pusta.")
        cert_chain = get_certificate_chain(hostname)

        if not cert_chain:
            print("Nie znaleziono żadnych certyfikatów.")
            return

        for i, cert in enumerate(cert_chain):
            print(f"\nCertyfikat {i+1}:{'-'*40}")
            print(f"Subject: {cert.subject.rfc4514_string()}")
            print(f"Issuer: {cert.issuer.rfc4514_string()}")
            print(f"Serial Number: {cert.serial_number}")
            print(f"Valid From: {cert.not_valid_before_utc.strftime('%Y-%m-%d %H:%M:%S %Z')}")
            print(f"Valid Until: {cert.not_valid_after_utc.strftime('%Y-%m-%d %H:%M:%S %Z')}")
            print(f"Signature Algorithm: {cert.signature_algorithm_oid._name}")

        valid, message = verify_certificate_chain(cert_chain)
        print(f"\nWeryfikacja łańcucha certyfikatów: {message}")
    except ValueError as val_err:
        print(f"Błąd: {val_err}")
    except socket.timeout:
        print("Błąd: przekroczono czas oczekiwania na połączenie.")
    except SSL.Error as ssl_err:
        print(f"Błąd weryfikacji certyfikatu: {ssl_err}")
    except RuntimeError as net_err:
        print(f"Błąd sieciowy: {net_err}")
    except Exception as gen_err:
        print(f"Wystąpił nieoczekiwany błąd: {gen_err}")

if __name__ == "__main__":
    main()

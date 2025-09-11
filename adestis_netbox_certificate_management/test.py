print("hallo")

from contextlib import contextmanager
from tempfile import NamedTemporaryFile
from pathlib import Path

from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption
from cryptography.hazmat.primitives.serialization.pkcs12 import load_key_and_certificates


import os



@contextmanager
def pfx_bytes_to_pem(pfx_bytes, pfx_password):
        '''Convert .pfx file to PEM format for use in requests or analysis.'''
        # pfx = Path(pfx_path).read_bytes()
        private_key, main_cert, add_certs = load_key_and_certificates(
            pfx_bytes, pfx_password.encode('utf-8'), None
        )

        with NamedTemporaryFile(suffix=".pem", delete=True, mode="wb") as t_pem:
            t_pem.write(private_key.private_bytes(Encoding.PEM, PrivateFormat.PKCS8, NoEncryption()))
            t_pem.write(main_cert.public_bytes(Encoding.PEM))
            for ca in add_certs or []:
                t_pem.write(ca.public_bytes(Encoding.PEM))
            t_pem.flush()
            yield t_pem.name      
            
# === Testaufruf ===
if __name__ == "__main__":
    # filename = "mycert.pfx"
    filepath = "/home/an/repos/mycert.pfx"
    pfx_password = "meinTestPasswort123"  # <-- hier ggf. dein echtes Passwort eintragen

    try:
        
        with open(filepath, "rb") as f:
            pfx_data = f.read()
            
        with pfx_bytes_to_pem(pfx_data, pfx_password) as pem_path:
            print(f"✅ PEM-Datei wurde erstellt unter: {pem_path}")
            
            # PEM-Datei anzeigen
            with open(pem_path, "r") as pem_file:
                print("📄 PEM-Inhalt:\n")
                print(pem_file.read())

    except FileNotFoundError:
        print(" Datei wurde nicht gefunden.")
    except ValueError as e:
        print(f" Entschlüsselung fehlgeschlagen (falsches Passwort?): {e}")
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
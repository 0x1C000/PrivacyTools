# File: qgp/encrypt.py
"""
Symmetric encryption for QGP using the hybrid shared key derived from Handshake.
Compression with Zstd and encryption with XSalsa20-Poly1305 (SecretBox).
"""
import zstd
from nacl.secret import SecretBox
from nacl.utils import random as random_bytes

class Encryptor:
    @staticmethod
    def encrypt(shared_key: bytes, plaintext: bytes) -> dict:
        """
        Encrypt plaintext using the shared_key:
          - Compress with Zstd
          - Encrypt with SecretBox (XSalsa20-Poly1305)
        Returns dict with:
          'nonce': bytes,
          'ciphertext': bytes
        """
        # Compress input data
        compressed = zstd.compress(plaintext)

        # Create symmetric box
        box = SecretBox(shared_key)

        # Generate nonce
        nonce = random_bytes(SecretBox.NONCE_SIZE)

        # Encrypt: SecretBox.encrypt returns nonce|ciphertext; use box.encrypt(compressed, nonce)
        ciphertext = box.encrypt(compressed, nonce)
        # SecretBox.encrypt prepends nonce; we return ciphertext.ciphertext (without nonce)
        return {
            'nonce': nonce,
            'ciphertext': ciphertext.ciphertext
        }

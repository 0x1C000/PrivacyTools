# File: qgp/decrypt.py
"""
Symmetric decryption for QGP using the hybrid shared key derived from Handshake.
Decompression with Zstd and decryption with XSalsa20-Poly1305 (SecretBox).
"""
import zstd
from nacl.secret import SecretBox

class Decryptor:
    @staticmethod
    def decrypt(shared_key: bytes, nonce: bytes, ciphertext: bytes) -> bytes:
        """
        Decrypt ciphertext using the shared_key and nonce:
          - Decrypt with SecretBox (XSalsa20-Poly1305)
          - Decompress with Zstd
        Returns the original plaintext bytes.
        """
        # Create symmetric box
        box = SecretBox(shared_key)

        # Combine nonce and ciphertext for decryption
        combined = nonce + ciphertext

        # Decrypt compressed data
        compressed = box.decrypt(combined)

        # Decompress and return plaintext
        plaintext = zstd.decompress(compressed)
        return plaintext

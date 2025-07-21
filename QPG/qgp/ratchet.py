# File: qgp/ratchet.py
"""
Simple symmetric ratchet for QGP: derives a new message key for each message by hashing the chain key.
"""
from nacl.secret import SecretBox
from nacl.hash import blake2b
from nacl.encoding import RawEncoder
from nacl.utils import random as random_bytes
import zstd

class SymmetricRatchet:
    """
    A basic symmetric ratchet:
      - `chain_key` evolves by hashing itself.
      - Each message derives a new `message_key` = H(chain_key).
      - Uses SecretBox with XSalsa20-Poly1305 for encryption.
    """
    def __init__(self, root_key: bytes):
        """
        Initialize the ratchet with a 32-byte root key from handshake.
        """
        self.chain_key = root_key

    def _kdf(self):
        """
        Derive next chain key (and message key) via BLAKE2b.
        """
        self.chain_key = blake2b(self.chain_key, encoder=RawEncoder, digest_size=32)
        return self.chain_key

    def encrypt(self, plaintext: bytes) -> dict:
        """
        Encrypt a message:
          1. Derive a new message key via ratchet step.
          2. Compress plaintext with Zstd.
          3. Encrypt with SecretBox and random nonce.
        Returns a dict with 'nonce' and 'ciphertext'.
        """
        msg_key = self._kdf()
        box = SecretBox(msg_key)
        compressed = zstd.compress(plaintext)
        nonce = random_bytes(SecretBox.NONCE_SIZE)
        ciphertext = box.encrypt(compressed, nonce).ciphertext
        return {'nonce': nonce, 'ciphertext': ciphertext}

    def decrypt(self, nonce: bytes, ciphertext: bytes) -> bytes:
        """
        Decrypt a message:
          1. Advance ratchet to derive expected message key.
          2. Decrypt with SecretBox.
          3. Decompress with Zstd.
        """
        msg_key = self._kdf()
        box = SecretBox(msg_key)
        combined = nonce + ciphertext
        compressed = box.decrypt(combined)
        plaintext = zstd.decompress(compressed)
        return plaintext

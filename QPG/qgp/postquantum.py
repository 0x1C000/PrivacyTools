# File: qgp/postquantum.py
"""
Post-Quantum key encapsulation mechanism (KEM) wrapper per QGP usando kyber-py.
"""

# richiede: pip install kyber-py
from kyber_py.ml_kem import ML_KEM_512

class PQPrivateKey:
    """Wrapper per la chiave privata post-quantum."""
    def __init__(self, sk_bytes: bytes):
        self._sk = sk_bytes

    def to_bytes(self) -> bytes:
        return self._sk

    @staticmethod
    def from_bytes(data: bytes) -> 'PQPrivateKey':
        return PQPrivateKey(data)

class PQPublicKey:
    """Wrapper per la chiave pubblica post-quantum."""
    def __init__(self, ek):
        # ML_KEM_512.keygen() restituisce ek (public-key object)
        self._ek = ek

    def to_bytes(self):
        return self._ek  # tieni ek come oggetto per kyber-py

    @staticmethod
    def from_bytes(data) -> 'PQPublicKey':
        return PQPublicKey(data)

class PQEncapsulation:
    """KEM operations: encapsulate e decapsulate via kyber-py."""
    @staticmethod
    def encapsulate(pk: PQPublicKey) -> tuple[bytes, bytes]:
        """
        Encapsula con la public key, ritorna (ciphertext, shared_secret).
        """
        shared_secret, ciphertext = ML_KEM_512.encaps(pk._ek)
        return ciphertext, shared_secret

    @staticmethod
    def decapsulate(sk: PQPrivateKey, ciphertext: bytes) -> bytes:
        """
        Decapsula con la private key, ritorna shared_secret.
        """
        return ML_KEM_512.decaps(sk._sk, ciphertext)

def generate_pq_keypair() -> tuple[PQPrivateKey, PQPublicKey]:
    """
    Genera una coppia KEM (ek, dk) con kyber-py.
    Restituisce (PQPrivateKey(dk), PQPublicKey(ek)).
    """
    ek, dk = ML_KEM_512.keygen()
    return PQPrivateKey(dk), PQPublicKey(ek)

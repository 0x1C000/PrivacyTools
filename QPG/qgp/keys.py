# File: qgp/keys.py
"""
Key management for QGP: ECC (Curve25519) + Post-Quantum (Kyber/NTRU) key generation,
storage, listing, and loading.
"""
import os
from nacl.public import PrivateKey, PublicKey
from nacl.encoding import RawEncoder
from qgp.postquantum import (
    generate_pq_keypair,
    PQPrivateKey,
    PQPublicKey,
)

# Directory for storing key files
KEY_DIR = os.path.expanduser("~/.qgp/keys")
os.makedirs(KEY_DIR, exist_ok=True)

class KeyManager:
    def __init__(self, key_dir=KEY_DIR):
        self.key_dir = key_dir

    def generate_keypair(self, label="default"):
        """
        Generate a hybrid keypair:
          - ECC: Curve25519
          - Post-Quantum: Kyber/NTRU
        Save keys under:
          {label}_ecc.sk, {label}_ecc.pk,
          {label}_pq.sk,  {label}_pq.pk
        Returns tuple of (ecc_sk, ecc_pk, pq_sk, pq_pk)
        """
        # ECC keypair
        ecc_sk = PrivateKey.generate()
        ecc_pk = ecc_sk.public_key
        # PQ keypair
        pq_sk, pq_pk = generate_pq_keypair()

        # Write ECC private key
        with open(os.path.join(self.key_dir, f"{label}_ecc.sk"), "wb") as f:
            f.write(ecc_sk.encode(encoder=RawEncoder))
        # Write ECC public key
        with open(os.path.join(self.key_dir, f"{label}_ecc.pk"), "wb") as f:
            f.write(ecc_pk.encode(encoder=RawEncoder))
        # Write PQ private key
        with open(os.path.join(self.key_dir, f"{label}_pq.sk"), "wb") as f:
            f.write(pq_sk.to_bytes())
        # Write PQ public key
        with open(os.path.join(self.key_dir, f"{label}_pq.pk"), "wb") as f:
            f.write(pq_pk.to_bytes())

        return ecc_sk, ecc_pk, pq_sk, pq_pk

    def list_labels(self):
        """
        List all unique labels for which both ECC and PQ keys exist.
        """
        files = os.listdir(self.key_dir)
        labels = set()
        for filename in files:
            if filename.endswith('_ecc.sk'):
                labels.add(filename.rsplit('_ecc.sk', 1)[0])
        return sorted(labels)

    def load_ecc_private(self, label="default"):
        path = os.path.join(self.key_dir, f"{label}_ecc.sk")
        data = open(path, 'rb').read()
        return PrivateKey(data, encoder=RawEncoder)

    def load_ecc_public(self, label="default"):
        path = os.path.join(self.key_dir, f"{label}_ecc.pk")
        data = open(path, 'rb').read()
        return PublicKey(data, encoder=RawEncoder)

    def load_pq_private(self, label="default"):
        path = os.path.join(self.key_dir, f"{label}_pq.sk")
        data = open(path, 'rb').read()
        return PQPrivateKey.from_bytes(data)

    def load_pq_public(self, label="default"):
        path = os.path.join(self.key_dir, f"{label}_pq.pk")
        data = open(path, 'rb').read()
        return PQPublicKey.from_bytes(data)

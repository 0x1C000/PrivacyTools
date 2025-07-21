# File: qgp/handshake.py
"""
Hybrid handshake for QGP combining ECC (X25519) and Post-Quantum KEM (Kyber512).
Derives a shared symmetric key via BLAKE2b from both secrets.
"""
from nacl.public import Box
from nacl.hash import blake2b
from nacl.encoding import RawEncoder
from qgp.postquantum import PQEncapsulation

class Handshake:
    @staticmethod
    def initiate(sender_ecc_sk, receiver_ecc_pk, receiver_pq_pk):
        """
        Initiator creates shared key and PQ ciphertext:
        - ECC shared secret via X25519
        - PQ KEM encapsulation
        Derives final shared key = BLAKE2b(ecc_ss || pq_ss)
        Returns dict with:
          'ciphertext_pq': bytes, KEM ciphertext
          'shared_key': bytes, 32-byte symmetric key
        """
        # ECC shared secret
        ecc_box = Box(sender_ecc_sk, receiver_ecc_pk)
        ecc_ss = ecc_box.shared_key()

        # PQ KEM encapsulation
        ct_pq, pq_ss = PQEncapsulation.encapsulate(receiver_pq_pk)

        # Derive final shared key
        concat = ecc_ss + pq_ss
        shared_key = blake2b(concat, encoder=RawEncoder, digest_size=32)

        return {"ciphertext_pq": ct_pq, "shared_key": shared_key}

    @staticmethod
    def respond(receiver_ecc_sk, sender_ecc_pk, receiver_pq_sk, ciphertext_pq):
        """
        Responder recovers shared key:
        - ECC shared secret via X25519
        - PQ KEM decapsulation
        Derives final shared key = BLAKE2b(ecc_ss || pq_ss)
        Returns bytes: 32-byte symmetric key
        """
        # ECC shared secret
        ecc_box = Box(receiver_ecc_sk, sender_ecc_pk)
        ecc_ss = ecc_box.shared_key()

        # PQ KEM decapsulation
        pq_ss = PQEncapsulation.decapsulate(receiver_pq_sk, ciphertext_pq)

        # Derive final shared key
        concat = ecc_ss + pq_ss
        shared_key = blake2b(concat, encoder=RawEncoder, digest_size=32)

        return shared_key

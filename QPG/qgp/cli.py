# File: qgp/cli.py
"""
Command-line interface for QGP (Quantum Good Privacy).
Supports key management, hybrid handshake, encryption/decryption, and revocation.
"""
import argparse
import sys
import binascii

from qgp.keys import KeyManager
from qgp.postquantum import PQPublicKey
from qgp.handshake import Handshake
from qgp.encrypt import Encryptor
from qgp.decrypt import Decryptor

# Helper to convert hex to bytes
def hex2bytes(s: str) -> bytes:
    try:
        return binascii.unhexlify(s)
    except binascii.Error:
        print("Invalid hex input.")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(prog="qgp", description="Quantum Good Privacy CLI")
    sub = parser.add_subparsers(dest="cmd")

    # keygen
    kg = sub.add_parser("keygen", help="Generate ECC+PQ keypair")
    kg.add_argument("--label", default="default", help="Label for the keypair")

    # list-keys
    sub.add_parser("list-keys", help="List available key labels")

    # send
    snd = sub.add_parser("send", help="Encrypt and output message payload for a peer")
    snd.add_argument("--sender", default="default", help="Your key label to send from")
    snd.add_argument("--to", required=True, help="Peer key label to send to")
    snd.add_argument("--msg", required=True, help="Message text to send")

    # receive
    rcv = sub.add_parser("receive", help="Decrypt incoming payload from a peer")
    rcv.add_argument("--sender", default="default", help="Your key label to receive with")
    rcv.add_argument("--from", dest="frm", required=True, help="Peer key label that sent the message")
    rcv.add_argument("--pqct", required=True, help="PQ KEM ciphertext hex string")
    rcv.add_argument("--nonce", required=True, help="Nonce hex string for symmetric decrypt")
    rcv.add_argument("--ciphertext", required=True, help="Symmetric ciphertext hex string")

    # revoke
    rv = sub.add_parser("revoke", help="Publish a key revocation")
    rv.add_argument("--key", required=True, help="Key fingerprint or label to revoke")
    rv.add_argument("--reason", help="Optional reason for revocation")

    # subscribe
    sub.add_parser("subscribe", help="Listen for revocation notices")

    args = parser.parse_args()
    km = KeyManager()

    if args.cmd == "keygen":
        ecc_sk, ecc_pk, pq_sk, pq_pk = km.generate_keypair(args.label)
        print(f"✔ Generated keypair '{args.label}'")
        print(f"  ECC Private:  {args.label}_ecc.sk")
        print(f"  ECC Public:   {args.label}_ecc.pk")
        print(f"  PQ Private:   {args.label}_pq.sk")
        print(f"  PQ Public:    {args.label}_pq.pk")

    elif args.cmd == "list-keys":
        labels = km.list_labels()
        if labels:
            print("Available key labels:")
            for lbl in labels:
                print(f" - {lbl}")
        else:
            print("No keypairs found. Generate one with 'qgp keygen'.")

    elif args.cmd == "send":
        # Load sender keys
        sk_ecc = km.load_ecc_private(args.sender)
        # Load receiver public keys
        pk_ecc = km.load_ecc_public(args.to)
        pq_pk = km.load_pq_public(args.to)
        # Hybrid handshake
        hs = Handshake.initiate(sk_ecc, pk_ecc, pq_pk)
        shared = hs['shared_key']
        ct_pq = hs['ciphertext_pq']
        # Symmetric encryption
        enc = Encryptor.encrypt(shared, args.msg.encode())
        # Output payloads
        print("# PQ KEM ciphertext (hex):", ct_pq.hex())
        print("# Nonce (hex):", enc['nonce'].hex())
        print("# Ciphertext (hex):", enc['ciphertext'].hex())

    elif args.cmd == "receive":
        # Load receiver (your) keys
        sk_ecc = km.load_ecc_private(args.sender)
        pq_sk = km.load_pq_private(args.sender)
        # Load sender public key
        pk_ecc = km.load_ecc_public(args.frm)
        # Hybrid respond: use PQ ciphertext
        shared = Handshake.respond(
            sk_ecc,
            pk_ecc,
            pq_sk,
            hex2bytes(args.pqct)
        )
        # Symmetric decryption: use nonce and ciphertext
        plaintext = Decryptor.decrypt(
            shared,
            hex2bytes(args.nonce),
            hex2bytes(args.ciphertext)
        )
        print("Decrypted message:", plaintext.decode())

    elif args.cmd == "revoke":
        from qgp.revocation import RevocationManager
        rm = RevocationManager()
        cid = rm.publish_revocation(args.key, args.reason)
        print(f"Published revocation record CID: {cid}")

    elif args.cmd == "subscribe":
        from qgp.revocation import RevocationManager
        rm = RevocationManager()
        print("Listening for revocations. Press Ctrl+C to stop.")
        def callback(rec):
            print(f"Revocation notice: {rec}")
        try:
            rm.subscribe_revocations(callback)
            import time
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Stopped listening.")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()

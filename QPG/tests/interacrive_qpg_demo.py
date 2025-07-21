#!/usr/bin/env python3
import sys
from nacl.public import PrivateKey, PublicKey, Box
from nacl.encoding import HexEncoder
from nacl.utils import random as random_bytes

def generate_user(name):
    sk = PrivateKey.generate()
    pk = sk.public_key
    return {"name": name, "sk": sk, "pk": pk}

def hexify(b):
    return b.hex()

def main():
    print("\nQGP Interactive Handshake & Encryption Demo\n" + "-"*44)
    # 1) Generate two users
    users = [generate_user("Alice"), generate_user("Bob")]

    print("Generated users & their public keys:")
    for idx, u in enumerate(users, start=1):
        print(f"  [{idx}] {u['name']}  -> Public Key: {u['pk'].encode(encoder=HexEncoder).decode()}")

    # 2) Select sender and receiver
    try:
        i = int(input("\nSelect sender (1 or 2): ").strip())
        j = int(input("Select receiver (1 or 2, not same as sender): ").strip())
        assert i in (1,2) and j in (1,2) and i != j
    except (ValueError, AssertionError):
        print("Invalid selection. Exiting.")
        sys.exit(1)

    sender = users[i-1]
    receiver = users[j-1]

    # 3) Prompt for message
    plaintext = input(f"\nEnter message to send from {sender['name']} to {receiver['name']}: ").encode()

    # 4) Show keys and derive Box
    print(f"\nStep 1: Load keys")
    print(f"  {sender['name']} Private Key (hex): {sender['sk'].encode(encoder=HexEncoder).decode()}")
    print(f"  {receiver['name']} Public  Key (hex): {receiver['pk'].encode(encoder=HexEncoder).decode()}")

    box = Box(sender['sk'], receiver['pk'])
    print("\nStep 2: Derive shared secret (internal to Box)")
    shared = box.shared_key()
    print(f"  Shared secret (hex): {hexify(shared)}")

    # 5) Encrypt
    nonce = random_bytes(Box.NONCE_SIZE)
    ciphertext = box.encrypt(plaintext, nonce)

    print("\nStep 3: Encrypt")
    print(f"  Nonce (hex):      {hexify(nonce)}")
    print(f"  Ciphertext (hex): {hexify(ciphertext.ciphertext)}")

    # 6) Decrypt
    print("\nStep 4: Decrypt at receiver side")
    recv_box = Box(receiver['sk'], sender['pk'])
    decrypted = recv_box.decrypt(ciphertext)
    print(f"  Decrypted text:   {decrypted.decode()}\n")

    # Check
    if decrypted == plaintext:
        print("✅ Success: plaintext round-trip OK.")
    else:
        print("❌ Failure: decrypted text does not match original.")

if __name__ == "__main__":
    main()

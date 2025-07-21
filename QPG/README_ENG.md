# QGP (Quantum Good Privacy)

Hybrid post-quantum & ECC secure messaging CLI.

## Prerequisites

* Python ≥ 3.8
* IPFS daemon running (optional, only for key revocation)
* **Virtualenv** (recommended)

## Installation

```bash
# Navigate to the project directory
cd ~/Desktop/QPG

# 1) Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2) Install the package in editable mode
pip install -e .

# 3) Install additional dependencies
pip install ipfshttpclient zstd kyber-py
```

> After this, the `qgp` command will be available in your active shell.

## Key Storage Structure

Keypairs are stored under `~/.qgp/keys/` with these filenames:

```
<label>_ecc.sk   # ECC private key (Curve25519)
<label>_ecc.pk   # ECC public key  
<label>_pq.sk    # PQ private key (Kyber)
<label>_pq.pk    # PQ public key   
```

## Configuration and Logs

* **Config file:** `~/.qgp/config.json`
* **Log file:**    `~/.qgp/qgp.log`

You can edit `ipfs_address` or `revocation_topic` in the config file if needed.

## CLI Usage

```bash
qgp <command> [flags]
```

### keygen

Generate a new ECC + Post-Quantum keypair:

```bash
qgp keygen --label <label>
```

* `--label`: identifier for the keypair (default: `default`)

### list-keys

List all stored key labels:

```bash
qgp list-keys
```

### send

Encrypt and output payload for a peer:

```bash
qgp send \
  --sender <your_label> \
  --to <peer_label> \
  --msg "<message_text>"
```

* `--sender`: your key label to send from
* `--to`: recipient's key label
* `--msg`: plaintext message

**Outputs:**

```
# PQ KEM ciphertext (hex): <PQCT_HEX>
# Nonce (hex):               <NONCE_HEX>
# Ciphertext (hex):          <CT_HEX>
```

### receive

Decrypt an incoming payload:

```bash
qgp receive \
  --sender <your_label> \
  --from <peer_label> \
  --pqct <PQCT_HEX> \
  --nonce <NONCE_HEX> \
  --ciphertext <CT_HEX>
```

* `--sender`: your key label to decrypt with
* `--from`: sender's key label
* `--pqct`: PQ KEM ciphertext from handshake
* `--nonce`: nonce for symmetric decryption
* `--ciphertext`: symmetric ciphertext

**Outputs:**

```
Decrypted message: <original_text>
```

### revoke

Publish a key revocation record via IPFS PubSub:

```bash
qgp revoke --key <label> [--reason "<reason_text>"]
```

* `--key`: label or fingerprint of the key to revoke
* `--reason`: optional human-readable reason

This command prints the CID of the revocation record.

### subscribe

Listen for revocation notices in real time:

```bash
qgp subscribe
```

* Press **Ctrl+C** to stop.

## Full Workflow Example

1. **Generate keys**:

   ```bash
   qgp keygen --label bob
   qgp keygen --label alice
   ```
2. **Send a message** (Bob → Alice):

   ```bash
   qgp send --sender bob --to alice --msg "Hello Alice!"
   ```
3. **Receive and decrypt** (Alice):

   ```bash
   qgp receive --sender alice --from bob \
     --pqct <PQCT_HEX> --nonce <NONCE_HEX> --ciphertext <CT_HEX>
   ```
4. **Publish a revocation** (Bob revoking Alice):

   ```bash
   qgp revoke --key alice --reason "compromised"
   qgp subscribe
   ```

## Roadmap

* Double Ratchet for per-message forward secrecy
* Group chat support (MLS)
* Decentralized store-and-forward
* Email client plugins (Thunderbird, Mutt)
* Desktop/mobile GUI

---

*QGP v0.1.0*
made by 0x1C

# QGP (Quantum Good Privacy)

Hybrid post-quantum & ECC secure messaging CLI.

##  Prerequisiti

* Python ≥ 3.8
* IPFS daemon in esecuzione (opzionale, solo per revoca)
* **Virtualenv** (consigliato)

##  Installazione

```bash
# Posizionati nella cartella del progetto
cd ~/Desktop/QPG

# 1) Crea e attiva virtualenv
python3 -m venv .venv
source .venv/bin/activate

# 2) Installa dipendenze e pacchetto in modalità editable
pip install -e .

# 3) Installa librerie aggiuntive
pip install ipfshttpclient zstd kyber-py
```

> Il comando `qgp` sarà ora disponibile nel PATH attivo.

## Struttura Chiavi

I keypair vengono salvati in `~/.qgp/keys/` con il formato:

```
<label>_ecc.sk   # privata ECC (Curve25519)
<label>_ecc.pk   # pubblica  "
<label>_pq.sk    # privata PQ (Kyber)
<label>_pq.pk    # pubblica  "
```

## Configurazione e Log

* **Config file:**  `~/.qgp/config.json`
* **Log file:**     `~/.qgp/qgp.log`

Modifica `ipfs_address` o `revocation_topic` in `config.json` se necessario.

## CLI Usage

```bash
qgp <comando> [flags]
```

### keygen

Genera coppia ECC + PQ:

```
qgp keygen --label <label>
```

* `--label`: nome identificativo (default: `default`)

### list-keys

Elenca tutti i label disponibili:

```
qgp list-keys
```

### send

Cifra e produce payload per un peer:

```
qgp send \
  --sender <your_label> \
  --to <peer_label> \
  --msg "<testo>"
```

* `--sender`: tua chiave di invio (label)
* `--to`: label del destinatario
* `--msg`: testo da cifrare

**Output:**

```
# PQ KEM ciphertext (hex): <PQCT>
# Nonce (hex):                <NONCE>
# Ciphertext (hex):           <CT>
```

### receive

Decifra un payload ricevuto:

```
qgp receive \
  --sender <your_label> \
  --from <peer_label> \
  --pqct <PQCT_hex> \
  --nonce <nonce_hex> \
  --ciphertext <ct_hex>
```

* `--sender`: tua chiave per decifrare
* `--from`: peer che ha inviato
* `--pqct`: ciphertext PQ KEM da handshake
* `--nonce`: nonce per SecretBox
* `--ciphertext`: ciphertext simmetrico

**Output:**

```
Decrypted message: <testo originale>
```

### revoke

Pubblica revoca di una chiave su IPFS PubSub:

```
qgp revoke --key <label> [--reason "<testo>"]
```

* `--key`: label o fingerprint da revocare
* `--reason`: motivo (opzionale)

Restituisce il **CID** del record.

### subscribe

Ascolta le notifiche di revoca in tempo reale:

```
qgp subscribe
```

Interrompi con `Ctrl+C`.

##  Esempio completo

1. Generazione chiavi:

   ```bash
   qgp keygen --label bob
   qgp keygen --label alice
   ```
2. Invio:

   ```bash
   qgp send --sender bob --to alice --msg "Ciao Alice!"
   ```
3. Ricezione:

   ```bash
   qgp receive --sender alice --from bob \
     --pqct <PQCT> --nonce <NONCE> --ciphertext <CT>
   ```
4. Revoca di test:

   ```bash
   qgp revoke --key alice --reason "compromesso"
   qgp subscribe
   ```

## Roadmap

* Double Ratchet messaggio-per-messaggio
* Group chat (MLS)
* Store-and-forward decentralizzato
* Plugin mail (Thunderbird, Mutt)
* GUI desktop/mobile

---

*QGP v0.1.0*
Made by 0x1C

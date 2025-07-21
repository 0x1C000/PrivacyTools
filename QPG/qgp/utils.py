# File: qgp/utils.py
"""
Utility functions for QGP: configuration management, logging setup, and serialization helpers.
"""
import os
import json
import logging
from pathlib import Path

# Default config directory and file
CONFIG_DIR = Path(os.path.expanduser("~/.qgp"))
CONFIG_FILE = CONFIG_DIR / "config.json"
LOG_FILE = CONFIG_DIR / "qgp.log"

# Ensure config directory exists
CONFIG_DIR.mkdir(parents=True, exist_ok=True)

# Default configuration
DEFAULT_CONFIG = {
    "ipfs_address": "/ip4/127.0.0.1/tcp/5001",
    "revocation_topic": "qgp-revocations",
    "log_level": "INFO"
}

# Load or create configuration

def load_config():
    if not CONFIG_FILE.exists():
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)


def save_config(config: dict):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)


def setup_logging(level=None):
    cfg = load_config()
    log_level = getattr(logging, level or cfg.get('log_level', 'INFO').upper(), logging.INFO)
    logging.basicConfig(
        filename=str(LOG_FILE),
        level=log_level,
        format='%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%dT%H:%M:%SZ'
    )
    # Also log to console
    console = logging.StreamHandler()
    console.setLevel(log_level)
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    console.setFormatter(formatter)
    logging.getLogger().addHandler(console)


def serialize_bytes(data: bytes) -> str:
    """Convert bytes to hex string for serialization."""
    return data.hex()


def deserialize_bytes(data_str: str) -> bytes:
    """Convert hex string back to bytes."""
    return bytes.fromhex(data_str)

# File: qgp/__init__.py
"""
QGP (Quantum Good Privacy) package initialization.
Imports core classes and defines the package version.
"""

__version__ = "0.1.0"

# Expose core components at package level
from .keys import KeyManager
from .postquantum import PQPublicKey, PQPrivateKey, PQEncapsulation
from .handshake import Handshake
from .encrypt import Encryptor
from .decrypt import Decryptor
from .revocation import RevocationManager
from .utils import load_config, save_config, setup_logging, serialize_bytes, deserialize_bytes

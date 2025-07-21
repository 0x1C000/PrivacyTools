# File: qgp/revocation.py
"""
Decentralized revocation manager for QGP using IPFS PubSub.
Publishes and listens for revocation records via IPFS.
"""
import json
import threading
from datetime import datetime
import ipfshttpclient

# Default PubSub topic
TOPIC = "qgp-revocations"

class RevocationManager:
    def __init__(self, ipfs_addr: str = None):
        """
        Initialize IPFS client. Requires a local IPFS daemon.
        :param ipfs_addr: API address, e.g. '/ip4/127.0.0.1/tcp/5001'
        """
        addr = ipfs_addr or "/ip4/127.0.0.1/tcp/5001"
        self.client = ipfshttpclient.connect(addr)
        self.topic = TOPIC

    def publish_revocation(self, key_fingerprint: str, reason: str = None) -> str:
        """
        Publish a revocation record to IPFS and broadcast via PubSub.
        :param key_fingerprint: identifier of the revoked key
        :param reason: optional text hint
        :return: CID of the stored revocation record
        """
        record = {
            'fingerprint': key_fingerprint,
            'reason': reason or '',
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }
        # Add record to IPFS
        cid = self.client.add_json(record)
        # Broadcast CID on PubSub
        self.client.pubsub.publish(self.topic, cid)
        return cid

    def subscribe_revocations(self, callback, stop_event: threading.Event = None):
        """
        Subscribe to the revocation topic and invoke callback for each record.
        :param callback: function accepting a record dict
        :param stop_event: threading.Event to signal termination
        """
        def _listen():
            sub = self.client.pubsub.subscribe(self.topic)
            for msg in sub:
                try:
                    cid = msg['data'].decode()
                    record = self.client.get_json(cid)
                    callback(record)
                except Exception:
                    continue
                if stop_event and stop_event.is_set():
                    break
        thread = threading.Thread(target=_listen, daemon=True)
        thread.start()
        return thread

    def list_revocations(self, cids: list) -> list:
        """
        Retrieve a list of revocation records given their CIDs.
        :param cids: list of CID strings
        :return: list of record dicts
        """
        records = []
        for cid in cids:
            try:
                rec = self.client.get_json(cid)
                records.append(rec)
            except Exception:
                continue
        return records

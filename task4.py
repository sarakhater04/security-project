import hashlib
import os
import time
import json
from datetime import datetime


FILES_TO_MONITOR = [
    r"C:\Users\Administrator\OneDrive\Desktop\load_file.txt",
]

HASH_STORE = "file_hashes.json"
LOG_FILE = "integrity_log.txt"
CHECK_INTERVAL = 60  


def calculate_hash(file_path):
    """Calculate SHA256 hash of a file."""
    sha256 = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
                
        return sha256.hexdigest()
    except FileNotFoundError:
        return None


def load_hashes():
    """Load previously stored hashes."""
    if os.path.exists(HASH_STORE):
        with open(HASH_STORE, "r") as f:
            return json.load(f)
    return {}


def save_hashes(hashes):
    """Save hashes to a file."""
    with open(HASH_STORE, "w") as f:
        json.dump(hashes, f, indent=4)


def log_change(message):
    """Log changes to a text file."""
    with open(LOG_FILE, "a") as log:
        log.write(f"{datetime.now()} - {message}\n")


def initialize_hashes():
    """Generate initial hashes if none exist."""
    hashes = {}
    for file in FILES_TO_MONITOR:
        hash_value = calculate_hash(file)
        if hash_value:
            hashes[file] = hash_value
    save_hashes(hashes)
    print("Initial hashes generated and saved.")


def check_integrity():
    """Check if any monitored file has changed."""
    stored_hashes = load_hashes()
    for file in FILES_TO_MONITOR:
        print(f"Checking file path: {file}")
        current_hash = calculate_hash(file)
        if current_hash is None:
            log_change(f"File missing: {file}")
        elif file not in stored_hashes:
            log_change(f"New file added: {file}")
            stored_hashes[file] = current_hash
        elif stored_hashes[file] != current_hash:
            log_change(f"File modified: {file}")
            stored_hashes[file] = current_hash

    save_hashes(stored_hashes)


if __name__ == "__main__":
    if not os.path.exists(HASH_STORE):
        initialize_hashes()

    print("Monitoring files for integrity changes...")
    while True:
        check_integrity()
        time.sleep(CHECK_INTERVAL)

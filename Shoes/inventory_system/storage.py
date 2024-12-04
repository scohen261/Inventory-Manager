import json
import os

DATA_FILE = "data/inventory.json"

def load_inventory():
    """Load inventory data from a JSON file."""
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, 'r') as file:
        return json.load(file)

def save_inventory(data):
    """Save inventory data to a JSON file."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=2)


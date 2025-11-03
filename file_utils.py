# file_utils.py
# Handles all JSON file read/write operations

import os
import json
import time
from config import console

def read_data(file):
    """Reads a JSON file and returns its content as a list."""
    if not os.path.exists(file):
        with open(file, "w") as f:
            json.dump([], f)
        return []

    with open(file, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def write_data(file, data):
    """Writes a list to a JSON file with indentation."""
    os.makedirs(os.path.dirname(file) or ".", exist_ok=True)
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

def save_entry(file, entry):
    """Appends a new entry to a JSON list file."""
    data = read_data(file)
    data.append(entry)
    write_data(file, data)
    console.print(f"✅ Saved successfully to: [cyan]{os.path.abspath(file)}[/cyan]", style="green")
    time.sleep(0.5)

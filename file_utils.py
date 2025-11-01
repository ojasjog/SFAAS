# file_utils.py
# Handles all JSON file read/write operations

import os
import json
import time
from config import console 

def read_data(file):
    """Reads a JSON file and returns its content as a list.
    Returns an empty list if the file doesn't exist or is empty.
    """
    if os.path.exists(file):
        with open(file, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def write_data(file, data):
    """Writes a list to a JSON file with indentation."""
    with open(file, "w") as f:
        json.dump(data, f, indent=2)

def save_entry(file, entry):
    """Reads data from a file, appends a new entry, and writes back."""
    data = read_data(file)
    data.append(entry)
    write_data(file, data)
    console.print("✅ Saved successfully!", style="green")
    time.sleep(1)
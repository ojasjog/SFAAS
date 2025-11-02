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
    if not os.path.exists(file):
        # If the file doesn't exist, create it as an empty list
        with open(file, "w") as f:
            json.dump([], f)
        return []

    with open(file, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            # If file is corrupted, reset it to an empty list
            return []

def write_data(file, data):
    """Writes a list to a JSON file with indentation."""
    # Ensure file directory exists (helps if you use subfolders)
    os.makedirs(os.path.dirname(file) or ".", exist_ok=True)
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

def save_entry(file, entry):
    """Reads data from a file, appends a new entry, and writes back."""
    data = read_data(file)
    data.append(entry)
    write_data(file, data)

    # Debug print (shows exact path)
    console.print(f"✅ Saved successfully to: [cyan]{os.path.abspath(file)}[/cyan]", style="green")
    time.sleep(1)

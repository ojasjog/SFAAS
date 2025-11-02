# admin_module.py
# All logic for the Admin user role

import time
from datetime import datetime
from rich.progress import track
from config import console, FORECAST_FILE, ADVISORY_FILE
from file_utils import save_entry

# --- Admin Menu Actions ---

def add_seasonal_forecast():
    """Handles logic for Admin Menu choice 1."""
    for i in track(range(1,4), description="Processing"):
        time.sleep(0.25)
    
    console.print("\n--- Add New Seasonal Forecast ---", style="bold")
    season = input("Enter season: ")
    region = input("Enter region: ")
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")
    rainfall = input("Enter rainfall (in mm): ")
    temperature = input("Enter temperature (in °C): ")
    humidity = input("Enter humidity (in %): ")
    crop_suggestions = input("Enter crop suggestions (comma-separated): ")
    pest_alert = input("Enter pest alert (comma-separated): ")

    entry = {
        "season": season,
        "region": region,
        "dates": {"start": start_date, "end": end_date},
        "weather_forecast": {
            "rainfall": rainfall, "temperature": temperature, "humidity": humidity
        },
        # Use .strip() to clean up user input
        "crop_suggestions": [c.strip() for c in crop_suggestions.split(",")],
        "pest_alert": [p.strip() for p in pest_alert.split(",")],
        "timestamp": datetime.now().isoformat()
    }
    
    save_entry(FORECAST_FILE, entry)
    console.print("Returning to Admin Menu...", style="green")
    time.sleep(1)

def manage_crop_advisories():
    """Handles logic for Admin Menu choice 3."""
    console.print("\n--- Manage Crop Advisories ---", style="bold")
    Crop = input("Enter Crop Name: ")
    Season = input("Enter Season: ")
    Practices = input("Enter Appropriate Practices: ")
    Fertilizers = input("Enter Fertilizers Name: ")
    Precaution = input("Enter Precaution to be taken: ") # Corrected typo

    entry = {
        "Crop": Crop,
        "Season": Season,
        "Practices": Practices,
        "Fertilizers": Fertilizers,
        "Precaution": Precaution,
        "timestamp": datetime.now().isoformat()
    }
    
    save_entry(ADVISORY_FILE, entry)
    console.print("Advisory saved. Returning to Admin Menu...", style="green")
    time.sleep(1)

# --- Placeholder functions for other admin options ---

def update_delete_forecast():
    for i in track(range(1,4), description="Processing"):
        time.sleep(0.25)
    print("Loading 2... (Functionality not yet implemented)")
    time.sleep(1)

def upload_bulk_data():
    for i in track(range(1,4), description="Processing"):
        time.sleep(0.25)
    print("Loading 4... (Functionality not yet implemented)")
    time.sleep(1)

def generate_reports():
    for i in track(range(1,4), description="Processing"):
        time.sleep(0.25)
    print("Loading 5... (Functionality not yet implemented)")
    time.sleep(1)

def manage_farmer_queries():
    for i in track(range(1,4), description="Processing"):
        time.sleep(0.25)
    print("Loading 6... (Functionality not yet implemented)")
    time.sleep(1)

# --- Main Admin Menu Loop ---

def admin_login():
    """Displays the admin menu and handles user choice."""
    while True:
        console.print("\n--- Admin Menu ---", style="bold underline black on white")
        print("1. Add Seasonal Forecast")
        print("2. Update/Delete Forecast")
        print("3. Manage Crop Advisories")
        print("4. Upload Bulk Forecast Data")
        print("5. Generate Reports")
        print("6. Manage Farmer Queries")
        print("7. Logout")

        choice = input("Enter choice: ")

        if choice == "1":
            add_seasonal_forecast()
        elif choice == "2":
            update_delete_forecast()
        elif choice == "3":
            manage_crop_advisories()
        elif choice == "4":
            upload_bulk_data()
        elif choice == "5":
            generate_reports()
        elif choice == "6":
            manage_farmer_queries()
        elif choice == "7":
            console.print("Logging out...", style="red")
            break  # Exit the while loop to return to the main menu
        else:
            console.print("Invalid choice.", style="red")
# Run admin menu when file is executed directly
if __name__ == "__main__":
    admin_login()

# # farmer_module.py
# # All logic for the Farmer user role

# import os
# import pandas as pd
# from tabulate import tabulate
# from config import console, FARMERS_FILE, DATA_CSV_FOLDER, FORECAST_FILE
# from file_utils import read_data, save_entry
# import json
# from config import FARMERS_FILE, console
# # Set pandas option

# pd.set_option('display.max_rows', None)

# # --- Farmer Menu Actions ---

# def view_seasonal_forecast():
#     """Displays all seasonal forecasts in a clean table, flattening mixed data."""
#     console.print("\n=== Seasonal Forecasts ===", style="bold cyan")

#     try:
#         with open(FORECAST_FILE, "r") as f:
#             forecasts = json.load(f)

#         if not forecasts:
#             console.print("⚠ No forecasts found.", style="yellow")
#             return

#         table_data = []
#         for fc in forecasts:
#             # --- Handle missing or malformed entries safely ---
#             if not isinstance(fc, dict):
#                 continue

#             season = str(fc.get("season", "N/A")).strip()
#             region = str(fc.get("region", "N/A")).strip()

#             # Dates can come as dict or string
#             dates = fc.get("dates", {})
#             if isinstance(dates, dict):
#                 start_date = str(dates.get("start", "N/A"))
#                 end_date = str(dates.get("end", "N/A"))
#             elif isinstance(dates, str) and "->" in dates:
#                 start_date, end_date = map(str.strip, dates.split("->"))
#             else:
#                 start_date = end_date = str(dates)
#             date_range = f"{start_date} → {end_date}"

#             # Weather details can be dict or plain strings
#             weather = fc.get("weather_forecast", {})
#             if isinstance(weather, dict):
#                 rainfall = str(weather.get("rainfall", "N/A"))
#                 temperature = str(weather.get("temperature", "N/A"))
#                 humidity = str(weather.get("humidity", "N/A"))
#             else:
#                 rainfall = temperature = humidity = str(weather)

#             # Crop suggestions and pest alerts
#             crops = fc.get("crop_suggestions", [])
#             pests = fc.get("pest_alert", [])

#             # Convert lists or strings to uniform text
#             if isinstance(crops, list):
#                 crops = ", ".join(crops)
#             if isinstance(pests, list):
#                 pests = ", ".join(pests)

#             crops = str(crops or "N/A")
#             pests = str(pests or "N/A")

#             # Add to table
#             table_data.append([
#                 season, region, date_range,
#                 rainfall, temperature, humidity,
#                 crops, pests
#             ])

#         headers = [
#             "Season", "Region", "Date Range",
#             "Rainfall (mm)", "Temperature (°C)", "Humidity (%)",
#             "Crop Suggestions", "Pest Alerts"
#         ]

#         print()
#         print(tabulate(table_data, headers=headers, tablefmt="grid", showindex=True))

#     except FileNotFoundError:
#         console.print("⚠ forecasts.json file not found.", style="red")
#     except json.JSONDecodeError:
#         console.print("⚠ Error reading forecasts.json (invalid JSON).", style="red")
#     except Exception as e:
#         console.print(f"⚠ Unexpected error: {e}", style="red")

# def access_crop_advisories():
#     print("Loading 2... (Functionality not yet implemented)")

# def search_historical_data():
#     """Handles logic for Farmer Menu choice 3."""
#     print("Loading 3...")
    
#     if not os.path.exists(DATA_CSV_FOLDER):
#         console.print(f"Error: Directory '{DATA_CSV_FOLDER}' not found.", style="red")
#         return

#     csv_files = [f for f in os.listdir(DATA_CSV_FOLDER) if f.endswith('.csv')]
    
#     if not csv_files:
#         console.print(f"No CSV files found in '{DATA_CSV_FOLDER}'.", style="yellow")
#         return

#     print("="*50)
#     print("📂 Available CSV Files 📂".center(50))
#     print("="*50)
#     for i, file in enumerate(csv_files):
#         print(f"{i + 1}. {file}")
#     print("="*50)

#     try:
#         choice = int(input("Enter the number of the CSV file you want to display: "))
#         if 1 <= choice <= len(csv_files):
#             file_to_read = csv_files[choice - 1]
#             file_path = os.path.join(DATA_CSV_FOLDER, file_to_read)
#             df = pd.read_csv(file_path)

#             print("\n" + "="*50)
#             print(f"📄 Displaying: {file_to_read}".center(50))
#             print(f"Shape: {df.shape[0]} rows x {df.shape[1]} columns".center(50))
#             print("="*50)

#             view_option = input("View (1) First & Last 5 rows or (2) Entire file? Enter 1 or 2: ").strip()
            
#             if view_option == '1':
#                 print("\n--- First 5 Rows ---")
#                 print(tabulate(df.head(), headers='keys', tablefmt='fancy_grid', showindex=True))
#                 print("\n--- Last 5 Rows ---")
#                 print(tabulate(df.tail(), headers='keys', tablefmt='fancy_grid', showindex=True))
#             elif view_option == '2':
#                 print("\n--- Entire File ---")
#                 print(tabulate(df, headers='keys', tablefmt='fancy_grid', showindex=True))
#             else:
#                 print("❌ Invalid option. Showing first & last 5 rows by default.")
#                 print(tabulate(df.head(), headers='keys', tablefmt='fancy_grid', showindex=True))
#                 print(tabulate(df.tail(), headers='keys', tablefmt='fancy_grid', showindex=True))

#             print("\n" + "="*50)
#             print("✅ End of CSV Display".center(50))
#             print("="*50)

#         else:
#             print("❌ Invalid choice.")
#     except ValueError:
#         print("❌ Please enter a valid number.")
#     except FileNotFoundError:
#         console.print(f"Error: File '{file_to_read}' not found.", style="red")
#     except Exception as e:
#         console.print(f"An unexpected error occurred: {e}", style="red")

# def submit_query():
#     print("Loading 4... (Functionality not yet implemented)")

# def manage_profile():
#     print("Loading 5... (Functionality not yet implemented)")

# def farmer_login_menu(username):
#     """Displays the farmer menu and handles user choice."""
#     while True:
#         console.print(f"\n--- Farmer Menu (Welcome {username}) ---", style="bold underline black on white")
#         print("1. View Seasonal Forecast")
#         print("2. Access Crop Advisories")
#         print("3. Search Historical Data")
#         print("4. Submit Query/Request Advisory")
#         print("5. Manage Profile")
#         print("6. Logout")

#         choice = input("Enter choice: ")

#         if choice == "1":
#             view_seasonal_forecast()
#         elif choice == "2":
#             access_crop_advisories()
#         elif choice == "3":
#             search_historical_data()
#         elif choice == "4":
#             submit_query()
#         elif choice == "5":
#             manage_profile()
#         elif choice == "6":
#             console.print("Logged out successfully", style="green")
#             break  # Exit the while loop to return to the main menu
#         else:
#             console.print("Invalid choice. Please try again.", style="red")

# # --- Farmer Authentication Functions ---

# def register_farmer():
#     """Registers a new farmer and saves to file."""
#     console.print("\n--- New Farmer Registration ---", style="bold")
#     username = input("Choose a username: ").strip()
#     password = input("Set a password: ").strip()
#     region = input("Enter your region: ").strip()

#     if not username or not password or not region:
#         console.print("⚠ All fields are required! Try again.", style="red")
#         return

#     farmers = read_data(FARMERS_FILE)
    
#     # Check if username already exists
#     for farmer in farmers:
#         if farmer.get("username") == username:
#             console.print("⚠ Username already exists! Try again.", style="red")
#             return

#     entry = {"username": username, "password": password, "region": region}
#     save_entry(FARMERS_FILE, entry)
#     console.print("✅ Registration successful!", style="green")

# def farmer_login():
#     """Logs in an existing farmer and shows the farmer menu."""
#     console.print("\n--- Farmer Login ---", style="bold")
#     username = input("Enter username: ").strip()
#     password = input("Enter password: ").strip()

#     farmers = read_data(FARMERS_FILE)
    
#     found = False
#     for farmer in farmers:
#         if farmer.get("username") == username and farmer.get("password") == password:
#             console.print(f"✅ Login successful! Welcome, {username}.", style="green")
#             found = True
#             farmer_login_menu(username)  # Enter the farmer menu
#             break
    
#     if not found:
#         console.print("❌ Invalid credentials. Please try again.", style="red")
# # Run farmer menu when file is executed directly
# if __name__ == "__main__":
#     console.print("\n--- Farmer Access Portal ---", style="bold underline")
#     print("1. Login as existing farmer")
#     print("2. Register new farmer")
#     print("3. Exit")

#     choice = input("Enter choice: ")

#     if choice == "1":
#         farmer_login()
#     elif choice == "2":
#         register_farmer()
#     else:
#         console.print("Exiting...", style="red")

# farmer_module.py
# All logic for the Farmer user role

import os
import pandas as pd
from tabulate import tabulate
from config import console, FARMERS_FILE, DATA_CSV_FOLDER, FORECAST_FILE, ADVISORY_FILE
from file_utils import read_data, save_entry, write_data
import json
from datetime import datetime

# Set pandas option
pd.set_option('display.max_rows', None)

# --- Farmer Menu Actions ---

def view_seasonal_forecast():
    """Displays all seasonal forecasts in a clean table, flattening mixed data."""
    console.print("\n=== Seasonal Forecasts ===", style="bold cyan")

    try:
        with open(FORECAST_FILE, "r") as f:
            forecasts = json.load(f)

        if not forecasts:
            console.print("⚠ No forecasts found.", style="yellow")
            return

        table_data = []
        for fc in forecasts:
            # --- Handle missing or malformed entries safely ---
            if not isinstance(fc, dict):
                continue

            season = str(fc.get("season", "N/A")).strip()
            region = str(fc.get("region", "N/A")).strip()

            # Dates can come as dict or string
            dates = fc.get("dates", {})
            if isinstance(dates, dict):
                start_date = str(dates.get("start", "N/A"))
                end_date = str(dates.get("end", "N/A"))
            elif isinstance(dates, str) and "->" in dates:
                start_date, end_date = map(str.strip, dates.split("->"))
            else:
                start_date = end_date = str(dates)
            date_range = f"{start_date} → {end_date}"

            # Weather details can be dict or plain strings
            weather = fc.get("weather_forecast", {})
            if isinstance(weather, dict):
                rainfall = str(weather.get("rainfall", "N/A"))
                temperature = str(weather.get("temperature", "N/A"))
                humidity = str(weather.get("humidity", "N/A"))
            else:
                rainfall = temperature = humidity = str(weather)

            # Crop suggestions and pest alerts
            crops = fc.get("crop_suggestions", [])
            pests = fc.get("pest_alert", [])

            # Convert lists or strings to uniform text
            if isinstance(crops, list):
                crops = ", ".join(crops)
            if isinstance(pests, list):
                pests = ", ".join(pests)

            crops = str(crops or "N/A")
            pests = str(pests or "N/A")

            # Add to table
            table_data.append([
                season, region, date_range,
                rainfall, temperature, humidity,
                crops, pests
            ])

        headers = [
            "Season", "Region", "Date Range",
            "Rainfall (mm)", "Temperature (°C)", "Humidity (%)",
            "Crop Suggestions", "Pest Alerts"
        ]

        print()
        print(tabulate(table_data, headers=headers, tablefmt="grid", showindex=True))

    except FileNotFoundError:
        console.print("⚠ forecasts.json file not found.", style="red")
    except json.JSONDecodeError:
        console.print("⚠ Error reading forecasts.json (invalid JSON).", style="red")
    except Exception as e:
        console.print(f"⚠ Unexpected error: {e}", style="red")

def access_crop_advisories():
    """Show crop advisories from ADVISORY_FILE; allow filtering by crop or season."""
    console.print("\n--- Crop Advisories ---", style="bold cyan")
    try:
        advisories = read_data(ADVISORY_FILE)
        if not advisories:
            console.print("No advisories available yet.", style="yellow")
            return

        # optional filter
        f_crop = input("Filter by crop (press Enter to skip): ").strip().lower()
        f_season = input("Filter by season (press Enter to skip): ").strip().lower()

        table = []
        for adv in advisories:
            crop = adv.get("Crop") or adv.get("crop") or adv.get("Crop Name") or ""
            season = adv.get("Season") or adv.get("season") or ""
            practices = adv.get("Practices") or adv.get("practices") or ""
            fertilizers = adv.get("Fertilizers") or adv.get("fertilizers") or ""
            precaution = adv.get("Precaution") or adv.get("precaution") or ""
            timestamp = adv.get("timestamp", "")

            if f_crop and f_crop not in crop.lower():
                continue
            if f_season and f_season not in season.lower():
                continue

            table.append([crop, season, practices, fertilizers, precaution, timestamp])

        if not table:
            console.print("No advisories match your filters.", style="yellow")
            return

        headers = ["Crop", "Season", "Practices", "Fertilizers", "Precaution", "Timestamp"]
        print(tabulate(table, headers=headers, tablefmt="fancy_grid", showindex=True))

    except Exception as e:
        console.print(f"Error loading advisories: {e}", style="red")

def search_historical_data():
    """Handles logic for Farmer Menu choice 3."""
    print("Loading 3...")

    if not os.path.exists(DATA_CSV_FOLDER):
        console.print(f"Error: Directory '{DATA_CSV_FOLDER}' not found.", style="red")
        return

    csv_files = [f for f in os.listdir(DATA_CSV_FOLDER) if f.endswith('.csv')]

    if not csv_files:
        console.print(f"No CSV files found in '{DATA_CSV_FOLDER}'.", style="yellow")
        return

    print("="*50)
    print("📂 Available CSV Files 📂".center(50))
    print("="*50)
    for i, file in enumerate(csv_files):
        print(f"{i + 1}. {file}")
    print("="*50)

    try:
        choice = int(input("Enter the number of the CSV file you want to display: "))
        if 1 <= choice <= len(csv_files):
            file_to_read = csv_files[choice - 1]
            file_path = os.path.join(DATA_CSV_FOLDER, file_to_read)
            df = pd.read_csv(file_path)

            print("\n" + "="*50)
            print(f"📄 Displaying: {file_to_read}".center(50))
            print(f"Shape: {df.shape[0]} rows x {df.shape[1]} columns".center(50))
            print("="*50)

            view_option = input("View (1) First & Last 5 rows or (2) Entire file? Enter 1 or 2: ").strip()

            if view_option == '1':
                print("\n--- First 5 Rows ---")
                print(tabulate(df.head(), headers='keys', tablefmt='fancy_grid', showindex=True))
                print("\n--- Last 5 Rows ---")
                print(tabulate(df.tail(), headers='keys', tablefmt='fancy_grid', showindex=True))
            elif view_option == '2':
                print("\n--- Entire File ---")
                print(tabulate(df, headers='keys', tablefmt='fancy_grid', showindex=True))
            else:
                print("❌ Invalid option. Showing first & last 5 rows by default.")
                print(tabulate(df.head(), headers='keys', tablefmt='fancy_grid', showindex=True))
                print(tabulate(df.tail(), headers='keys', tablefmt='fancy_grid', showindex=True))

            print("\n" + "="*50)
            print("✅ End of CSV Display".center(50))
            print("="*50)

        else:
            print("❌ Invalid choice.")
    except ValueError:
        print("❌ Please enter a valid number.")
    except FileNotFoundError:
        console.print(f"Error: File '{file_to_read}' not found.", style="red")
    except Exception as e:
        console.print(f"An unexpected error occurred: {e}", style="red")

def submit_query():
    """Allow a logged-in farmer to submit a query; saved to queries.json."""
    console.print("\n--- Submit Query / Request Advisory ---", style="bold")
    username = input("Enter your username (for submission): ").strip()
    if not username:
        console.print("Username required.", style="red")
        return

    crop = input("Crop concerned: ").strip()
    issue = input("Describe the issue or request advisory: ").strip()

    if not crop or not issue:
        console.print("Both crop and issue are required.", style="red")
        return

    entry = {
        "farmer_username": username,
        "crop": crop,
        "issue": issue,
        "status": "pending",
        "response": "",
        "timestamp": datetime.now().isoformat()
    }

    # save to queries.json
    queries_file = "queries.json"
    try:
        if os.path.exists(queries_file):
            with open(queries_file, "r", encoding="utf-8") as qf:
                data = json.load(qf) or []
        else:
            data = []
        data.append(entry)
        with open(queries_file, "w", encoding="utf-8") as qf:
            json.dump(data, qf, indent=4)
        console.print("Query submitted successfully. Admin will respond soon.", style="green")
    except Exception as e:
        console.print(f"Error saving query: {e}", style="red")

def manage_profile():
    """Allow farmer to update their profile details stored in FARMERS_FILE."""
    console.print("\n--- Manage Profile ---", style="bold")
    username = input("Enter your username to edit: ").strip()
    if not username:
        console.print("Username required.", style="red")
        return

    farmers = read_data(FARMERS_FILE)
    idx = None
    for i, f in enumerate(farmers):
        if f.get("username") == username:
            idx = i
            break

    if idx is None:
        console.print("User not found.", style="red")
        return

    farmer = farmers[idx]
    console.print(f"Editing profile for {username}", style="cyan")
    console.print("Press Enter to keep current value.", style="yellow")

    new_password = input(f"Password [{farmer.get('password','')}]: ") or farmer.get('password')
    new_region = input(f"Region [{farmer.get('region','')}]: ") or farmer.get('region')

    farmer['password'] = new_password
    farmer['region'] = new_region
    farmer['updated_on'] = datetime.now().isoformat()

    farmers[idx] = farmer
    write_data(FARMERS_FILE, farmers)
    console.print("Profile updated successfully.", style="green")

def farmer_login_menu(username):
    """Displays the farmer menu and handles user choice."""
    while True:
        console.print(f"\n--- Farmer Menu (Welcome {username}) ---", style="bold underline black on white")
        print("1. View Seasonal Forecast")
        print("2. Access Crop Advisories")
        print("3. Search Historical Data")
        print("4. Submit Query/Request Advisory")
        print("5. Manage Profile")
        print("6. Logout")

        choice = input("Enter choice: ")

        if choice == "1":
            view_seasonal_forecast()
        elif choice == "2":
            access_crop_advisories()
        elif choice == "3":
            search_historical_data()
        elif choice == "4":
            submit_query()
        elif choice == "5":
            manage_profile()
        elif choice == "6":
            console.print("Logged out successfully", style="green")
            break  # Exit the while loop to return to the main menu
        else:
            console.print("Invalid choice. Please try again.", style="red")

# --- Farmer Authentication Functions ---

def register_farmer():
    """Registers a new farmer and saves to file."""
    console.print("\n--- New Farmer Registration ---", style="bold")
    username = input("Choose a username: ").strip()
    password = input("Set a password: ").strip()
    region = input("Enter your region: ").strip()

    if not username or not password or not region:
        console.print("⚠ All fields are required! Try again.", style="red")
        return

    farmers = read_data(FARMERS_FILE)
    
    # Check if username already exists
    for farmer in farmers:
        if farmer.get("username") == username:
            console.print("⚠ Username already exists! Try again.", style="red")
            return

    entry = {"username": username, "password": password, "region": region}
    save_entry(FARMERS_FILE, entry)
    console.print("✅ Registration successful!", style="green")

def farmer_login():
    """Logs in an existing farmer and shows the farmer menu."""
    console.print("\n--- Farmer Login ---", style="bold")
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()

    farmers = read_data(FARMERS_FILE)
    
    found = False
    for farmer in farmers:
        if farmer.get("username") == username and farmer.get("password") == password:
            console.print(f"✅ Login successful! Welcome, {username}.", style="green")
            found = True
            farmer_login_menu(username)  # Enter the farmer menu
            break
    
    if not found:
        console.print("❌ Invalid credentials. Please try again.", style="red")
# Run farmer menu when file is executed directly
if __name__ == "__main__":
    console.print("\n--- Farmer Access Portal ---", style="bold underline")
    print("1. Login as existing farmer")
    print("2. Register new farmer")
    print("3. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        farmer_login()
    elif choice == "2":
        register_farmer()
    else:
        console.print("Exiting...", style="red")

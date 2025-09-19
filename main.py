import time
from rich.console import Console
console = Console()
import json
import os
from datetime import datetime   
from rich.progress import track
import pandas as pd
pd.set_option('display.max_rows', None)
from tabulate import tabulate
#-----------------------------Read list from file---------------------------

def read_data(file):
    if os.path.exists(file):
        with open(file, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

#------------------------Write list to file------------------------------   

def write_data(file, data):        
    with open(file, "w") as f:
        json.dump(data, f, indent=2)

#-----------------------Save list back to file------------------------------

def save_entry(file, entry):
    data = read_data(file)
    data.append(entry)
    write_data(file, data)
    print("✅ Saved:")
    time.sleep(1)

#-----------------------------Admin login-----------------------------------------

def admin_login():
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
            for i in track(range(1,4), description="Processing"):
                time.sleep(0.25)
            global DATA_FILE  
            DATA_FILE = "forecasts.json"  
            season = input("Enter season: ")
            region = input("Enter region: ")
            start_date = input("Enter start date: ")
            end_date=input("Enter end date: ")
            rainfall=input("Enter rainfall(in mm): ")
            temperature=input("Enter temperature(in °C): ")
            humidity=input("Enter humidity(in %): ")
            crop_suggestions=input("Enter crop suggestions (comma-separated): ")
            pest_alert=input("Enter pest alert (comma-separated): ")

            entry = {
                "season": season,
                "region": region,
                "dates": {"start": start_date, "end": end_date},
                "weather_forecast": {
                    "rainfall": rainfall, "temperature": temperature, "humidity": humidity
                },
                "crop_suggestions": list(crop_suggestions.split(",")),
                "pest_alert": list(pest_alert.split(",")),
                "timestamp": datetime.now().isoformat()
            }
            save_entry(DATA_FILE, entry)  
            console.print("Returning to Admin Menu...", style="green")
            time.sleep(1)

        elif choice == "2":
            for i in track(range(1,4), description="Processing"):
                time.sleep(0.25)
            print("Loading 2")
            time.sleep(1)

        elif choice == "3":
            DATA_FILE = "advisory.json" 
            Crop=input("Enter Crop Name: ") 
            Season=input("Enter Season: ")
            Practices=input("Enter Appropriate Practices: ")
            Fertilizers=input("Enter Fertilizers Name: ")
            Precausion=input("Enter Precaution to be taken: ")

            entry = {
                "Crop":Crop,
                "Season":Season,
                "Practices":Practices,
                "Fertilizers":Fertilizers,
                "Precausion":Precausion,
                "timestamp": datetime.now().isoformat()
            }
            save_entry(DATA_FILE, entry)

        elif choice == "4":
            for i in track(range(1,4), description="Processing"):
                time.sleep(0.25)
            print("Loading 4")
            time.sleep(1)

        elif choice == "5":
            for i in track(range(1,4), description="Processing"):
                time.sleep(0.25)
            print("Loading 5")
            time.sleep(1)

        elif choice == "6":
            for i in track(range(1,4), description="Processing"):
                time.sleep(0.25)
            print("Loading 6")
            time.sleep(1)

        elif choice == "7":
            console.print("Logging out...", style="red")
            break   
        else:
            print("Invalid choice.")

#---------------------------Farmer menu after login-------------------

FARMERS_FILE = "farmers.json" 
def farmer_login_menu(username):
    console.print(f"\n--- Farmer Menu (Welcome {username}) ---", style="bold underline black on white")
    print("1. View Seasonal Forecast")
    print("2. Access Crop Advisories")
    print("3. Search Historical Data")
    print("4. Submit Query/Request Advisory")
    print("5. Manage Profile")
    print("6. Logout")

    choice = input("Enter choice: ")

    if choice == "1":
        print("Loading 1")
    elif choice == "2":
        print("Loading 2")
    elif choice == "3":
        print("Loading 3")  # pip install tabulate
        

        csv_folder = "data_csv"
        csv_files = [f for f in os.listdir(csv_folder) if f.endswith('.csv')]

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
                df = pd.read_csv(os.path.join(csv_folder, file_to_read))

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

    elif choice == "4":
        print("Loading 4")
    elif choice == "5":
        print("Loading 5")
    elif choice == "6":
        console.print("Logged out successfully", style="red")
    else:
        print("Nothing updated")

#---------------------------Farmer registration & login-------------------

def register_farmer():
    username = input("Choose a username: ").strip()
    password = input("Set a password: ").strip()
    region = input("Enter your region: ").strip()

    farmers = read_data(FARMERS_FILE)
    
    for farmer in farmers:
        if farmer.get("username") == username:
            console.print("⚠ Username already exists! Try again.", style="red")
            return

    entry = {"username": username, "password": password, "region": region}
    save_entry(FARMERS_FILE, entry)
    console.print("✅ Registration successful!", style="green")

def farmer_login():
    
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()

    farmers = read_data(FARMERS_FILE)  


    for farmer in farmers:
        if farmer.get("username") == username and farmer.get("password") == password:
            console.print("✅ Login successful!", style="green")
            farmer_login_menu(username)
            return

    else:
        console.print("Invalid credentials", style="red")
    return


#---------------------------Main Menu-----------------------------------

def main_menu():
    console.print("\n== Seasonal Forecast & Agriculture Advisory System ===", style="bold underline black on white")
    print("1. Admin Login")
    print("2. Farmer Login")
    print("3. Register as New Farmer")
    print("4. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        admin_login()
    elif choice == "2":
        farmer_login()
    elif choice == "3":
        register_farmer()
    elif choice == "4":
        console.print("Closed successfully.", style="red")
        exit()
    else:
        console.print("Invalid choice. Try again.", style="red")

#--------------------Coming back to main menu after every logout----------------------------

while True:
    main_menu()
    again = input("Return to main menu? (y/n): ")
    if again.lower() != "y":
        console.print("Exiting application...", style="red")
        break
    
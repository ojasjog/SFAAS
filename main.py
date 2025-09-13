import time
from rich.console import Console
console = Console()
import json
import os
from datetime import datetime   

#-----------------------------Read list from file---------------------------

def read_data():

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                    return []
    return []




#------------------------Write list to file------------------------------   

def write_data(data):
            
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

#-----------------------Save list back to file------------------------------

def save_entry(entry):


    data = read_data()
    data.append(entry)
    write_data(data)
    print("✅ Saved:")

#-----------------------------Admin login-----------------------------------------

def admin_login():
    
    print("\n--- Admin Menu ---")
    print("1. Add Seasonal Forecast")
    print("2. Update/Delete Forecast")
    print("3. Manage Forecast")
    print("4. Upload Bulk Forecast Data")
    print("5. Generate Reports")
    print("6. Manage Farmer Queries")
    print("7. Logout")

    


#---------------------------Farmer login-----------------------------------
def farmer_login():
    print("\n--- Farmer Menu ---")
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
        print("Loading 3")
    elif choice == "4":
        print("Loading 4")
    elif choice == "5":
        print("Loading 5")
    elif choice == "6":
        print("Logging out...")
    else:
        print("Nothing updated")

#---------------------------Main Menu-----------------------------------


print("\n== Seasonal Forecast & Agriculture Advisory System ===")
print("1. Admin Login")
print("2. Farmer Login")
print("3. Register as New Farmer")
print("4. Exit")

choice = input("Enter choice: ")

if choice == "1":
    for i in range(1, 4):
        console.log(f"Loading data...{i}")
        time.sleep(0.25)
    admin_login()
    choice= input("Enter choice: ")

    DATA_FILE = "forecasts.json"

    if choice == "1":  
        season = input("Enter season: ")
        region = input("Enter region: ")
        start_date = input("Enter start date: ")
        end_date=input("Enter end date: ")
        rainfall=input("Enter rainfall(in mm): ")
        temperature=input("Enter temperature(in °C): ")
        humidity=input("Enter humidity(in %): ")
        crop_suggestions=input("Enter crop suggestions: ")
        pest_alert=input("Enter pest alert: ")
        advisory_notes=input("Enter advisory notes: ")


        entry = {
                "season": season,
                "region": region,
                "dates": {"start": start_date, 
                          "end": end_date},
                "weather_forecast": {
                    "rainfall": rainfall, "temperature": temperature, "humidity": humidity
                },
                "crop_suggestions": list(crop_suggestions.split(",")),
                "pest_alert": list(pest_alert.split(",")),
                "advisory_notes": advisory_notes,
                "timestamp": datetime.now().isoformat()
            }
        save_entry(entry)   
            
               
    elif choice == "2":
        print("Loading 2")
    elif choice == "3":
        print("Loading 3")
    elif choice == "4":
        print("Loading 4")
    elif choice == "5":
        print("Loading 5")
    elif choice == "6":
        print("Loading 6")
    elif choice == "7":
        print("Logging out...")
    else:
        print("Invalid choice.")



elif choice == "2":
    for i in range(1, 4):
        console.log(f"Loading data...{i}")
        time.sleep(0.25)
    farmer_login()

elif choice == "3":
    for i in range(1, 4):
        console.log(f"Loading data...{i}")
        time.sleep(0.25)
    print("Registration")

elif choice == "4":
    print("Closed succesfully.")

else:
    print("Invalid choice. Try again.")


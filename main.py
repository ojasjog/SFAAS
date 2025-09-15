import time
from rich.console import Console
console = Console()
import json
import os
from datetime import datetime   
from rich.progress import track

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
                    "dates": {"start": start_date, 
                              "end": end_date},
                    "weather_forecast": {
                        "rainfall": rainfall, "temperature": temperature, "humidity": humidity
                    },
                    "crop_suggestions": list(crop_suggestions.split(",")),
                    "pest_alert": list(pest_alert.split(",")),
                    
                    "timestamp": datetime.now().isoformat()
                }
            save_entry(entry)  
            console.print("Returning to Admin Menu...", style="green")
            time.sleep(1)

        elif choice == "2":
            for i in track(range(1,4), description="Processing"):
                print
                time.sleep(0.25)
            print("Loading 2")
            time.sleep(1)
            print("Returning to Admin Menu...")
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
            save_entry(entry)


          
        elif choice == "4":
            for i in track(range(1,4), description="Processing"):
                print
                time.sleep(0.25)
            print("Loading 4")
            time.sleep(1)
            print("Returning to Admin Menu...")
            time.sleep(1)


        elif choice == "5":
            for i in track(range(1,4), description="Processing"):
                print
                time.sleep(0.25)

            print("Loading 5")
            time.sleep(1)
            print("Returning to Admin Menu...")
            time.sleep(1)


        elif choice == "6":
            for i in track(range(1,4), description="Processing"):
                print
                time.sleep(0.25)
            print("Loading 6")
            time.sleep(1)
            print("Returning to Admin Menu...")
            time.sleep(1)


        elif choice == "7":
            console.print("Logging out...", style="red")
            break   
        else:
            print("Invalid choice.")

#---------------------------Farmer login-----------------------------------
def farmer_login():
    console.print("\n--- Farmer Menu ---", style="bold underline black on white")
    print("1. View Seasonal Forecast")
    print("2. Access Crop Advisories")
    print("3. Search Historical Data")
    print("4. Submit Query/Request Advisory")
    print("5. Manage Profile")
    print("6. Logout")

    choice = input("Enter choice: ")

    if choice == "1":
        for i in track(range(1,4), description="Processing"):
            print
            time.sleep(0.25)
        print("Loading 1")


    elif choice == "2":
        for i in track(range(1,4), description="Processing"):
            print
            time.sleep(0.25)
        print("Loading 2")


    elif choice == "3":
        for i in track(range(1,4), description="Searching"):
            print
            time.sleep(0.25)
        print("Loading 3")


    elif choice == "4":
        print("Loading 4")


    elif choice == "5":
        print("Loading 5")


    elif choice == "6":
        for i in track(range(1,4), description="Logging out"):
            print
            time.sleep(0.25)
        console.print("Logged out succesfully", style="red")

    else:
        print("Nothing updated")

#---------------------------Main Menu-----------------------------------

def main_menu():

    console.print("\n== Seasonal Forecast & Agriculture Advisory System ===", style="bold underline black on white")
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
        console.print("Closed succesfully.", style="red")
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
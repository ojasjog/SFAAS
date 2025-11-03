# # admin_module.py
# # All logic for the Admin user role

# import time
# from datetime import datetime
# from rich.progress import track
# from config import console, FORECAST_FILE, ADVISORY_FILE
# from file_utils import save_entry

# # --- Admin Menu Actions ---

# def add_seasonal_forecast():
#     """Handles logic for Admin Menu choice 1."""
#     for i in track(range(1,4), description="Processing"):
#         time.sleep(0.25)
    
#     console.print("\n--- Add New Seasonal Forecast ---", style="bold")
#     season = input("Enter season: ")
#     region = input("Enter region: ")
#     start_date = input("Enter start date (YYYY-MM-DD): ")
#     end_date = input("Enter end date (YYYY-MM-DD): ")
#     rainfall = input("Enter rainfall (in mm): ")
#     temperature = input("Enter temperature (in °C): ")
#     humidity = input("Enter humidity (in %): ")
#     crop_suggestions = input("Enter crop suggestions (comma-separated): ")
#     pest_alert = input("Enter pest alert (comma-separated): ")

#     entry = {
#         "season": season,
#         "region": region,
#         "dates": {"start": start_date, "end": end_date},
#         "weather_forecast": {
#             "rainfall": rainfall, "temperature": temperature, "humidity": humidity
#         },
#         # Use .strip() to clean up user input
#         "crop_suggestions": [c.strip() for c in crop_suggestions.split(",")],
#         "pest_alert": [p.strip() for p in pest_alert.split(",")],
#         "timestamp": datetime.now().isoformat()
#     }
    
#     save_entry(FORECAST_FILE, entry)
#     console.print("Returning to Admin Menu...", style="green")
#     time.sleep(1)

# def manage_crop_advisories():
#     """Handles logic for Admin Menu choice 3."""
#     console.print("\n--- Manage Crop Advisories ---", style="bold")
#     Crop = input("Enter Crop Name: ")
#     Season = input("Enter Season: ")
#     Practices = input("Enter Appropriate Practices: ")
#     Fertilizers = input("Enter Fertilizers Name: ")
#     Precaution = input("Enter Precaution to be taken: ") # Corrected typo

#     entry = {
#         "Crop": Crop,
#         "Season": Season,
#         "Practices": Practices,
#         "Fertilizers": Fertilizers,
#         "Precaution": Precaution,
#         "timestamp": datetime.now().isoformat()
#     }
    
#     save_entry(ADVISORY_FILE, entry)
#     console.print("Advisory saved. Returning to Admin Menu...", style="green")
#     time.sleep(1)

# # --- Placeholder functions for other admin options ---

# def update_delete_forecast():
#     for i in track(range(1,4), description="Processing"):
#         time.sleep(0.25)
#     print("Loading 2... (Functionality not yet implemented)")
#     time.sleep(1)

# def upload_bulk_data():
#     for i in track(range(1,4), description="Processing"):
#         time.sleep(0.25)
#     print("Loading 4... (Functionality not yet implemented)")
#     time.sleep(1)

# def generate_reports():
#     for i in track(range(1,4), description="Processing"):
#         time.sleep(0.25)
#     print("Loading 5... (Functionality not yet implemented)")
#     time.sleep(1)

# def manage_farmer_queries():
#     for i in track(range(1,4), description="Processing"):
#         time.sleep(0.25)
#     print("Loading 6... (Functionality not yet implemented)")
#     time.sleep(1)

# # --- Main Admin Menu Loop ---

# def admin_login():
#     """Displays the admin menu and handles user choice."""
#     while True:
#         console.print("\n--- Admin Menu ---", style="bold underline black on white")
#         print("1. Add Seasonal Forecast")
#         print("2. Update/Delete Forecast")
#         print("3. Manage Crop Advisories")
#         print("4. Upload Bulk Forecast Data")
#         print("5. Generate Reports")
#         print("6. Manage Farmer Queries")
#         print("7. Logout")

#         choice = input("Enter choice: ")

#         if choice == "1":
#             add_seasonal_forecast()
#         elif choice == "2":
#             update_delete_forecast()
#         elif choice == "3":
#             manage_crop_advisories()
#         elif choice == "4":
#             upload_bulk_data()
#         elif choice == "5":
#             generate_reports()
#         elif choice == "6":
#             manage_farmer_queries()
#         elif choice == "7":
#             console.print("Logging out...", style="red")
#             break  # Exit the while loop to return to the main menu
#         else:
#             console.print("Invalid choice.", style="red")
# # Run admin menu when file is executed directly
# if __name__ == "__main__":
#     admin_login()

# admin_module.py
# All logic for the Admin user role

# import time
# from datetime import datetime
# from rich.progress import track
# from config import console, FORECAST_FILE, ADVISORY_FILE, DATA_CSV_FOLDER
# from file_utils import save_entry, read_data, write_data
# import csv
# import os
# import json
# from collections import Counter

# # --- Admin Menu Actions ---

# def add_seasonal_forecast():
#     """Handles logic for Admin Menu choice 1."""
#     for i in track(range(1,4), description="Processing"):
#         time.sleep(0.25)
    
#     console.print("\n--- Add New Seasonal Forecast ---", style="bold")
#     season = input("Enter season: ")
#     region = input("Enter region: ")
#     start_date = input("Enter start date (YYYY-MM-DD): ")
#     end_date = input("Enter end date (YYYY-MM-DD): ")
#     rainfall = input("Enter rainfall (in mm): ")
#     temperature = input("Enter temperature (in °C): ")
#     humidity = input("Enter humidity (in %): ")
#     crop_suggestions = input("Enter crop suggestions (comma-separated): ")
#     pest_alert = input("Enter pest alert (comma-separated): ")

#     entry = {
#         "season": season,
#         "region": region,
#         "dates": {"start": start_date, "end": end_date},
#         "weather_forecast": {
#             "rainfall": rainfall, "temperature": temperature, "humidity": humidity
#         },
#         # Use .strip() to clean up user input
#         "crop_suggestions": [c.strip() for c in crop_suggestions.split(",")] if crop_suggestions else [],
#         "pest_alert": [p.strip() for p in pest_alert.split(",")] if pest_alert else [],
#         "timestamp": datetime.now().isoformat()
#     }
    
#     save_entry(FORECAST_FILE, entry)
#     console.print("Returning to Admin Menu...", style="green")
#     time.sleep(1)

# def update_delete_forecast():
#     """Allow admin to update or delete forecasts stored in FORECAST_FILE."""
#     for i in track(range(1,3), description="Loading forecasts"):
#         time.sleep(0.1)

#     forecasts = read_data(FORECAST_FILE)

#     if not forecasts:
#         console.print("⚠ No forecasts to manage.", style="yellow")
#         return

#     console.print("\n--- Update/Delete Forecast ---", style="bold")
#     # show list
#     for idx, fc in enumerate(forecasts, start=1):
#         season = fc.get("season", "N/A")
#         region = fc.get("region", "N/A")
#         dates = fc.get("dates", {})
#         if isinstance(dates, dict):
#             dr = f"{dates.get('start','N/A')} → {dates.get('end','N/A')}"
#         else:
#             dr = str(dates)
#         console.print(f"{idx}. {season} | {region} | {dr}")

#     try:
#         choice = int(input("Enter forecast number to manage (0 to cancel): "))
#     except ValueError:
#         console.print("Invalid input.", style="red")
#         return

#     if choice == 0:
#         console.print("Cancelled.", style="yellow")
#         return
#     if choice < 1 or choice > len(forecasts):
#         console.print("Invalid choice.", style="red")
#         return

#     selected = forecasts[choice - 1]
#     console.print(f"\nSelected: {selected}", style="cyan")
#     action = input("Enter 'u' to update, 'd' to delete, anything else to cancel: ").strip().lower()

#     if action == 'd':
#         del forecasts[choice - 1]
#         write_data(FORECAST_FILE, forecasts)
#         console.print("Forecast deleted.", style="green")
#         return

#     if action == 'u':
#         console.print("Press Enter to keep current value.", style="yellow")
#         season = input(f"Season [{selected.get('season','')}]: ") or selected.get('season')
#         region = input(f"Region [{selected.get('region','')}]: ") or selected.get('region')

#         dates = selected.get("dates", {})
#         start_date = input(f"Start date [{dates.get('start','') if isinstance(dates, dict) else dates}]: ")
#         end_date = input(f"End date [{dates.get('end','') if isinstance(dates, dict) else dates}]: ")

#         weather = selected.get("weather_forecast", {})
#         rainfall = input(f"Rainfall [{weather.get('rainfall','')}]: ") or weather.get('rainfall')
#         temperature = input(f"Temperature [{weather.get('temperature','')}]: ") or weather.get('temperature')
#         humidity = input(f"Humidity [{weather.get('humidity','')}]: ") or weather.get('humidity')

#         crop_suggestions = input("Crop suggestions (comma-separated) or Enter to keep: ")
#         pest_alert = input("Pest alerts (comma-separated) or Enter to keep: ")

#         # Update entry
#         selected['season'] = season
#         selected['region'] = region
#         selected['dates'] = {"start": start_date or dates.get('start',''), "end": end_date or dates.get('end','')} if isinstance(dates, dict) else (start_date or end_date or dates)
#         selected['weather_forecast'] = {"rainfall": rainfall, "temperature": temperature, "humidity": humidity}
#         if crop_suggestions:
#             selected['crop_suggestions'] = [c.strip() for c in crop_suggestions.split(",")]
#         if pest_alert:
#             selected['pest_alert'] = [p.strip() for p in pest_alert.split(",")]
#         selected['timestamp'] = datetime.now().isoformat()

#         forecasts[choice - 1] = selected
#         write_data(FORECAST_FILE, forecasts)
#         console.print("Forecast updated.", style="green")
#         return

#     console.print("No changes made.", style="yellow")

# def manage_crop_advisories():
#     """Handles logic for Admin Menu choice 3."""
#     console.print("\n--- Manage Crop Advisories ---", style="bold")
#     Crop = input("Enter Crop Name: ")
#     Season = input("Enter Season: ")
#     Practices = input("Enter Appropriate Practices: ")
#     Fertilizers = input("Enter Fertilizers Name: ")
#     Precaution = input("Enter Precaution to be taken: ") # Corrected typo

#     entry = {
#         "Crop": Crop,
#         "Season": Season,
#         "Practices": Practices,
#         "Fertilizers": Fertilizers,
#         "Precaution": Precaution,
#         "timestamp": datetime.now().isoformat()
#     }
    
#     save_entry(ADVISORY_FILE, entry)
#     console.print("Advisory saved. Returning to Admin Menu...", style="green")
#     time.sleep(1)

# def upload_bulk_data():
#     """
#     Upload bulk forecast data from a CSV located under DATA_CSV_FOLDER.
#     Expected CSV columns (best-effort): season,region,start_date,end_date,rainfall,temperature,humidity,crop_suggestions,pest_alert
#     """
#     for i in track(range(1,3), description="Preparing bulk upload"):
#         time.sleep(0.1)

#     if not os.path.isdir(DATA_CSV_FOLDER):
#         console.print(f"⚠ Directory '{DATA_CSV_FOLDER}' not found. Create it and put CSV files there.", style="red")
#         return

#     csv_files = [f for f in os.listdir(DATA_CSV_FOLDER) if f.lower().endswith('.csv')]

#     if not csv_files:
#         console.print("⚠ No CSV files found in data folder.", style="yellow")
#         return

#     console.print("\nAvailable CSV files:", style="bold")
#     for i, f in enumerate(csv_files, start=1):
#         console.print(f"{i}. {f}")

#     try:
#         choice = int(input("Enter file number to import (0 to cancel): "))
#     except ValueError:
#         console.print("Invalid input.", style="red")
#         return

#     if choice == 0:
#         console.print("Cancelled.", style="yellow")
#         return

#     if not (1 <= choice <= len(csv_files)):
#         console.print("Invalid choice.", style="red")
#         return

#     csv_path = os.path.join(DATA_CSV_FOLDER, csv_files[choice - 1])
#     inserted = 0
#     try:
#         with open(csv_path, newline='', encoding='utf-8') as csvfile:
#             reader = csv.DictReader(csvfile)
#             for row in reader:
#                 # Map known columns, fallback to generic
#                 season = row.get('season') or row.get('Season') or row.get('SEASON') or row.get('season_name') or ''
#                 region = row.get('region') or row.get('Region') or ''
#                 start_date = row.get('start_date') or row.get('start') or ''
#                 end_date = row.get('end_date') or row.get('end') or ''
#                 rainfall = row.get('rainfall') or row.get('Rainfall') or ''
#                 temperature = row.get('temperature') or row.get('Temperature') or ''
#                 humidity = row.get('humidity') or row.get('Humidity') or ''
#                 crops = row.get('crop_suggestions') or row.get('crops') or ''
#                 pests = row.get('pest_alert') or row.get('pests') or ''

#                 entry = {
#                     "season": season,
#                     "region": region,
#                     "dates": {"start": start_date, "end": end_date},
#                     "weather_forecast": {"rainfall": rainfall, "temperature": temperature, "humidity": humidity},
#                     "crop_suggestions": [c.strip() for c in crops.split(',')] if crops else [],
#                     "pest_alert": [p.strip() for p in pests.split(',')] if pests else [],
#                     "timestamp": datetime.now().isoformat()
#                 }
#                 save_entry(FORECAST_FILE, entry)
#                 inserted += 1
#     except Exception as e:
#         console.print(f"Error reading CSV: {e}", style="red")
#         return

#     console.print(f"Imported {inserted} forecast rows from {csv_files[choice - 1]}.", style="green")

# def generate_reports():
#     """
#     Generate simple summary reports from forecasts.json:
#       - number of forecasts
#       - forecasts per region
#       - average rainfall (attempt numeric conversion)
#     """
#     for i in track(range(1,3), description="Generating report"):
#         time.sleep(0.1)

#     forecasts = read_data(FORECAST_FILE)
#     if not forecasts:
#         console.print("No forecasts available to generate reports.", style="yellow")
#         return

#     total = len(forecasts)
#     regions = [f.get('region', 'Unknown') for f in forecasts]
#     region_counts = Counter(regions)

#     # collect rainfall values as floats if possible
#     rain_vals = []
#     for f in forecasts:
#         try:
#             wf = f.get('weather_forecast', {})
#             r = wf.get('rainfall', None) if isinstance(wf, dict) else None
#             if r is None:
#                 continue
#             # allow strings like "12.5" or "12 mm"
#             if isinstance(r, (int, float)):
#                 rain_vals.append(float(r))
#             elif isinstance(r, str):
#                 rv = ''.join(ch for ch in r if (ch.isdigit() or ch == '.' or ch == '-'))
#                 if rv:
#                     rain_vals.append(float(rv))
#         except Exception:
#             continue

#     avg_rain = (sum(rain_vals) / len(rain_vals)) if rain_vals else None

#     console.print("\n--- Forecast Summary Report ---", style="bold underline")
#     console.print(f"Total forecasts: {total}")
#     console.print("Forecasts per region:")
#     for reg, cnt in region_counts.most_common():
#         console.print(f"  {reg}: {cnt}")

#     if avg_rain is not None:
#         console.print(f"Average rainfall (mm): {avg_rain:.2f}")
#     else:
#         console.print("Average rainfall: N/A (no numeric data)")

#     # Optional: write this report to a file
#     now = datetime.now().strftime("%Y%m%d_%H%M%S")
#     report = {
#         "generated_on": datetime.now().isoformat(),
#         "total_forecasts": total,
#         "per_region": dict(region_counts),
#         "average_rainfall_mm": avg_rain
#     }
#     report_file = f"reports_{now}.json"
#     try:
#         with open(report_file, "w", encoding="utf-8") as rf:
#             json.dump(report, rf, indent=4)
#         console.print(f"Saved summary report to {report_file}", style="green")
#     except Exception as e:
#         console.print(f"Could not save report file: {e}", style="red")

# def manage_farmer_queries():
#     """
#     Admin can view pending queries from farmers and respond (approve/reject/respond text).
#     Queries are stored in 'queries.json' with fields:
#       { "farmer_username": ..., "crop":..., "issue":..., "status": "pending"/"responded"/"approved"/"rejected", "response":..., "timestamp":... }
#     """
#     queries_file = "queries.json"
#     for i in track(range(1,3), description="Loading queries"):
#         time.sleep(0.1)

#     queries = []
#     if os.path.exists(queries_file):
#         try:
#             with open(queries_file, "r", encoding="utf-8") as qf:
#                 queries = json.load(qf) or []
#         except Exception:
#             queries = []

#     pending = [q for q in queries if q.get("status", "pending") in ("pending", "open")]

#     if not queries:
#         console.print("No queries found.", style="yellow")
#         return

#     console.print("\n--- Farmer Queries ---", style="bold")
#     for idx, q in enumerate(queries, start=1):
#         user = q.get("farmer_username", "N/A")
#         crop = q.get("crop", "N/A")
#         issue = q.get("issue", "N/A")
#         status = q.get("status", "N/A")
#         console.print(f"{idx}. [{status}] {user} - {crop} -> {issue}")

#     try:
#         choice = int(input("Enter query number to respond (0 to cancel): "))
#     except ValueError:
#         console.print("Invalid input.", style="red")
#         return

#     if choice == 0:
#         console.print("Canceled.", style="yellow")
#         return

#     if not (1 <= choice <= len(queries)):
#         console.print("Invalid choice.", style="red")
#         return

#     q = queries[choice - 1]
#     console.print(f"Selected query: {q}", style="cyan")
#     response = input("Enter response text (or type 'approve' or 'reject'): ").strip()
#     if not response:
#         console.print("No response entered. Canceling.", style="yellow")
#         return

#     if response.lower() == 'approve':
#         q['status'] = 'approved'
#         q['response'] = 'Approved by admin.'
#     elif response.lower() == 'reject':
#         q['status'] = 'rejected'
#         q['response'] = 'Rejected by admin.'
#     else:
#         q['status'] = 'responded'
#         q['response'] = response

#     q['responded_on'] = datetime.now().isoformat()
#     # save back
#     try:
#         with open(queries_file, "w", encoding="utf-8") as qf:
#             json.dump(queries, qf, indent=4)
#         console.print("Response saved.", style="green")
#     except Exception as e:
#         console.print(f"Error saving response: {e}", style="red")

# # --- Main Admin Menu Loop ---

# def admin_login():
#     """Displays the admin menu and handles user choice."""
#     while True:
#         console.print("\n--- Admin Menu ---", style="bold underline black on white")
#         print("1. Add Seasonal Forecast")
#         print("2. Update/Delete Forecast")
#         print("3. Manage Crop Advisories")
#         print("4. Upload Bulk Forecast Data")
#         print("5. Generate Reports")
#         print("6. Manage Farmer Queries")
#         print("7. Logout")

#         choice = input("Enter choice: ")

#         if choice == "1":
#             add_seasonal_forecast()
#         elif choice == "2":
#             update_delete_forecast()
#         elif choice == "3":
#             manage_crop_advisories()
#         elif choice == "4":
#             upload_bulk_data()
#         elif choice == "5":
#             generate_reports()
#         elif choice == "6":
#             manage_farmer_queries()
#         elif choice == "7":
#             console.print("Logging out...", style="red")
#             break  # Exit the while loop to return to the main menu
#         else:
#             console.print("Invalid choice.", style="red")
# # Run admin menu when file is executed directly
# if __name__ == "__main__":
#     admin_login()

# admin_module.py

import os, csv, json, time
from datetime import datetime
from collections import Counter
from rich.progress import track
from config import console, FORECAST_FILE, ADVISORY_FILE, DATA_CSV_FOLDER
from file_utils import save_entry, read_data, write_data

def add_seasonal_forecast():
    for _ in track(range(3), description="Processing"): time.sleep(0.2)
    console.print("\n--- Add New Seasonal Forecast ---", style="bold")
    entry = {
        "season": input("Season: "),
        "region": input("Region: "),
        "dates": {
            "start": input("Start Date (YYYY-MM-DD): "),
            "end": input("End Date (YYYY-MM-DD): ")
        },
        "weather_forecast": {
            "rainfall": input("Rainfall (mm): "),
            "temperature": input("Temperature (°C): "),
            "humidity": input("Humidity (%): ")
        },
        "crop_suggestions": [c.strip() for c in input("Crop suggestions: ").split(",")],
        "pest_alert": [p.strip() for p in input("Pest alerts: ").split(",")],
        "timestamp": datetime.now().isoformat()
    }
    save_entry(FORECAST_FILE, entry)

def update_delete_forecast():
    forecasts = read_data(FORECAST_FILE)
    if not forecasts:
        console.print("⚠ No forecasts found.", style="yellow")
        return
    for i, f in enumerate(forecasts, 1):
        console.print(f"{i}. {f.get('season','')} | {f.get('region','')}")
    try:
        idx = int(input("Enter number to edit/delete (0 cancel): "))
        if idx == 0 or idx > len(forecasts): return
    except: return
    action = input("(U)pdate / (D)elete? ").lower()
    if action == 'd':
        forecasts.pop(idx - 1)
    elif action == 'u':
        f = forecasts[idx - 1]
        f['season'] = input(f"Season [{f['season']}]: ") or f['season']
        f['region'] = input(f"Region [{f['region']}]: ") or f['region']
    write_data(FORECAST_FILE, forecasts)
    console.print("✔ Done.", style="green")

def manage_crop_advisories():
    console.print("\n--- Add Crop Advisory ---", style="bold")
    entry = {
        "Crop": input("Crop: "),
        "Season": input("Season: "),
        "Practices": input("Practices: "),
        "Fertilizers": input("Fertilizers: "),
        "Precaution": input("Precaution: "),
        "timestamp": datetime.now().isoformat()
    }
    save_entry(ADVISORY_FILE, entry)

def upload_bulk_data():
    if not os.path.isdir(DATA_CSV_FOLDER):
        console.print("⚠ No data_csv folder.", style="red")
        return
    files = [f for f in os.listdir(DATA_CSV_FOLDER) if f.endswith(".csv")]
    if not files:
        console.print("⚠ No CSVs found.", style="yellow")
        return
    for i, f in enumerate(files, 1): print(f"{i}. {f}")
    idx = int(input("File number: ")) - 1
    if idx < 0 or idx >= len(files): return
    path = os.path.join(DATA_CSV_FOLDER, files[idx])
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            entry = {
                "season": row.get("season",""),
                "region": row.get("region",""),
                "dates": {"start": row.get("start_date",""), "end": row.get("end_date","")},
                "weather_forecast": {"rainfall": row.get("rainfall",""), "temperature": row.get("temperature",""), "humidity": row.get("humidity","")},
                "crop_suggestions": [c.strip() for c in row.get("crop_suggestions","").split(",")],
                "pest_alert": [p.strip() for p in row.get("pest_alert","").split(",")],
                "timestamp": datetime.now().isoformat()
            }
            save_entry(FORECAST_FILE, entry)
    console.print("✅ Bulk upload done!", style="green")

def generate_reports():
    forecasts = read_data(FORECAST_FILE)
    if not forecasts:
        console.print("⚠ No data.", style="yellow")
        return
    total = len(forecasts)
    regions = Counter(f.get("region","Unknown") for f in forecasts)
    avg_rain = 0
    vals = []
    for f in forecasts:
        r = f.get("weather_forecast",{}).get("rainfall")
        try: vals.append(float(r))
        except: pass
    if vals: avg_rain = sum(vals)/len(vals)
    console.print(f"\nTotal forecasts: {total}")
    for k,v in regions.items(): console.print(f"{k}: {v}")
    console.print(f"Average rainfall: {avg_rain:.2f} mm")
    with open("report.json","w") as f: json.dump({"total":total,"regions":regions,"avg_rain":avg_rain},f,indent=4)

def manage_farmer_queries():
    file = "queries.json"
    if not os.path.exists(file):
        console.print("⚠ No queries yet.", style="yellow"); return
    with open(file) as f: data=json.load(f)
    for i,q in enumerate(data,1):
        console.print(f"{i}. [{q['status']}] {q['farmer_username']} - {q['crop']}: {q['issue']}")
    idx = int(input("Query number to reply (0 cancel): "))
    if idx<=0 or idx>len(data): return
    reply = input("Enter reply / approve / reject: ").lower()
    q=data[idx-1]
    q["status"]="approved" if reply=="approve" else "rejected" if reply=="reject" else "responded"
    q["response"]=reply
    q["responded_on"]=datetime.now().isoformat()
    with open(file,"w") as f: json.dump(data,f,indent=4)
    console.print("✅ Response saved.",style="green")
    
def admin_login():
    """Authenticate admin before showing admin menu."""
    console.print("\n--- Admin Login ---", style="bold")
    username = input("Enter Admin Username: ").strip()
    password = input("Enter Admin Password: ").strip()

    if username != "admin10" or password != "password10":
        console.print("❌ Wrong credentials! Access denied.", style="red")
        time.sleep(1)
        return  # Go back to main menu

    console.print("✅ Admin login successful!", style="green")

    # --- Admin Menu after successful login ---
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
            break
        else:
            console.print("Invalid choice.", style="red")

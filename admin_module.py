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

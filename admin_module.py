# admin_module.py

import os, csv, json, time
from datetime import datetime
from collections import Counter
from rich.progress import track
from config import console, FORECAST_FILE, ADVISORY_FILE, DATA_CSV_FOLDER
from file_utils import save_entry, read_data, write_data

# Ensure data_csv folder always exists
if not os.path.exists(DATA_CSV_FOLDER):
    os.makedirs(DATA_CSV_FOLDER)


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
    """
    FAST Bulk upload from CSV → writes once instead of per row
    """
    if not os.path.isdir(DATA_CSV_FOLDER):
        console.print(f"⚠ Directory '{DATA_CSV_FOLDER}' not found.", style="red")
        return

    csv_files = [f for f in os.listdir(DATA_CSV_FOLDER) if f.endswith('.csv')]
    if not csv_files:
        console.print("⚠ No CSV files found in folder.", style="yellow")
        return

    console.print("\nChoose CSV to upload:", style="bold cyan")
    for i, f in enumerate(csv_files, start=1):
        print(f"{i}. {f}")

    try:
        idx = int(input("File number: ")) - 1
        if idx < 0 or idx >= len(csv_files):
            console.print("❌ Invalid choice", style="red")
            return
    except:
        console.print("❌ Invalid input", style="red")
        return

    file_path = os.path.join(DATA_CSV_FOLDER, csv_files[idx])

    import pandas as pd
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        console.print(f"⚠ Error reading CSV: {e}", style="red")
        return

    # Build entries list
    new_entries = []
    for _, row in df.iterrows():
        entry = {
            "season": row.get('season', ''),
            "region": row.get('region', ''),
            "dates": {"start": row.get('start_date',''), "end": row.get('end_date','')},
            "weather_forecast": {
                "rainfall": row.get('rainfall',''),
                "temperature": row.get('temperature',''),
                "humidity": row.get('humidity','')
            },
            "crop_suggestions": [c.strip() for c in str(row.get('crop_suggestions','')).split(',')],
            "pest_alert": [p.strip() for p in str(row.get('pest_alert','')).split(',')],
            "timestamp": datetime.now().isoformat()
        }
        new_entries.append(entry)

    # Append all rows at once
    existing = read_data(FORECAST_FILE)
    existing.extend(new_entries)
    write_data(FORECAST_FILE, existing)

    console.print(f"✅ Bulk imported {len(new_entries)} records from {csv_files[idx]}", style="green")


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

def generate_bulk_reports():
    """
    Reads ALL CSV files inside data_csv folder and generates a weather summary report.
    Only reports values from CSV-based bulk uploads.
    """
    if not os.path.isdir(DATA_CSV_FOLDER):
        console.print(f"⚠ Folder '{DATA_CSV_FOLDER}' not found.", style="red")
        return

    csv_files = [f for f in os.listdir(DATA_CSV_FOLDER) if f.endswith(".csv")]
    if not csv_files:
        console.print("⚠ No CSV files found for bulk reports.", style="yellow")
        return

    import pandas as pd

    all_data = []
    for file in csv_files:
        try:
            df = pd.read_csv(os.path.join(DATA_CSV_FOLDER, file))
            all_data.append(df)
        except:
            console.print(f"⚠ Error reading {file}. Skipping.", style="yellow")

    if not all_data:
        console.print("⚠ No readable CSV data found.", style="yellow")
        return

    final_df = pd.concat(all_data, ignore_index=True)
    cols = set(final_df.columns.str.lower())
    if {"element", "item", "year", "unit", "value"} <= cols:
         try:
                df = final_df.rename(columns={c: c.lower() for c in final_df.columns})
                df["value"] = pd.to_numeric(df["value"], errors="coerce")

                console.print("\n📊 Top 10 Items by Total Value (all Elements combined)", style="bold")
                top_items = (df.groupby("item")["value"].sum().sort_values(ascending=False).head(10))
                for item, val in top_items.items():
                    console.print(f"  • {item}: {val:,.0f} {df['unit'].mode().iat[0] if not df['unit'].isna().all() else ''}")

        # Save a richer bulk report next to bulk_report.json
                rich_report = {
            "type": "bulk_csv_report",
            "total_records": int(len(df)),
            "top_items_total_value": top_items.to_dict(),
            "timestamp": datetime.now().isoformat()
        }
                with open("bulk_report_rich.json","w",encoding="utf-8") as f:
                    json.dump(rich_report, f, indent=4)
                console.print("✅ Extra summary saved to bulk_report_rich.json", style="green")
         except Exception as e:
                console.print(f"Note: FAO summary skipped ({e})", style="yellow")


    # Attempt conversion to numeric (safe)
    for col in ["rainfall", "temperature", "humidity"]:
        if col in final_df.columns:
            final_df[col] = pd.to_numeric(final_df[col], errors="coerce")

    # Summary
    avg_rain = final_df["rainfall"].mean() if "rainfall" in final_df else None
    avg_temp = final_df["temperature"].mean() if "temperature" in final_df else None
    avg_hum = final_df["humidity"].mean() if "humidity" in final_df else None

    console.print("\n🌾 --- Bulk Forecast Report (CSV Data Only) ---", style="bold cyan")
    console.print(f"📦 Total records read: {len(final_df)}")
    if avg_rain: console.print(f"🌧 Average Rainfall: {avg_rain:.2f} mm")
    if avg_temp: console.print(f"🌡 Average Temperature: {avg_temp:.2f}°C")
    if avg_hum:  console.print(f"💧 Average Humidity: {avg_hum:.2f}%")

    # Save JSON output
    report = {
        "type": "bulk_csv_report",
        "total_records": len(final_df),
        "avg_rain": float(avg_rain) if avg_rain else None,
        "avg_temp": float(avg_temp) if avg_temp else None,
        "avg_humidity": float(avg_hum) if avg_hum else None,
        "timestamp": datetime.now().isoformat()
    }

    with open("bulk_report.json","w") as f:
        json.dump(report, f, indent=4)

    console.print("✅ Bulk report saved to bulk_report.json", style="green")





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
        print("7. Generate Bulk Reports (from CSV)")
        print("8. Logout")

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
            generate_bulk_reports()
        elif choice == "8":
            console.print("Logging out...", style="red")
            break
        else:
            console.print("Invalid choice.", style="red")

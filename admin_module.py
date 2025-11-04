# admin_module.py


import os, csv, json, time
from datetime import datetime
from collections import Counter
from rich.progress import track
from config import console, FORECAST_FILE, ADVISORY_FILE, DATA_CSV_FOLDER
from file_utils import save_entry, read_data, write_data
from rich.table import Table
from rich.panel import Panel
from rich.console import Group

def _safe_float(value):
    """Safely converts a value to float, returning None on failure."""
    try:
        return float(value)
    except (ValueError, TypeError, AttributeError):
        return None

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

    # Display available forecasts
    for i, f in enumerate(forecasts, 1):
        console.print(f"{i}. {f.get('season','')} | {f.get('region','')}")

    try:
        idx_str = input("Enter number to edit/delete (0 cancel): ")
        if not idx_str.isdigit(): return
        
        idx = int(idx_str)
        if idx == 0 or idx > len(forecasts):
            return
    except ValueError:
        return # Handle non-integer input gracefully

    action = input("(U)pdate / (D)elete? ").lower().strip()

    if action == 'd':
        # --- Delete Action ---
        try:
            removed = forecasts.pop(idx - 1)
            write_data(FORECAST_FILE, forecasts)
            console.print(f"✔ Deleted forecast for {removed.get('season','')} | {removed.get('region','')}.", style="green")
        except IndexError:
            console.print("❌ Invalid number.", style="red")

    elif action == 'u':
        # --- Update Action ---
        try:
            f = forecasts[idx - 1] # Get the forecast to edit
            
            console.print(f"\n--- Updating: {f.get('season','')} | {f.get('region','')} ---", style="bold")
            console.print("(Press Enter to keep the current value)")

            # Simple string fields
            f['season'] = input(f"Season [{f.get('season', '')}]: ") or f.get('season', '')
            f['region'] = input(f"Region [{f.get('region', '')}]: ") or f.get('region', '')

            # Nested 'dates' dictionary
            # Ensure nested dicts exist before accessing keys
            if 'dates' not in f: f['dates'] = {} 
            f_dates = f.get('dates', {}) 
            f['dates']['start'] = input(f"Start Date [{f_dates.get('start', '')}]: ") or f_dates.get('start', '')
            f['dates']['end'] = input(f"End Date [{f_dates.get('end', '')}]: ") or f_dates.get('end', '')

            # Nested 'weather_forecast' dictionary
            if 'weather_forecast' not in f: f['weather_forecast'] = {}
            f_weather = f.get('weather_forecast', {})
            f['weather_forecast']['rainfall'] = input(f"Rainfall (mm) [{f_weather.get('rainfall', '')}]: ") or f_weather.get('rainfall', '')
            f['weather_forecast']['temperature'] = input(f"Temperature (°C) [{f_weather.get('temperature', '')}]: ") or f_weather.get('temperature', '')
            f['weather_forecast']['humidity'] = input(f"Humidity (%) [{f_weather.get('humidity', '')}]: ") or f_weather.get('humidity', '')

            # List 'crop_suggestions'
            current_crops = ', '.join(f.get('crop_suggestions', []))
            new_crops_str = input(f"Crop suggestions [{current_crops}]: ") or current_crops
            # Repopulate list, removing empty strings
            f['crop_suggestions'] = [c.strip() for c in new_crops_str.split(",") if c.strip()]

            # List 'pest_alert'
            current_pests = ', '.join(f.get('pest_alert', []))
            new_pests_str = input(f"Pest alerts [{current_pests}]: ") or current_pests
            # Repopulate list, removing empty strings
            f['pest_alert'] = [p.strip() for p in new_pests_str.split(",") if p.strip()]

            # Update the timestamp to reflect the edit time
            f['timestamp'] = datetime.now().isoformat()
            
            write_data(FORECAST_FILE, forecasts)
            console.print("✔ Forecast updated successfully.", style="green")

        except IndexError:
            console.print("❌ Invalid number.", style="red")
        except Exception as e:
            console.print(f"❌ An error occurred during update: {e}", style="red")
    
    else:
        console.print("Cancelled.", style="yellow")

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

    for i, f in enumerate(files, 1):
        print(f"{i}. {f}")

    try:
        idx_str = input("File number (0 cancel): ")
        if not idx_str.isdigit(): return
        
        idx = int(idx_str)
        if idx == 0 or idx > len(files):
            console.print("Cancelled.")
            return
        
        path = os.path.join(DATA_CSV_FOLDER, files[idx - 1])

        # --- OPTIMIZATION START ---

        # 1. Read the existing data ONCE
        all_forecasts = read_data(FORECAST_FILE)
        new_entries = []
        
        console.print(f"Processing '{files[idx - 1]}'...", style="cyan")

        # 2. Open the CSV and process rows into a temporary list
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                entry = {
                    "season": row.get("season", ""),
                    "region": row.get("region", ""),
                    "dates": {
                        "start": row.get("start_date", ""), 
                        "end": row.get("end_date", "")
                    },
                    "weather_forecast": {
                        "rainfall": row.get("rainfall", ""), 
                        "temperature": row.get("temperature", ""), 
                        "humidity": row.get("humidity", "")
                    },
                    # Clean lists: "a,b," becomes ['a', 'b'] not ['a', 'b', '']
                    "crop_suggestions": [c.strip() for c in row.get("crop_suggestions", "").split(",") if c.strip()],
                    "pest_alert": [p.strip() for p in row.get("pest_alert", "").split(",") if p.strip()],
                    "timestamp": datetime.now().isoformat()
                }
                # 3. Add to the in-memory list (NOT the file)
                new_entries.append(entry)
        
        # 4. Add all new entries to the main list
        all_forecasts.extend(new_entries)
        
        # 5. Write to the file ONCE
        write_data(FORECAST_FILE, all_forecasts)
        
        # --- OPTIMIZATION END ---

        console.print(f"✅ Bulk upload done! Added {len(new_entries)} new entries.", style="green")

    except FileNotFoundError:
        console.print(f"❌ Error: File not found at {path}", style="red")
    except Exception as e:
        console.print(f"❌ An error occurred during processing: {e}", style="red")

def generate_reports():
    forecasts = read_data(FORECAST_FILE)
    if not forecasts:
        console.print("⚠ No forecast data found to generate reports.", style="yellow")
        return

    console.print("\n[bold cyan]Generating comprehensive forecast report...[/bold cyan]")

    # --- 1. Data Processing ---
    # Initialize containers
    total_forecasts = len(forecasts)
    all_crops = []
    all_pests = []
    all_seasons = []
    regional_data = {}
    
    overall_rainfall = []
    overall_temp = []
    overall_humidity = []
    
    missing_data = {
        "rainfall": 0,
        "temperature": 0,
        "humidity": 0,
        "region": 0,
        "season": 0
    }

    # Loop through all forecasts ONCE
    for f in forecasts:
        region = f.get("region") or "Unknown"
        season = f.get("season") or "Unknown"
        
        if region == "Unknown": missing_data["region"] += 1
        if season == "Unknown": missing_data["season"] += 1
        
        all_seasons.append(season)

        # Initialize region if not seen
        if region not in regional_data:
            regional_data[region] = {
                "count": 0,
                "rainfall": [],
                "temp": [],
                "humidity": []
            }
        
        regional_data[region]["count"] += 1
        
        # Process weather data
        weather = f.get("weather_forecast", {})
        
        rain = _safe_float(weather.get("rainfall"))
        temp = _safe_float(weather.get("temperature"))
        humid = _safe_float(weather.get("humidity"))

        if rain is not None:
            overall_rainfall.append(rain)
            regional_data[region]["rainfall"].append(rain)
        else:
            missing_data["rainfall"] += 1

        if temp is not None:
            overall_temp.append(temp)
            regional_data[region]["temp"].append(temp)
        else:
            missing_data["temperature"] += 1

        if humid is not None:
            overall_humidity.append(humid)
            regional_data[region]["humidity"].append(humid)
        else:
            missing_data["humidity"] += 1
            
        # Process lists
        all_crops.extend([c for c in f.get("crop_suggestions", []) if c])
        all_pests.extend([p for p in f.get("pest_alert", []) if p])

    # --- 2. Calculate Statistics ---
    
    # Overall averages
    avg_stats = {
        "avg_rainfall": sum(overall_rainfall) / len(overall_rainfall) if overall_rainfall else 0,
        "avg_temp": sum(overall_temp) / len(overall_temp) if overall_temp else 0,
        "avg_humidity": sum(overall_humidity) / len(overall_humidity) if overall_humidity else 0,
    }

    # Counts
    season_counts = Counter(all_seasons)
    crop_counts = Counter(all_crops)
    pest_counts = Counter(all_pests)

    # Final regional stats
    final_regional_stats = {}
    for region, data in regional_data.items():
        final_regional_stats[region] = {
            "count": data["count"],
            "avg_rainfall": sum(data["rainfall"]) / len(data["rainfall"]) if data["rainfall"] else 0,
            "avg_temp": sum(data["temp"]) / len(data["temp"]) if data["temp"] else 0,
            "avg_humidity": sum(data["humidity"]) / len(data["humidity"]) if data["humidity"] else 0,
        }

    # --- 3. Rich Console Output ---
    
    # Panel 1: Overall Statistics
    stats_table = Table(show_header=False, box=None, padding=(0, 2))
    stats_table.add_row("[bold]Total Forecasts:[/bold]", f"{total_forecasts}")
    stats_table.add_row("[bold]Avg. Rainfall:[/bold]", f"{avg_stats['avg_rainfall']:.2f} mm")
    stats_table.add_row("[bold]Avg. Temperature:[/bold]", f"{avg_stats['avg_temp']:.2f} °C")
    stats_table.add_row("[bold]Avg. Humidity:[/bold]", f"{avg_stats['avg_humidity']:.2f} %")
    
    # Panel 2: Regional Breakdown
    region_table = Table(title="[bold]Regional Breakdown[/bold]", pad_edge=False)
    region_table.add_column("Region", style="cyan", no_wrap=True)
    region_table.add_column("Count", style="magenta")
    region_table.add_column("Avg. Rain (mm)", style="blue")
    region_table.add_column("Avg. Temp (°C)", style="red")
    region_table.add_column("Avg. Humidity (%)", style="green")
    
    for region, stats in sorted(final_regional_stats.items()):
        region_table.add_row(
            region,
            f"{stats['count']}",
            f"{stats['avg_rainfall']:.2f}",
            f"{stats['avg_temp']:.2f}",
            f"{stats['avg_humidity']:.2f}"
        )

    # Panel 3: Seasonal & Trend Analysis
    season_table = Table(title="[bold]Seasonal Entries[/bold]", box=None, padding=(0,1))
    season_table.add_column("Season", style="cyan")
    season_table.add_column("Count", style="magenta")
    for season, count in season_counts.most_common():
        season_table.add_row(season, str(count))

    crop_table = Table(title="[bold]Top 5 Crops[/bold]", box=None, padding=(0,1))
    crop_table.add_column("Crop", style="green")
    crop_table.add_column("Count", style="magenta")
    for crop, count in crop_counts.most_common(5):
        crop_table.add_row(crop, str(count))
        
    pest_table = Table(title="[bold]Top 5 Pests[/bold]", box=None, padding=(0,1))
    pest_table.add_column("Pest", style="red")
    pest_table.add_column("Count", style="magenta")
    for pest, count in pest_counts.most_common(5):
        pest_table.add_row(pest, str(count))
        
    trend_table = Table.grid(expand=True, padding=2)
    trend_table.add_column()
    trend_table.add_column()
    trend_table.add_column()
    trend_table.add_row(season_table, crop_table, pest_table)

    # Panel 4: Data Quality
    quality_table = Table(title="[bold]Data Quality (Missing Values)[/bold]", box=None, padding=(0, 2))
    quality_table.add_column("Field", style="yellow")
    quality_table.add_column("Missing Count", style="red")
    for field, count in missing_data.items():
        if count > 0:
            quality_table.add_row(field.title(), str(count))
    if all(v == 0 for v in missing_data.values()):
        quality_table.add_row("All fields", "[green]Excellent (0 missing)[/green]")
        

    # Print all panels
    console.print(Panel(stats_table, title="[bold]Overall Statistics[/bold]", border_style="blue", expand=False))
    console.print(region_table)
    console.print(trend_table)
    console.print(Panel(quality_table, title="[bold]Report Health[/bold]", border_style="yellow", expand=False))

    # --- 4. Structured JSON Output ---
    report_data = {
        "report_generated_on": datetime.now().isoformat(),
        "overall_stats": {
            "total_forecasts": total_forecasts,
            "avg_rainfall_mm": float(f"{avg_stats['avg_rainfall']:.2f}"),
            "avg_temp_c": float(f"{avg_stats['avg_temp']:.2f}"),
            "avg_humidity_percent": float(f"{avg_stats['avg_humidity']:.2f}")
        },
        "regional_breakdown": {
            region: {
                "count": stats["count"],
                "avg_rainfall_mm": float(f"{stats['avg_rainfall']:.2f}"),
                "avg_temp_c": float(f"{stats['avg_temp']:.2f}"),
                "avg_humidity_percent": float(f"{stats['avg_humidity']:.2f}")
            } for region, stats in final_regional_stats.items()
        },
        "trends": {
            "seasons": dict(season_counts),
            "top_crops": crop_counts.most_common(10), # Save top 10 to JSON
            "top_pests": pest_counts.most_common(10)  # Save top 10 to JSON
        },
        "data_quality": {
            "missing_entries": missing_data
        }
    }

    report_filename = "report.json"
    with open(report_filename, "w") as f:
        json.dump(report_data, f, indent=4)
        
    console.print(f"\n✅ [bold green]Report saved to {report_filename}[/bold green]")


def generate_historical_report():
    HISTORICAL_FILE = "historical_temps.json"
    REPORT_FILE = "historical_report.json"

    # 1. Read the historical data file
    if not os.path.exists(HISTORICAL_FILE):
        console.print(f"⚠ [bold red]File not found:[/bold red] '{HISTORICAL_FILE}' does not exist.", style="yellow")
        console.print("Please run 'Upload Historical Temperature Data' first (Option 7).")
        return

    try:
        with open(HISTORICAL_FILE, "r") as f:
            data = json.load(f)
    except Exception as e:
        console.print(f"❌ Error reading {HISTORICAL_FILE}: {e}", style="red")
        return

    if not data:
        console.print("⚠ No historical data found in file.", style="yellow")
        return

    console.print("\n[bold cyan]Generating Historical Temperature Report...[/bold cyan]")

    # 2. Process Data and Calculate Stats
    
    # Ensure data is sorted by year
    data.sort(key=lambda x: x["YEAR"])
    
    total_years = len(data)
    
    # Find extremes
    hottest_year = max(data, key=lambda x: x['ANNUAL'])
    coldest_year = min(data, key=lambda x: x['ANNUAL'])
    
    # Calculate seasonal averages
    avg_annual = sum(d['ANNUAL'] for d in data) / total_years
    avg_jan_feb = sum(d['JAN-FEB'] for d in data) / total_years
    avg_mar_may = sum(d['MAR-MAY'] for d in data) / total_years
    avg_jun_sep = sum(d['JUN-SEP'] for d in data) / total_years
    avg_oct_dec = sum(d['OCT-DEC'] for d in data) / total_years

    # Calculate decadal trend
    first_decade_data = [d['ANNUAL'] for d in data if 1961 <= d['YEAR'] <= 1970]
    last_decade_data = [d['ANNUAL'] for d in data if 2009 <= d['YEAR'] <= 2018]
    
    avg_first_decade = sum(first_decade_data) / len(first_decade_data) if first_decade_data else 0
    avg_last_decade = sum(last_decade_data) / len(last_decade_data) if last_decade_data else 0
    trend_diff = avg_last_decade - avg_first_decade

    # 3. Rich Console Output
    
    # Panel 1: Overall Summary
    summary_table = Table(show_header=False, box=None, padding=(0, 2))
    summary_table.add_row("[bold]Data Span:[/bold]", f"{data[0]['YEAR']} - {data[-1]['YEAR']} ({total_years} years)")
    summary_table.add_row("[bold]Overall Avg. Temp:[/bold]", f"{avg_annual:.2f} °C")
    
    # Panel 2: Extremes
    extreme_table = Table(title="[bold]Record Years[/bold]", box=None, padding=(0, 2))
    extreme_table.add_column("Record", style="cyan")
    extreme_table.add_column("Year (Temp)", style="white")
    extreme_table.add_row("Hottest Year", f"{hottest_year['YEAR']} ({hottest_year['ANNUAL']:.2f} °C)")
    extreme_table.add_row("Coldest Year", f"{coldest_year['YEAR']} ({coldest_year['ANNUAL']:.2f} °C)")

    # Panel 3: Seasonal Averages
    season_table = Table(title="[bold]Average Temperature by Season[/bold]")
    season_table.add_column("Season", style="cyan")
    season_table.add_column("Avg. Temp (°C)", style="magenta")
    season_table.add_row("Jan-Feb", f"{avg_jan_feb:.2f}")
    season_table.add_row("Mar-May", f"{avg_mar_may:.2f}")
    season_table.add_row("Jun-Sep", f"{avg_jun_sep:.2f}")
    season_table.add_row("Oct-Dec", f"{avg_oct_dec:.2f}")

   # Panel 4: Trend
    trend_table = Table(title="[bold]Decadal Warming Trend[/bold]")
    trend_table.add_column("Decade", style="cyan")
    trend_table.add_column("Avg. Temp (°C)", style="magenta")
    trend_table.add_row("1961-1970", f"{avg_first_decade:.2f}")
    trend_table.add_row("2009-2018", f"{avg_last_decade:.2f}")

    # --- FIX ---
    # Determine the style *before* creating the string
    style = "bold red" if trend_diff > 0 else "bold blue"
    change_str = f"[{style}]{trend_diff:+.2f} °C[/{style}]"
    
    # Add the fully formed string to the table
    trend_table.add_row("[bold]Change[/bold]", change_str)
    # --- END FIX ---

    # Print all panels
    console.print(Panel(summary_table, title="[bold]Overall Statistics[/bold]", border_style="blue", expand=False))
    console.print(Panel(extreme_table, title="[bold]Extremes[/bold]", border_style="red", expand=False))
    console.print(season_table)
    console.print(trend_table)

    # 4. Structured JSON Output
    report_data = {
        "report_generated_on": datetime.now().isoformat(),
        "data_span": f"{data[0]['YEAR']} - {data[-1]['YEAR']}",
        "total_years": total_years,
        "overall_avg_temp_c": float(f"{avg_annual:.2f}"),
        "extremes": {
            "hottest_year": hottest_year,
            "coldest_year": coldest_year,
        },
        "seasonal_averages_c": {
            "JAN-FEB": float(f"{avg_jan_feb:.2f}"),
            "MAR-MAY": float(f"{avg_mar_may:.2f}"),
            "JUN-SEP": float(f"{avg_jun_sep:.2f}"),
            "OCT-DEC": float(f"{avg_oct_dec:.2f}"),
        },
        "decadal_trend": {
            "first_decade_avg": float(f"{avg_first_decade:.2f}"),
            "last_decade_avg": float(f"{avg_last_decade:.2f}"),
            "change_c": float(f"{trend_diff:.2f}"),
        }
    }
    
    with open(REPORT_FILE, "w") as f:
        json.dump(report_data, f, indent=4)
        
    console.print(f"\n✅ [bold green]Historical report saved to {REPORT_FILE}[/bold green]")


def manage_farmer_queries():
    file = "queries.json"
    data = []  # Default to an empty list

    try:
        # Try to open and read the file
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
    except FileNotFoundError:
        # File doesn't exist yet, which is fine. data is already []
        pass 
        
    except json.JSONDecodeError:
        # This catches your exact error: file is empty or corrupt
        console.print(f"⚠ Warning: '{file}' is empty or unreadable. A new list will be used.", style="yellow")
        data = [] # Ensure data is an empty list
        
    except Exception as e:
        console.print(f"❌ An unexpected error occurred reading {file}: {e}", style="red")
        return # Exit on unknown errors

    # Check if data is empty (from FileNotFoundError or JSONDecodeError)
    if not data:
        console.print("⚠ No queries yet.", style="yellow")
        # Don't return, allow admin to see the 'no queries' message
        # but the rest of the function will be skipped.
        # We'll re-evaluate this logic.
        # Let's adjust: if no data, just return.
        return

    # Display queries
    for i, q in enumerate(data, 1):
        console.print(
            f"{i}. [{q.get('status','new')}] "
            f"{q.get('farmer_username','Unknown User')} - "
            f"{q.get('crop','No Crop')}: {q.get('issue','No Issue')}"
        )

    try:
        idx_str = input("Query number to reply (0 cancel): ")
        if not idx_str.isdigit(): 
            console.print("Cancelled.", style="yellow")
            return
        
        idx = int(idx_str)
        if idx <= 0 or idx > len(data):
            console.print("Cancelled or invalid number.", style="yellow")
            return
    except ValueError:
        return # Handle non-integer input

    reply = input("Enter reply / approve / reject: ").lower().strip()
    q = data[idx - 1]

    # Update status and response
    if reply == "approve":
        q["status"] = "approved"
        q["response"] = "Your query has been approved."
    elif reply == "reject":
        q["status"] = "rejected"
        q["response"] = "Your query has been rejected."
    else:
        q["status"] = "responded"
        q["response"] = reply  # Use the custom reply

    q["responded_on"] = datetime.now().isoformat()

    # Write back to the file
    try:
        with open(file, "w", encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        console.print("✅ Response saved.", style="green")
    except Exception as e:
        console.print(f"❌ Error writing response to {file}: {e}", style="red")

def upload_historical_temps():
    """
    Reads 'temperatures.csv' from the data folder and saves it 
    as 'historical_temps.json' in the root directory.
    """
    file_name = "temperature.csv"
    path = os.path.join(DATA_CSV_FOLDER, file_name)

    # Check if the file exists in the data folder
    if not os.path.exists(path):
        console.print(f"⚠ [bold red]File not found:[/bold red] '{file_name}' was not found in the '{DATA_CSV_FOLDER}' folder.", style="yellow")
        console.print("Please add the file and try again.")
        return

    historical_data = []
    console.print(f"Processing '{file_name}'...", style="cyan")

    # Read the CSV file
    try:
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Convert string values to numbers for correct JSON storage
                processed_row = {
                    "YEAR": int(row["YEAR"]),
                    "ANNUAL": float(row["ANNUAL"]),
                    "JAN-FEB": float(row["JAN-FEB"]),
                    "MAR-MAY": float(row["MAR-MAY"]),
                    "JUN-SEP": float(row["JUN-SEP"]),
                    "OCT-DEC": float(row["OCT-DEC"]),
                }
                historical_data.append(processed_row)
        
        # Write the processed data to a new JSON file
        output_filename = "historical_temps.json"
        with open(output_filename, "w", encoding='utf-8') as f:
            json.dump(historical_data, f, indent=4)
        
        console.print(f"✅ Success! Historical data saved to [bold green]'{output_filename}'[/bold green].", style="green")

    except KeyError as e:
        console.print(f"❌ [bold red]CSV Format Error:[/bold red] The file is missing an expected column: {e}", style="red")
        console.print("Please ensure the CSV has headers: YEAR, ANNUAL, JAN-FEB, MAR-MAY, JUN-SEP, OCT-DEC")
    except ValueError as e:
        console.print(f"❌ [bold red]Data Error:[/bold red] Could not convert a value to a number. {e}", style="red")
        console.print("Please check the CSV for non-numeric data (e.g., text) in the value columns.")
    except Exception as e:
        console.print(f"❌ An unexpected error occurred: {e}", style="red")


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
        print("7. Upload Historical Temperature Data")
        print("8. Generate Temperature Reports")
        print("9. Logout")

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
            upload_historical_temps()
        elif choice == "8":
            generate_historical_report() # <-- NEW OPTION
        elif choice == "9":
            console.print("Logging out...", style="red")
            break
        else:
            console.print("Invalid choice.", style="red")
# farmer_module.py

import os, json, pandas as pd
from datetime import datetime
from tabulate import tabulate
from config import console, FARMERS_FILE, DATA_CSV_FOLDER, FORECAST_FILE, ADVISORY_FILE
from file_utils import read_data, save_entry, write_data

pd.set_option('display.max_rows', None)

def view_seasonal_forecast(farmer_region):
    """
    Displays filtered forecasts for the logged-in farmer's region.
    Filters out any empty/invalid forecast entries.
    """
    try:
        data = read_data(FORECAST_FILE)
        if not data:
            console.print("⚠ No forecasts available.", style="yellow"); return

        table = []
        
        # Filter data based on region and check for empty rows
        filtered_forecasts = []
        for f in data:
            # 1. Filter out empty/invalid rows (skip if no season is listed)
            if not f.get("season"):
                continue
                
            # 2. Filter by farmer's region
            if f.get("region", "").lower() == farmer_region.lower():
                filtered_forecasts.append(f)

        if not filtered_forecasts:
            console.print(f"⚠ No forecasts found for your region ('{farmer_region}').", style="yellow")
            return

        # Build table from the clean, filtered data
        for f in filtered_forecasts:
            d = f.get("dates", {})
            w = f.get("weather_forecast", {})
            table.append([
                f.get("season"), f.get("region"),
                f"{d.get('start','N/A')}→{d.get('end','N/A')}",
                w.get("rainfall", "N/A"), w.get("temperature", "N/A"), w.get("humidity", "N/A"),
                ", ".join(f.get("crop_suggestions", []) or ["N/A"]), 
                ", ".join(f.get("pest_alert", []) or ["N/A"])
            ])
            
        headers = ["Season", "Region", "Date", "Rain(mm)", "Temp(°C)", "Hum(%)", "Crops", "Pests"]
        print(tabulate(table, headers, tablefmt="grid", showindex=True))
        
    except Exception as e:
        console.print(f"Error loading forecasts: {e}", style="red")

def access_crop_advisories():
    data = read_data(ADVISORY_FILE)
    if not data: console.print("⚠ No advisories.",style="yellow"); return
    crop=input("Filter by crop (enter to skip): ").lower()
    filt=[a for a in data if not crop or crop in a.get("Crop","").lower()]
    if not filt: console.print("No match.",style="yellow"); return
    table=[[a["Crop"],a["Season"],a["Practices"],a["Fertilizers"],a["Precaution"]] for a in filt]
    print(tabulate(table,headers=["Crop","Season","Practices","Fertilizers","Precaution"],tablefmt="fancy_grid"))

def search_historical_data():
    # 1. Check for folder
    if not os.path.isdir(DATA_CSV_FOLDER): 
        console.print("⚠ data_csv folder missing", style="red"); return
        
    # 2. List CSV files
    files = [f for f in os.listdir(DATA_CSV_FOLDER) if f.endswith(".csv")]
    if not files: 
        console.print("⚠ No CSV files found in data_csv folder", style="yellow"); return
        
    console.print("\n--- Search Historical Data ---", style="bold")
    for i, f in enumerate(files, 1): 
        print(f"{i}. {f}")
    
    # 3. Get file choice
    try:
        n_str = input("Choose file to search (0 cancel): ")
        if not n_str.isdigit(): return
        n = int(n_str) - 1
        
        if n == -1: # User entered 0
             return
        if n < 0 or n >= len(files):
            console.print("Invalid selection.", style="red")
            return
    except ValueError:
        return

    # 4. Load DataFrame
    try:
        file_path = os.path.join(DATA_CSV_FOLDER, files[n])
        df = pd.read_csv(file_path)
    except Exception as e:
        console.print(f"❌ Error reading file: {e}", style="red")
        return
        
    # 5. Get search term (this is the simplified part)
    search_term = input("Enter search term (Crops and livestock products/Area Code/Element Code/ India/ Iteam name): ").strip().lower()
    if not search_term:
        console.print("Search cancelled.", style="yellow")
        return
        
    # 6. Filter DataFrame
    try:
        # Convert all columns to string and lowercase for a robust, universal search
        df_str = df.astype(str).apply(lambda x: x.str.lower())
        
        # Create a mask that is True for any row where *any* column contains the search term
        mask = df_str.apply(lambda col: col.str.contains(search_term, na=False)).any(axis=1)
        
        # Apply the mask to the original DataFrame
        filtered_df = df[mask]
            
    except Exception as e:
        console.print(f"❌ Error during search: {e}", style="red")
        return

    # 7. Display results
    if filtered_df.empty:
        console.print(f"⚠ No results found for '{search_term}'.", style="yellow")
    else:
        console.print(f"\n[bold green]Found {len(filtered_df)} result(s):[/bold green]")
        print(tabulate(filtered_df, headers="keys", tablefmt="fancy_grid", showindex=False))

def submit_query(username):
    """
    Submits a query for the logged-in farmer.
    Now accepts 'username' as an argument.
    """
    console.print("\n--- Submit Query ---", style="bold")
    # No need to ask for username, we already have it
    console.print(f"Submitting as: [cyan]{username}[/cyan]")
    
    c = input("Crop: ")
    i = input("Issue: ")

    if not (c and i):
        console.print("⚠ Crop and Issue fields are required.", style="red")
        return

    q = {
        "farmer_username": username,  # Use the passed-in username
        "crop": c,
        "issue": i,
        "status": "pending",
        "response": "",
        "timestamp": datetime.now().isoformat()
    }
    
    f = "queries.json"
    arr = []  # Default to an empty list

    # Robustly read the file, in case it's empty or doesn't exist
    try:
        with open(f, 'r', encoding='utf-8') as file:
            arr = json.load(file)
            # Make sure it's a list
            if not isinstance(arr, list):
                arr = []
    except FileNotFoundError:
        # File doesn't exist yet, which is fine. arr is already []
        pass
    except json.JSONDecodeError:
        # File is empty or corrupt. arr is already []
        pass
    except Exception as e:
        console.print(f"❌ An error occurred reading {f}: {e}", style="red")
        return  # Don't proceed if we can't read the file

    # Add the new query
    arr.append(q)
    
    # Write the data back
    try:
        write_data(f, arr) 
        console.print("✅ Query sent.", style="green")
    except Exception as e:
        console.print(f"❌ Error saving query: {e}", style="red")


def view_my_queries(username):
    """
    Shows the logged-in farmer a list of their submitted queries and any responses.
    """
    console.print(f"\n--- My Queries ({username}) ---", style="bold")
    file = "queries.json"
    all_queries = []

    # Robustly read the queries file
    try:
        with open(file, 'r', encoding='utf-8') as f:
            all_queries = json.load(f)
    except FileNotFoundError:
        pass  # No file, all_queries remains []
    except json.JSONDecodeError:
        pass  # Empty file, all_queries remains []
    except Exception as e:
        console.print(f"❌ Error reading queries: {e}", style="red")
        return

    # Filter for the specific user, newest queries first
    my_queries = [q for q in all_queries if q.get('farmer_username') == username]
    my_queries.reverse() # Show most recent first

    if not my_queries:
        console.print("You have not submitted any queries yet.", style="yellow")
        return

    # Format for tabulate
    table = []
    headers = ["Status", "Issue Submitted", "Response", "Submitted On"]
    
    for q in my_queries:
        status = q.get('status', 'N/A')
        response = q.get('response', '...')
        
        # Make it clear if a response is pending
        if status in ('pending', 'new'):
            response = "[yellow]Pending Admin Response...[/yellow]"
        elif status == 'rejected':
            response = f"[red]{response}[/red]"
        elif status in ('approved', 'responded'):
            response = f"[green]{response}[/green]"
            
        table.append([
            status.title(),
            q.get('issue', 'N/A'),
            response,
            q.get('timestamp', 'N/A').split('T')[0] # Show just the date
        ])
    
    console.print(tabulate(table, headers, tablefmt="fancy_grid"))

def manage_profile(username):
    console.print(f"\n--- Manage Profile for [cyan]{username}[/cyan] ---", style="bold")
    arr = read_data(FARMERS_FILE)
    
    for f in arr:
        if f["username"] == username:
            # Show current region, allow "Enter" to keep
            current_region = f.get('region', 'N/A')
            f["password"] = input(f"New password (or press Enter to keep): ") or f["password"]
            f["region"] = input(f"New region [{current_region}]: ") or f.get('region')
            
            write_data(FARMERS_FILE, arr)
            console.print("✔ Updated.", style="green")
            return
            
    console.print("User not found.", style="red")

def farmer_login_menu(farmer):
    """Farmer menu, now accepts the full farmer object."""
    username = farmer.get('username', 'Farmer')
    
    while True:
        console.print(f"\n--- Farmer Menu ({username}) ---", style="bold underline black on white")
        print("1. View Forecasts")
        print("2. View Advisories")
        print("3. Search Data")
        print("4. Submit Query")
        print("5. View My Queries")   # <-- NEW
        print("6. Manage Profile")  # <-- Renumbered
        print("7. Logout")          # <-- Renumbered
        
        c = input("Enter choice: ")
        
        if c == "1":
            view_seasonal_forecast(farmer.get('region'))
        elif c == "2":
            access_crop_advisories()
        elif c == "3":
            search_historical_data()
        elif c == "4":
            submit_query(username)
        elif c == "5":
            view_my_queries(username)  
        elif c == "6":
            manage_profile(username)  
        elif c == "7":
            break                    

def register_farmer():
    u=input("Username: "); p=input("Password: "); r=input("Region: ")
    if not (u and p and r): console.print("⚠ Required.",style="red"); return
    arr=read_data(FARMERS_FILE)
    if any(f["username"]==u for f in arr): console.print("Exists.",style="red"); return
    arr.append({"username":u,"password":p,"region":r})
    write_data(FARMERS_FILE,arr); console.print("✅ Registered.",style="green")

def farmer_login():
    u = input("Username: "); p = input("Password: ")
    arr = read_data(FARMERS_FILE)
    for f in arr:
        if f["username"] == u and f["password"] == p:
            console.print(f"✅ Login success. Welcome, {u}!", style="green")
            # Pass the *entire* farmer object (f), which includes username and region
            farmer_login_menu(f)
            return
    console.print("❌ Invalid credentials", style="red")

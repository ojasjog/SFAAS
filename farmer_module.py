# farmer_module.py

import os, json, pandas as pd
from datetime import datetime
from tabulate import tabulate
from config import console, FARMERS_FILE, DATA_CSV_FOLDER, FORECAST_FILE, ADVISORY_FILE
from file_utils import read_data, save_entry, write_data

pd.set_option('display.max_rows', None)

def view_seasonal_forecast():
    try:
        data = read_data(FORECAST_FILE)
        if not data:
            console.print("⚠ No forecasts.", style="yellow"); return
        table=[]
        for f in data:
            d=f.get("dates",{})
            w=f.get("weather_forecast",{})
            table.append([
                f.get("season"), f.get("region"),
                f"{d.get('start')}→{d.get('end')}",
                w.get("rainfall"), w.get("temperature"), w.get("humidity"),
                ", ".join(f.get("crop_suggestions",[])), ", ".join(f.get("pest_alert",[]))
            ])
        headers=["Season","Region","Date","Rain(mm)","Temp(°C)","Hum(%)","Crops","Pests"]
        print(tabulate(table,headers,tablefmt="grid",showindex=True))
    except Exception as e: console.print(f"Error: {e}",style="red")

def access_crop_advisories():
    data = read_data(ADVISORY_FILE)
    if not data: console.print("⚠ No advisories.",style="yellow"); return
    crop=input("Filter by crop (enter to skip): ").lower()
    filt=[a for a in data if not crop or crop in a.get("Crop","").lower()]
    if not filt: console.print("No match.",style="yellow"); return
    table=[[a["Crop"],a["Season"],a["Practices"],a["Fertilizers"],a["Precaution"]] for a in filt]
    print(tabulate(table,headers=["Crop","Season","Practices","Fertilizers","Precaution"],tablefmt="fancy_grid"))

def search_historical_data():
    if not os.path.isdir(DATA_CSV_FOLDER): console.print("⚠ data_csv missing",style="red"); return
    files=[f for f in os.listdir(DATA_CSV_FOLDER) if f.endswith(".csv")]
    if not files: console.print("⚠ No CSV files",style="yellow"); return
    for i,f in enumerate(files,1): print(f"{i}. {f}")
    n=int(input("Choose: "))-1
    if n<0 or n>=len(files): return
    df=pd.read_csv(os.path.join(DATA_CSV_FOLDER,files[n]))
    print(tabulate(df.head(),headers="keys",tablefmt="fancy_grid"))

def submit_query():
    console.print("\n--- Submit Query ---",style="bold")
    u=input("Username: "); c=input("Crop: "); i=input("Issue: ")
    if not (u and c and i): console.print("All fields required.",style="red"); return
    q={"farmer_username":u,"crop":c,"issue":i,"status":"pending","response":"","timestamp":datetime.now().isoformat()}
    f="queries.json"
    arr=read_data(f); arr.append(q); write_data(f,arr)
    console.print("✅ Query sent.",style="green")

def manage_profile():
    u=input("Username: ").strip()
    arr=read_data(FARMERS_FILE)
    for f in arr:
        if f["username"]==u:
            f["password"]=input("New password: ") or f["password"]
            f["region"]=input("New region: ") or f["region"]
            write_data(FARMERS_FILE,arr)
            console.print("✔ Updated.",style="green")
            return
    console.print("User not found.",style="red")

def farmer_login_menu(u):
    while True:
        console.print(f"\n--- Farmer Menu ({u}) ---",style="bold underline black on white")
        print("1.View Forecasts\n2.View Advisories\n3.Search Data\n4.Submit Query\n5.Manage Profile\n6.Logout")
        c=input("Enter choice: ")
        if c=="1": view_seasonal_forecast()
        elif c=="2": access_crop_advisories()
        elif c=="3": search_historical_data()
        elif c=="4": submit_query()
        elif c=="5": manage_profile()
        elif c=="6": break

def register_farmer():
    u=input("Username: "); p=input("Password: "); r=input("Region: ")
    if not (u and p and r): console.print("⚠ Required.",style="red"); return
    arr=read_data(FARMERS_FILE)
    if any(f["username"]==u for f in arr): console.print("Exists.",style="red"); return
    arr.append({"username":u,"password":p,"region":r})
    write_data(FARMERS_FILE,arr); console.print("✅ Registered.",style="green")

def farmer_login():
    u=input("Username: "); p=input("Password: ")
    arr=read_data(FARMERS_FILE)
    for f in arr:
        if f["username"]==u and f["password"]==p:
            console.print("✅ Login success",style="green")
            farmer_login_menu(u); return
    console.print("❌ Invalid credentials",style="red")

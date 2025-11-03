from config import console
from admin_module import admin_login
from farmer_module import farmer_login, register_farmer

def main_menu():
    console.print("\n=== Seasonal Forecast & Agriculture Advisory System ===", style="bold underline black on white")
    print("1.Admin Login\n2.Farmer Login\n3.Register Farmer\n4.Exit")
    return input("Enter choice: ")

def run_app():
    
    while True:
        c = main_menu()
        if c=="1": admin_login()
        elif c=="2": farmer_login()
        elif c=="3": register_farmer()
        elif c=="4":
            console.print("✅ Successfully closed the app. Goodbye!", style="red")
            break
        else: console.print("Invalid.",style="red")

if __name__=="__main__": run_app()

import time
from rich.console import Console
console = Console()

def admin_login():
    print("\n--- Admin Menu ---")
    print("1. Add Seasonal Forecast")
    print("2. Update/Delete Forecast")
    print("3. Manage Forecast")
    print("4. Upload Bulk Forecast Data")
    print("5. Generate Reports")
    print("6. Manage Farmer Queries")
    print("7. Logout")

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
        print("Loading 6")
    elif choice == "7":
        print("Logging out...")
    else:
        print("Invalid choice.")


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


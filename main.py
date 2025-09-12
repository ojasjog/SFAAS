# admin_login = int(input())
# admin_menu = int(input())
# farmer_login = int(input())
# farmer_entry = int(input())
# register_farmer = int(input())

import time
from rich.console import Console
console = Console()



print("\n== Seasonal Forecast & Agriculture Advisory System ===")
print("1. Admin Login")
print("2. Farmer Login")
print("3. Register as New Farmer")
print("4. Exit")

choice = input("Enter choice: ")

if choice == "1":
    for i in range(1,4):
        console.log(f"Doing important stuff...{i}")
        time.sleep(0.25)
    print("Admin")
elif choice == "2":
    for i in range(1,4):
        console.log(f"Doing important stuff...{i}")
        time.sleep(0.25)
    print("Farmer")
elif choice == "3":
    for i in range(1,4):
        console.log(f"Doing important stuff...{i}")
        time.sleep(0.25)
    print("Registration")
elif choice == "4":
    print("Loaded. Goodbye!")

else:
    print("Invalid choice. Try again.")
    
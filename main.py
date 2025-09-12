import time
from rich.console import Console
console = Console()

def admin_login():
    print("1. Hello")
    print("2. Bye")

def farmer_login():
    print("1. Siu")
    print("2. oo")


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
    admin_login()
    choice = input("Enter choice: ")
    if choice=="1":
        print("ok")

elif choice == "2":
    for i in range(1,4):
        console.log(f"Doing important stuff...{i}")
        time.sleep(0.25)
    farmer_login()
    choice = input("Enter choice: ")
    if choice=="1":
        print("okk")
elif choice == "3":
    for i in range(1,4):
        console.log(f"Doing important stuff...{i}")
        time.sleep(0.25)
    print("Registration")
elif choice == "4":
    print("Loaded. Goodbye!")

else:
    print("Invalid choice. Try again.")
    

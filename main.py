# main.py
# The main entry point for the application.

from config import console
from admin_module import admin_login
from farmer_module import farmer_login, register_farmer

def main_menu():
    """Displays the main menu and returns the user's choice."""
    console.print("\n== Seasonal Forecast & Agriculture Advisory System ===", style="bold underline black on white")
    print("1. Admin Login")
    print("2. Farmer Login")
    print("3. Register as New Farmer")
    print("4. Exit")
    
    choice = input("Enter choice: ")
    return choice

def run_app():
    """Main application loop."""
    while True:
        choice = main_menu()

        if choice == "1":
            admin_login()
        elif choice == "2":
            farmer_login()
        elif choice == "3":
            register_farmer()
        elif choice == "4":
            console.print("Exiting application... Goodbye!", style="red")
            break  # Exit the main while loop
        else:
            console.print("Invalid choice. Try again.", style="red")
        
   
        """
        # --- Optional: Keep the 'return to menu' prompt ---
        if choice in ('1', '2', '3'):
            again = input("\nReturn to main menu? (y/n): ")
            if again.lower() != "y":
                console.print("Exiting application... Goodbye!", style="red")
                break
        elif choice == '4':
             break # Already exiting
        # ---------------------------------------------------
        """

if __name__ == "__main__":
    run_app()
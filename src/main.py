"""Main entry point for the CLI To-Do List Application."""

import json
import os
from pathlib import Path

from models import AuthManager


# Data file paths
DATA_DIR = Path(__file__).parent.parent / "data"
USERS_FILE = DATA_DIR / "users.json"
TODOS_FILE = DATA_DIR / "todos.json"

# Initialize AuthManager
auth_manager = AuthManager(USERS_FILE)


def ensure_data_files():
    """Ensure data directory and files exist."""
    DATA_DIR.mkdir(exist_ok=True)
    if not USERS_FILE.exists():
        USERS_FILE.write_text(json.dumps([]))
    if not TODOS_FILE.exists():
        TODOS_FILE.write_text(json.dumps([]))


def show_prelogin_menu():
    """Display the pre-login menu and return user's choice."""
    print("\n" + "=" * 40)
    print("Welcome to the To-Do List Application")
    print("=" * 40)
    print("[1] Login")
    print("[2] Sign Up")
    print("[3] Exit")
    print("=" * 40)

    while True:
        choice = input("\nEnter your choice (1-3): ").strip()
        if choice in ["1", "2", "3"]:
            return choice
        print("Invalid choice. Please enter 1, 2, or 3.")


def handle_login():
    """Handle user login."""
    print("\n--- Login ---")
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    success, message = auth_manager.login(username, password)
    if success:
        print(f"\n✓ {message}")
        return username  # Return logged-in username
    else:
        print(f"\n✗ {message}")
        return None


def handle_signup():
    """Handle user sign-up."""
    print("\n--- Sign Up ---")
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    confirm_password = input("Confirm Password: ").strip()

    if not username or not password:
        print("Username and password cannot be empty.")
        return

    if password != confirm_password:
        print("Passwords do not match.")
        return

    success, message = auth_manager.sign_up(username, password)
    if success:
        print(f"\n✓ {message}")
    else:
        print(f"\n✗ {message}")


def main():
    """Main application loop."""
    ensure_data_files()

    while True:
        choice = show_prelogin_menu()

        if choice == "1":
            logged_in_user = handle_login()
            if logged_in_user:
                # TODO: Show post-login menu and handle authenticated operations
                print(f"User {logged_in_user} is now logged in.")
                print("(Post-login menu will be implemented in Task 6)")
        elif choice == "2":
            handle_signup()
        elif choice == "3":
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()

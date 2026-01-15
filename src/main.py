"""Main entry point for the CLI To-Do List Application."""

import json
import os
from pathlib import Path

from models import AuthManager, TodoManager, Priority


# Data file paths
DATA_DIR = Path(__file__).parent.parent / "data"
USERS_FILE = DATA_DIR / "users.json"
TODOS_FILE = DATA_DIR / "todos.json"

# Initialize AuthManager
auth_manager = AuthManager(USERS_FILE)

# Initialize TodoManager
todo_manager = TodoManager(TODOS_FILE)


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


def handle_create_task(username: str) -> None:
    """Handle creation of a new task.
    
    Args:
        username: The currently logged-in user.
    """
    print("\n--- Add New Task ---")
    title = input("Task title: ").strip()
    if not title:
        print("Task title cannot be empty.")
        return

    details = input("Task details: ").strip()
    if not details:
        print("Task details cannot be empty.")
        return

    print("Priority levels: HIGH, MID, LOW")
    priority_input = input("Priority (HIGH/MID/LOW): ").strip().upper()

    try:
        priority = Priority[priority_input]
    except KeyError:
        print(f"Invalid priority '{priority_input}'. Please use HIGH, MID, or LOW.")
        return

    success, message = todo_manager.create_item(
        title=title,
        details=details,
        priority=priority,
        owner=username,
    )

    if success:
        print(f"\n✓ {message}")
    else:
        print(f"\n✗ {message}")


def handle_view_all_tasks(username: str) -> None:
    """Display all tasks for the logged-in user.
    
    Args:
        username: The currently logged-in user.
    """
    print("\n--- Your Tasks ---")
    tasks = todo_manager.view_all(username)

    if not tasks:
        print("You have no tasks yet.")
        return

    print(f"\n{len(tasks)} task(s) found:")
    for idx, (task_id, title) in enumerate(tasks, 1):
        print(f"  {idx}. [{task_id[:8]}...] {title}")


def handle_view_details(username: str) -> None:
    """Display full details of a specific task.
    
    Args:
        username: The currently logged-in user.
    """
    print("\n--- View Task Details ---")
    
    # Get task ID from user
    task_id = input("Enter task ID: ").strip()
    
    success, task = todo_manager.view_details(task_id)
    if not success:
        print("✗ Task not found.")
        return
    
    # Verify ownership
    if task["owner"] != username:
        print("✗ You don't have permission to view this task.")
        return
    
    # Display task details
    print("\n" + "=" * 40)
    print(f"Title:       {task['title']}")
    print(f"Details:     {task['details']}")
    print(f"Priority:    {task['priority']}")
    print(f"Status:      {task['status']}")
    print(f"Owner:       {task['owner']}")
    print(f"Created:     {task['created_at']}")
    print(f"Updated:     {task['updated_at']}")
    print("=" * 40)


def handle_mark_completed(username: str) -> None:
    """Mark a task as completed.
    
    Args:
        username: The currently logged-in user.
    """
    print("\n--- Mark Task as Completed ---")
    
    # Get task ID from user
    task_id = input("Enter task ID: ").strip()
    
    success, task = todo_manager.view_details(task_id)
    if not success:
        print("✗ Task not found.")
        return
    
    # Verify ownership
    if task["owner"] != username:
        print("✗ You don't have permission to modify this task.")
        return
    
    # Check if already completed
    if task["status"] == "COMPLETED":
        print("✗ Task is already completed.")
        return
    
    # Mark as completed
    success, message = todo_manager.mark_as_completed(task_id)
    if success:
        print(f"✓ {message}")
    else:
        print(f"✗ {message}")


def handle_edit_task(username: str) -> None:
    """Edit an existing task.
    
    Args:
        username: The currently logged-in user.
    """
    print("\n--- Edit Task ---")
    
    # Get task ID from user
    task_id = input("Enter task ID: ").strip()
    
    success, task = todo_manager.view_details(task_id)
    if not success:
        print("✗ Task not found.")
        return
    
    # Verify ownership
    if task["owner"] != username:
        print("✗ You don't have permission to modify this task.")
        return
    
    # Collect updates
    print("\nLeave blank to keep current value.")
    new_title = input(f"New title [{task['title']}]: ").strip() or None
    new_details = input(f"New details [{task['details']}]: ").strip() or None
    
    new_priority = None
    if input("Change priority? (y/n): ").strip().lower() == "y":
        print("Priority levels: HIGH, MID, LOW")
        priority_input = input("New priority: ").strip().upper()
        try:
            new_priority = Priority[priority_input]
        except KeyError:
            print(f"Invalid priority '{priority_input}'. Using existing priority.")
    
    # Update task
    success, message = todo_manager.edit_item(
        task_id,
        title=new_title,
        details=new_details,
        priority=new_priority,
    )
    
    if success:
        print(f"✓ {message}")
    else:
        print(f"✗ {message}")


def show_postlogin_menu() -> str:
    """Display the post-login menu and return user's choice."""
    print("\n" + "=" * 40)
    print("Post-Login Menu")
    print("=" * 40)
    print("[1] Add Task")
    print("[2] View All Tasks")
    print("[3] View Task Details")
    print("[4] Edit Task")
    print("[5] Mark Task as Completed")
    print("[6] Logout")
    print("=" * 40)

    while True:
        choice = input("\nEnter your choice (1-6): ").strip()
        if choice in ["1", "2", "3", "4", "5", "6"]:
            return choice
        print("Invalid choice. Please enter 1-6.")


def handle_postlogin_menu(username: str) -> bool:
    """Handle the post-login menu operations.
    
    Args:
        username: The currently logged-in user.
        
    Returns:
        False if user logs out, True to continue the session.
    """
    while True:
        choice = show_postlogin_menu()

        if choice == "1":
            handle_create_task(username)
        elif choice == "2":
            handle_view_all_tasks(username)
        elif choice == "3":
            handle_view_details(username)
        elif choice == "4":
            handle_edit_task(username)
        elif choice == "5":
            handle_mark_completed(username)
        elif choice == "6":
            print(f"\n✓ Logged out successfully. Goodbye, {username}!")
            return False

def main():
    """Main application loop."""
    ensure_data_files()

    while True:
        choice = show_prelogin_menu()

        if choice == "1":
            logged_in_user = handle_login()
            if logged_in_user:
                handle_postlogin_menu(logged_in_user)
        elif choice == "2":
            handle_signup()
        elif choice == "3":
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()


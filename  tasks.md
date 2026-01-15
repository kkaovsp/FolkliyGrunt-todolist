# Project: Python CLI To-Do List Application

## Context & Architecture
We are building a command-line interface (CLI) application for managing to-do lists. The application acts as a REPL (Read-Eval-Print Loop) or interactive shell.
* **Language:** Python 3.10+
* **Data Storage:** Local JSON files (`users.json` for auth, `todos.json` for items).
* **Structure:** Separation of concerns between `AuthManager` (User logic), `TodoManager` (Business logic), and `App` (CLI presentation).

## Data Models

**1. User Schema**
Stored in `users.json`:
`{"username": "...", "password": "..."}`

**2. Todo Schema**
Stored in `todos.json`. Note that `id` must be unique (UUID).
    {
      "id": "uuid-string",
      "title": "String",
      "details": "String",
      "priority": "HIGH | MID | LOW",
      "status": "PENDING | COMPLETED",
      "owner": "username_string",
      "created_at": "ISO-8601 String",
      "updated_at": "ISO-8601 String"
    }

---

## Development Tasks

- [ ] **1. Project Initialization & Data Models**
    - Create `main.py` as the entry point.
    - Create a `models.py` file.
    - Define a `TodoItem` class (using dataclasses or Pydantic) containing the fields defined in the Todo Schema above.
    - Create Python `Enum` classes for Priority (HIGH, MID, LOW) and Status (PENDING, COMPLETED) to ensure consistency.

- [ ] **2. CLI Interface - Basic Interaction**
    - Implement a main application loop.
    - Create a "Pre-Login" menu: Options for [1] Login, [2] Sign Up, [3] Exit.

- [ ] **3. Authentication Logic (AuthManager)**
    - Implement AuthManager class to handle user authentication.
    - **Sign Up:** Create a function to register new users and save them to `users.json`. Check if the username already exists.
    - **Login:** Create a function to verify username/password against `users.json`.
    - Integrate these functions into the "Pre-Login" menu options created in Task 2.

- [ ] **4. Core Logic - Todo Creation & Listing (TodoManager)**
    - Implement TodoManager class to handle business logic.
    - **Create Item:** Implement a function to add a new task. It should prompt for `title`, `details`, and `priority`. Auto-generate id (UUID), status (PENDING), owner (current user), `created_at`, and `updated_at`. Save to `todos.json`.
    - **View All:** Implement a function to list all tasks *belonging to the current logged-in user*. Display basic info (e.g., ID and Title).

- [ ] **5. Core Logic - View Details & Update (TodoManager)**
    - **View Details:** Implement a function to show full details of a specific task (Title, Details, Priority, Status, Owner, Updated date, Created date).
    - **Mark as Completed:** Implement a function to change a task's status to COMPLETED and update `updated_at`.
    - **Edit Item:** Implement a function to modify `title`, `details`, or priority of an existing task. Ensure updated_at is refreshed.

- [ ] **6. Post-Login CLI Menu**
    - Create a "Post-Login" menu shown after successful login.
    - Options:
        1. Add Task
        2. View All Tasks (which then allows selecting a task to View Details, Edit, or Mark Completed)
        3. Logout (return to Pre-Login menu)
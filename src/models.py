"""Data models for the CLI To-Do List Application."""

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Optional
from uuid import uuid4


class Priority(Enum):
    """Priority levels for to-do items."""

    HIGH = "HIGH"
    MID = "MID"
    LOW = "LOW"


class Status(Enum):
    """Status values for to-do items."""

    PENDING = "PENDING"
    COMPLETED = "COMPLETED"


@dataclass
class TodoItem:
    """Represents a single to-do item."""

    title: str
    details: str
    priority: Priority
    owner: str
    id: str = field(default_factory=lambda: str(uuid4()))
    status: Status = field(default=Status.PENDING)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> dict:
        """Convert TodoItem to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "title": self.title,
            "details": self.details,
            "priority": self.priority.value,
            "status": self.status.value,
            "owner": self.owner,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "TodoItem":
        """Create TodoItem from dictionary (e.g., from JSON)."""
        return cls(
            id=data["id"],
            title=data["title"],
            details=data["details"],
            priority=Priority(data["priority"]),
            status=Status(data["status"]),
            owner=data["owner"],
            created_at=data["created_at"],
            updated_at=data["updated_at"],
        )


class AuthManager:
    """Manages user authentication operations."""

    def __init__(self, users_file: Path):
        """Initialize AuthManager with path to users JSON file.
        
        Args:
            users_file: Path to the users.json file.
        """
        self.users_file = users_file

    def _hash_password(self, password: str) -> str:
        """Hash a password using SHA-256.
        
        Args:
            password: Plain text password to hash.
            
        Returns:
            Hashed password as a hex string.
        """
        return hashlib.sha256(password.encode()).hexdigest()

    def _load_users(self) -> list:
        """Load users from JSON file.
        
        Returns:
            List of user dictionaries.
        """
        if not self.users_file.exists():
            return []
        try:
            with open(self.users_file, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    def _save_users(self, users: list) -> None:
        """Save users to JSON file.
        
        Args:
            users: List of user dictionaries to save.
        """
        self.users_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.users_file, "w") as f:
            json.dump(users, f, indent=2)

    def user_exists(self, username: str) -> bool:
        """Check if a username already exists.
        
        Args:
            username: Username to check.
            
        Returns:
            True if username exists, False otherwise.
        """
        users = self._load_users()
        return any(user["username"] == username for user in users)

    def sign_up(self, username: str, password: str) -> tuple[bool, str]:
        """Register a new user.
        
        Args:
            username: Username for the new account.
            password: Password for the new account.
            
        Returns:
            Tuple of (success: bool, message: str).
        """
        if not username or not password:
            return False, "Username and password cannot be empty."

        if self.user_exists(username):
            return False, f"Username '{username}' already exists."

        users = self._load_users()
        new_user = {
            "username": username,
            "password": self._hash_password(password),
        }
        users.append(new_user)
        self._save_users(users)
        return True, f"User '{username}' registered successfully."

    def login(self, username: str, password: str) -> tuple[bool, str]:
        """Verify user credentials.
        
        Args:
            username: Username to authenticate.
            password: Password to verify.
            
        Returns:
            Tuple of (success: bool, message: str).
        """
        users = self._load_users()
        hashed_password = self._hash_password(password)

        for user in users:
            if user["username"] == username:
                if user["password"] == hashed_password:
                    return True, f"Welcome back, {username}!"
                else:
                    return False, "Invalid password."

        return False, f"User '{username}' not found."


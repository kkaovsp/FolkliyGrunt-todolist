"""Unit tests for src/main.py functionality."""

import json
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from io import StringIO

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from main import (
    ensure_data_files,
    handle_login,
    handle_signup,
    handle_create_task,
    handle_view_all_tasks,
    handle_view_details,
    handle_mark_completed,
    handle_edit_task,
    show_prelogin_menu,
    show_postlogin_menu,
)
from models import Priority


@pytest.fixture
def temp_data_dir(tmp_path):
    """Create a temporary data directory for testing."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    users_file = data_dir / "users.json"
    todos_file = data_dir / "todos.json"
    users_file.write_text(json.dumps([]))
    todos_file.write_text(json.dumps([]))
    return data_dir, users_file, todos_file


@pytest.fixture
def mock_managers(temp_data_dir, monkeypatch):
    """Mock the AuthManager and TodoManager with temp files."""
    data_dir, users_file, todos_file = temp_data_dir
    
    # Patch the file paths in main module
    import main
    monkeypatch.setattr(main, "DATA_DIR", data_dir)
    monkeypatch.setattr(main, "USERS_FILE", users_file)
    monkeypatch.setattr(main, "TODOS_FILE", todos_file)
    
    # Reinitialize managers with temp files
    from models import AuthManager, TodoManager
    main.auth_manager = AuthManager(users_file)
    main.todo_manager = TodoManager(todos_file)
    
    return main.auth_manager, main.todo_manager


class TestEnsureDataFiles:
    """Test data file initialization."""

    def test_ensure_data_files_creates_directory(self, tmp_path, monkeypatch):
        """Test that ensure_data_files creates the data directory."""
        import main
        data_dir = tmp_path / "data"
        monkeypatch.setattr(main, "DATA_DIR", data_dir)
        
        assert not data_dir.exists()
        ensure_data_files()
        assert data_dir.exists()

    def test_ensure_data_files_creates_users_file(self, tmp_path, monkeypatch):
        """Test that ensure_data_files creates the users.json file."""
        import main
        data_dir = tmp_path / "data"
        users_file = data_dir / "users.json"
        monkeypatch.setattr(main, "DATA_DIR", data_dir)
        monkeypatch.setattr(main, "USERS_FILE", users_file)
        
        ensure_data_files()
        assert users_file.exists()
        assert json.loads(users_file.read_text()) == []

    def test_ensure_data_files_creates_todos_file(self, tmp_path, monkeypatch):
        """Test that ensure_data_files creates the todos.json file."""
        import main
        data_dir = tmp_path / "data"
        todos_file = data_dir / "todos.json"
        monkeypatch.setattr(main, "DATA_DIR", data_dir)
        monkeypatch.setattr(main, "TODOS_FILE", todos_file)
        
        ensure_data_files()
        assert todos_file.exists()
        assert json.loads(todos_file.read_text()) == []


class TestPreloginMenu:
    """Test pre-login menu functionality."""

    @patch("builtins.input", side_effect=["1"])
    @patch("builtins.print")
    def test_show_prelogin_menu_login_choice(self, mock_print, mock_input):
        """Test that prelogin menu returns '1' for login."""
        result = show_prelogin_menu()
        assert result == "1"

    @patch("builtins.input", side_effect=["2"])
    @patch("builtins.print")
    def test_show_prelogin_menu_signup_choice(self, mock_print, mock_input):
        """Test that prelogin menu returns '2' for signup."""
        result = show_prelogin_menu()
        assert result == "2"

    @patch("builtins.input", side_effect=["3"])
    @patch("builtins.print")
    def test_show_prelogin_menu_exit_choice(self, mock_print, mock_input):
        """Test that prelogin menu returns '3' for exit."""
        result = show_prelogin_menu()
        assert result == "3"

    @patch("builtins.input", side_effect=["invalid", "1"])
    @patch("builtins.print")
    def test_show_prelogin_menu_invalid_choice(self, mock_print, mock_input):
        """Test that prelogin menu handles invalid input."""
        result = show_prelogin_menu()
        assert result == "1"
        # Check that error message was printed
        assert any("Invalid" in str(call) for call in mock_print.call_args_list)


class TestLogin:
    """Test login functionality."""

    @patch("builtins.input", side_effect=["testuser", "password123"])
    @patch("builtins.print")
    def test_handle_login_success(self, mock_print, mock_input, mock_managers):
        """Test successful login."""
        auth_manager, _ = mock_managers
        
        # Create a user first
        auth_manager.sign_up("testuser", "password123")
        
        result = handle_login()
        assert result == "testuser"

    @patch("builtins.input", side_effect=["testuser", "wrongpassword"])
    @patch("builtins.print")
    def test_handle_login_wrong_password(self, mock_print, mock_input, mock_managers):
        """Test login with wrong password."""
        auth_manager, _ = mock_managers
        
        # Create a user first
        auth_manager.sign_up("testuser", "password123")
        
        result = handle_login()
        assert result is None

    @patch("builtins.input", side_effect=["nonexistent", "password"])
    @patch("builtins.print")
    def test_handle_login_user_not_found(self, mock_print, mock_input, mock_managers):
        """Test login with non-existent user."""
        result = handle_login()
        assert result is None


class TestSignup:
    """Test signup functionality."""

    @patch("builtins.input", side_effect=["newuser", "password123", "password123"])
    @patch("builtins.print")
    def test_handle_signup_success(self, mock_print, mock_input, mock_managers):
        """Test successful signup."""
        auth_manager, _ = mock_managers
        
        handle_signup()
        
        # Verify user was created
        assert auth_manager.user_exists("newuser")

    @patch("builtins.input", side_effect=["newuser", "password123", "different"])
    @patch("builtins.print")
    def test_handle_signup_password_mismatch(self, mock_print, mock_input, mock_managers):
        """Test signup with mismatched passwords."""
        auth_manager, _ = mock_managers
        
        handle_signup()
        
        # Verify user was not created
        assert not auth_manager.user_exists("newuser")

    @patch("builtins.input", side_effect=["", "password", "password"])
    @patch("builtins.print")
    def test_handle_signup_empty_username(self, mock_print, mock_input, mock_managers):
        """Test signup with empty username."""
        auth_manager, _ = mock_managers
        
        handle_signup()
        
        # Verify error message was printed
        assert any("empty" in str(call).lower() for call in mock_print.call_args_list)

    @patch("builtins.input", side_effect=["testuser", "password123", "password123"])
    @patch("builtins.print")
    def test_handle_signup_duplicate_user(self, mock_print, mock_input, mock_managers):
        """Test signup with duplicate username."""
        auth_manager, _ = mock_managers
        
        # Create first user
        auth_manager.sign_up("testuser", "password123")
        
        # Try to create duplicate
        handle_signup()
        
        # Verify error message was printed
        assert any("already exists" in str(call) for call in mock_print.call_args_list)


class TestCreateTask:
    """Test task creation functionality."""

    @patch("builtins.input", side_effect=["Task Title", "Task Details", "HIGH"])
    @patch("builtins.print")
    def test_handle_create_task_success(self, mock_print, mock_input, mock_managers):
        """Test successful task creation."""
        _, todo_manager = mock_managers
        
        handle_create_task("testuser")
        
        # Verify task was created
        tasks = todo_manager.view_all("testuser")
        assert len(tasks) == 1
        assert tasks[0][1] == "Task Title"

    @patch("builtins.input", side_effect=["", "Details", "HIGH"])
    @patch("builtins.print")
    def test_handle_create_task_empty_title(self, mock_print, mock_input, mock_managers):
        """Test task creation with empty title."""
        _, todo_manager = mock_managers
        
        handle_create_task("testuser")
        
        # Verify task was not created
        tasks = todo_manager.view_all("testuser")
        assert len(tasks) == 0

    @patch("builtins.input", side_effect=["Task Title", "", "HIGH"])
    @patch("builtins.print")
    def test_handle_create_task_empty_details(self, mock_print, mock_input, mock_managers):
        """Test task creation with empty details."""
        _, todo_manager = mock_managers
        
        handle_create_task("testuser")
        
        # Verify task was not created
        tasks = todo_manager.view_all("testuser")
        assert len(tasks) == 0

    @patch("builtins.input", side_effect=["Task Title", "Task Details", "INVALID"])
    @patch("builtins.print")
    def test_handle_create_task_invalid_priority(self, mock_print, mock_input, mock_managers):
        """Test task creation with invalid priority."""
        _, todo_manager = mock_managers
        
        handle_create_task("testuser")
        
        # Verify task was not created
        tasks = todo_manager.view_all("testuser")
        assert len(tasks) == 0

    @patch("builtins.input", side_effect=["Task Title", "Task Details", "MID"])
    @patch("builtins.print")
    def test_handle_create_task_mid_priority(self, mock_print, mock_input, mock_managers):
        """Test task creation with MID priority."""
        _, todo_manager = mock_managers
        
        handle_create_task("testuser")
        
        tasks = todo_manager.view_all("testuser")
        assert len(tasks) == 1

    @patch("builtins.input", side_effect=["Task Title", "Task Details", "LOW"])
    @patch("builtins.print")
    def test_handle_create_task_low_priority(self, mock_print, mock_input, mock_managers):
        """Test task creation with LOW priority."""
        _, todo_manager = mock_managers
        
        handle_create_task("testuser")
        
        tasks = todo_manager.view_all("testuser")
        assert len(tasks) == 1


class TestViewAllTasks:
    """Test viewing all tasks functionality."""

    @patch("builtins.print")
    def test_handle_view_all_tasks_empty(self, mock_print, mock_managers):
        """Test viewing tasks when user has none."""
        handle_view_all_tasks("testuser")
        
        # Verify "no tasks" message was printed
        assert any("no tasks" in str(call).lower() for call in mock_print.call_args_list)

    @patch("builtins.input", side_effect=["Task 1", "Details 1", "HIGH", "Task 2", "Details 2", "LOW"])
    @patch("builtins.print")
    def test_handle_view_all_tasks_with_tasks(self, mock_print, mock_input, mock_managers):
        """Test viewing tasks when user has multiple tasks."""
        _, todo_manager = mock_managers
        
        # Create two tasks
        handle_create_task("testuser")
        handle_create_task("testuser")
        
        # View tasks
        handle_view_all_tasks("testuser")
        
        # Verify task count message includes "2 task"
        assert any("2 task" in str(call) for call in mock_print.call_args_list)

    @patch("builtins.input", side_effect=["Task 1", "Details 1", "HIGH"])
    @patch("builtins.print")
    def test_handle_view_all_tasks_filters_by_owner(self, mock_print, mock_input, mock_managers):
        """Test that view_all_tasks only shows user's tasks."""
        _, todo_manager = mock_managers
        
        # Create task for testuser
        handle_create_task("testuser")
        
        # View tasks for different user
        handle_view_all_tasks("otheruser")
        
        # Verify "no tasks" message was printed
        assert any("no tasks" in str(call).lower() for call in mock_print.call_args_list)


class TestViewDetails:
    """Test viewing task details functionality."""

    @patch("builtins.input", side_effect=["Task Title", "Task Details", "HIGH", "invalid-id"])
    @patch("builtins.print")
    def test_handle_view_details_task_not_found(self, mock_print, mock_input, mock_managers):
        """Test viewing details of non-existent task."""
        handle_create_task("testuser")
        handle_view_details("testuser")
        
        # Verify "task not found" message
        assert any("not found" in str(call).lower() for call in mock_print.call_args_list)

    @patch("builtins.input", side_effect=["Task Title", "Task Details", "HIGH"])
    @patch("builtins.print")
    def test_handle_view_details_success(self, mock_print, mock_input, mock_managers):
        """Test successful task detail viewing."""
        _, todo_manager = mock_managers
        
        # Create task
        handle_create_task("testuser")
        
        # Get task ID
        tasks = todo_manager.view_all("testuser")
        task_id = tasks[0][0]
        
        # View details with correct task ID
        with patch("builtins.input", return_value=task_id):
            handle_view_details("testuser")
            
        # Verify task details were printed
        assert any("Title:" in str(call) for call in mock_print.call_args_list)
        assert any("Task Title" in str(call) for call in mock_print.call_args_list)

    @patch("builtins.input", side_effect=["Task Title", "Task Details", "HIGH"])
    @patch("builtins.print")
    def test_handle_view_details_permission_denied(self, mock_print, mock_input, mock_managers):
        """Test viewing task details for another user's task."""
        _, todo_manager = mock_managers
        
        # Create task for testuser
        handle_create_task("testuser")
        
        # Get task ID
        tasks = todo_manager.view_all("testuser")
        task_id = tasks[0][0]
        
        # Try to view as different user
        with patch("builtins.input", return_value=task_id):
            handle_view_details("otheruser")
            
        # Verify permission error message
        assert any("permission" in str(call).lower() for call in mock_print.call_args_list)


class TestMarkCompleted:
    """Test marking tasks as completed functionality."""

    @patch("builtins.input", side_effect=["Task Title", "Task Details", "HIGH"])
    @patch("builtins.print")
    def test_handle_mark_completed_success(self, mock_print, mock_input, mock_managers):
        """Test successfully marking a task as completed."""
        _, todo_manager = mock_managers
        
        # Create task
        handle_create_task("testuser")
        
        # Get task ID
        tasks = todo_manager.view_all("testuser")
        task_id = tasks[0][0]
        
        # Mark as completed
        with patch("builtins.input", return_value=task_id):
            handle_mark_completed("testuser")
        
        # Verify task status changed
        success, task = todo_manager.view_details(task_id)
        assert task["status"] == "COMPLETED"

    @patch("builtins.input", side_effect=["invalid-id"])
    @patch("builtins.print")
    def test_handle_mark_completed_task_not_found(self, mock_print, mock_input, mock_managers):
        """Test marking non-existent task as completed."""
        handle_mark_completed("testuser")
        
        # Verify "task not found" message
        assert any("not found" in str(call).lower() for call in mock_print.call_args_list)

    @patch("builtins.input", side_effect=["Task Title", "Task Details", "HIGH"])
    @patch("builtins.print")
    def test_handle_mark_completed_permission_denied(self, mock_print, mock_input, mock_managers):
        """Test marking another user's task as completed."""
        _, todo_manager = mock_managers
        
        # Create task for testuser
        handle_create_task("testuser")
        
        # Get task ID
        tasks = todo_manager.view_all("testuser")
        task_id = tasks[0][0]
        
        # Try to mark as completed with different user
        with patch("builtins.input", return_value=task_id):
            handle_mark_completed("otheruser")
        
        # Verify permission error message
        assert any("permission" in str(call).lower() for call in mock_print.call_args_list)

    @patch("builtins.input", side_effect=["Task Title", "Task Details", "HIGH"])
    @patch("builtins.print")
    def test_handle_mark_completed_already_completed(self, mock_print, mock_input, mock_managers):
        """Test marking already completed task as completed."""
        _, todo_manager = mock_managers
        
        # Create and complete task
        handle_create_task("testuser")
        tasks = todo_manager.view_all("testuser")
        task_id = tasks[0][0]
        
        with patch("builtins.input", return_value=task_id):
            handle_mark_completed("testuser")
        
        # Try to mark as completed again
        with patch("builtins.input", return_value=task_id):
            handle_mark_completed("testuser")
        
        # Verify "already completed" message
        assert any("already completed" in str(call).lower() for call in mock_print.call_args_list)


class TestEditTask:
    """Test editing task functionality."""

    @patch("builtins.input", side_effect=["Task Title", "Task Details", "HIGH"])
    @patch("builtins.print")
    def test_handle_edit_task_success(self, mock_print, mock_input, mock_managers):
        """Test successfully editing a task."""
        _, todo_manager = mock_managers
        
        # Create task
        handle_create_task("testuser")
        
        # Get task ID
        tasks = todo_manager.view_all("testuser")
        task_id = tasks[0][0]
        
        # Edit task
        with patch("builtins.input", side_effect=[task_id, "New Title", "New Details", "n"]):
            handle_edit_task("testuser")
        
        # Verify task was updated
        success, task = todo_manager.view_details(task_id)
        assert task["title"] == "New Title"
        assert task["details"] == "New Details"

    @patch("builtins.input", side_effect=["invalid-id"])
    @patch("builtins.print")
    def test_handle_edit_task_not_found(self, mock_print, mock_input, mock_managers):
        """Test editing non-existent task."""
        handle_edit_task("testuser")
        
        # Verify "task not found" message
        assert any("not found" in str(call).lower() for call in mock_print.call_args_list)

    @patch("builtins.input", side_effect=["Task Title", "Task Details", "HIGH"])
    @patch("builtins.print")
    def test_handle_edit_task_permission_denied(self, mock_print, mock_input, mock_managers):
        """Test editing another user's task."""
        _, todo_manager = mock_managers
        
        # Create task for testuser
        handle_create_task("testuser")
        
        # Get task ID
        tasks = todo_manager.view_all("testuser")
        task_id = tasks[0][0]
        
        # Try to edit as different user
        with patch("builtins.input", return_value=task_id):
            handle_edit_task("otheruser")
        
        # Verify permission error message
        assert any("permission" in str(call).lower() for call in mock_print.call_args_list)

    @patch("builtins.input", side_effect=["Task Title", "Task Details", "HIGH"])
    @patch("builtins.print")
    def test_handle_edit_task_priority_change(self, mock_print, mock_input, mock_managers):
        """Test editing task with priority change."""
        _, todo_manager = mock_managers
        
        # Create task
        handle_create_task("testuser")
        
        # Get task ID
        tasks = todo_manager.view_all("testuser")
        task_id = tasks[0][0]
        
        # Edit task with priority change
        with patch("builtins.input", side_effect=[task_id, "", "", "y", "LOW"]):
            handle_edit_task("testuser")
        
        # Verify priority was updated
        success, task = todo_manager.view_details(task_id)
        assert task["priority"] == "LOW"

    @patch("builtins.input", side_effect=["Task Title", "Task Details", "HIGH"])
    @patch("builtins.print")
    def test_handle_edit_task_keep_current_values(self, mock_print, mock_input, mock_managers):
        """Test editing task while keeping current values."""
        _, todo_manager = mock_managers
        
        # Create task
        handle_create_task("testuser")
        
        # Get task ID
        tasks = todo_manager.view_all("testuser")
        task_id = tasks[0][0]
        original_task = todo_manager.view_details(task_id)[1]
        
        # Edit task without changing anything
        with patch("builtins.input", side_effect=[task_id, "", "", "n"]):
            handle_edit_task("testuser")
        
        # Verify task values remain the same
        updated_task = todo_manager.view_details(task_id)[1]
        assert updated_task["title"] == original_task["title"]
        assert updated_task["details"] == original_task["details"]


class TestPostloginMenu:
    """Test post-login menu functionality."""

    @patch("builtins.input", side_effect=["1"])
    @patch("builtins.print")
    def test_show_postlogin_menu_add_task(self, mock_print, mock_input):
        """Test post-login menu returns '1' for add task."""
        result = show_postlogin_menu()
        assert result == "1"

    @patch("builtins.input", side_effect=["2"])
    @patch("builtins.print")
    def test_show_postlogin_menu_view_all(self, mock_print, mock_input):
        """Test post-login menu returns '2' for view all tasks."""
        result = show_postlogin_menu()
        assert result == "2"

    @patch("builtins.input", side_effect=["3"])
    @patch("builtins.print")
    def test_show_postlogin_menu_view_details(self, mock_print, mock_input):
        """Test post-login menu returns '3' for view details."""
        result = show_postlogin_menu()
        assert result == "3"

    @patch("builtins.input", side_effect=["4"])
    @patch("builtins.print")
    def test_show_postlogin_menu_edit_task(self, mock_print, mock_input):
        """Test post-login menu returns '4' for edit task."""
        result = show_postlogin_menu()
        assert result == "4"

    @patch("builtins.input", side_effect=["5"])
    @patch("builtins.print")
    def test_show_postlogin_menu_mark_completed(self, mock_print, mock_input):
        """Test post-login menu returns '5' for mark completed."""
        result = show_postlogin_menu()
        assert result == "5"

    @patch("builtins.input", side_effect=["6"])
    @patch("builtins.print")
    def test_show_postlogin_menu_logout(self, mock_print, mock_input):
        """Test post-login menu returns '6' for logout."""
        result = show_postlogin_menu()
        assert result == "6"

    @patch("builtins.input", side_effect=["invalid", "2"])
    @patch("builtins.print")
    def test_show_postlogin_menu_invalid_choice(self, mock_print, mock_input):
        """Test that post-login menu handles invalid input."""
        result = show_postlogin_menu()
        assert result == "2"
        # Check that error message was printed
        assert any("Invalid" in str(call) for call in mock_print.call_args_list)

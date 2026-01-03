#!/usr/bin/env python3
"""
Console-based Todo Application
Phase I - In-Memory Python Console Todo App
"""

import sys
from typing import Dict, List, Optional


class Task:
    """Represents a single task in the todo list."""
    
    def __init__(self, task_id: int, description: str, completed: bool = False):
        self.id = task_id
        self.description = description
        self.completed = completed
    
    def __str__(self):
        status = "✓" if self.completed else "○"
        return f"[{status}] {self.id}: {self.description}"


class TodoApp:
    """Main Todo Application class."""
    
    def __init__(self):
        self.tasks: Dict[int, Task] = {}
        self.next_id = 1
    
    def add_task(self, description: str) -> str:
        """Add a new task with the given description."""
        if not description.strip():
            return "Error: Task description cannot be empty."
        
        task = Task(self.next_id, description.strip())
        self.tasks[self.next_id] = task
        task_id = self.next_id
        self.next_id += 1
        return f"Task {task_id} added successfully."
    
    def view_tasks(self) -> str:
        """Return a string representation of all tasks."""
        if not self.tasks:
            return "No tasks in the list."
        
        task_list = []
        for task_id in sorted(self.tasks.keys()):
            task_list.append(str(self.tasks[task_id]))
        
        return "\n".join(task_list)
    
    def update_task(self, task_id: int, new_description: str) -> str:
        """Update the description of an existing task."""
        if task_id not in self.tasks:
            return f"Error: Task with ID {task_id} does not exist."
        
        if not new_description.strip():
            return "Error: Task description cannot be empty."
        
        self.tasks[task_id].description = new_description.strip()
        return f"Task {task_id} updated successfully."
    
    def delete_task(self, task_id: int) -> str:
        """Delete a task by its ID."""
        if task_id not in self.tasks:
            return f"Error: Task with ID {task_id} does not exist."
        
        del self.tasks[task_id]
        return f"Task {task_id} deleted successfully."
    
    def mark_complete(self, task_id: int) -> str:
        """Mark a task as complete."""
        if task_id not in self.tasks:
            return f"Error: Task with ID {task_id} does not exist."
        
        self.tasks[task_id].completed = True
        return f"Task {task_id} marked as complete."
    
    def mark_incomplete(self, task_id: int) -> str:
        """Mark a task as incomplete."""
        if task_id not in self.tasks:
            return f"Error: Task with ID {task_id} does not exist."
        
        self.tasks[task_id].completed = False
        return f"Task {task_id} marked as incomplete."


def print_help():
    """Print help information for the application."""
    help_text = """
Todo Application Help
=====================

Available Commands:
  add <description>     - Add a new task
  view                  - View all tasks
  update <id> <desc>    - Update task description
  delete <id>           - Delete a task
  complete <id>         - Mark task as complete
  incomplete <id>       - Mark task as incomplete
  help                  - Show this help message
  quit                  - Exit the application

Examples:
  add Buy groceries
  update 1 Buy milk and eggs
  complete 2
"""
    print(help_text)


def main():
    """Main application loop."""
    app = TodoApp()
    print("Welcome to the Todo Application!")
    print("Type 'help' for available commands or 'quit' to exit.")
    
    while True:
        try:
            # Get user input
            user_input = input("\n> ").strip()
            
            if not user_input:
                continue
            
            # Parse command
            parts = user_input.split(maxsplit=1)
            command = parts[0].lower()
            
            # Handle different commands
            if command == "quit":
                print("Thank you for using the Todo Application. Goodbye!")
                break
            elif command == "help":
                print_help()
            elif command == "add":
                if len(parts) < 2:
                    print("Error: Please provide a task description. Usage: add <description>")
                else:
                    result = app.add_task(parts[1])
                    print(result)
            elif command == "view":
                print(app.view_tasks())
            elif command == "update":
                if len(parts) < 2:
                    print("Error: Please provide task ID and new description. Usage: update <id> <description>")
                else:
                    # Split the remaining part to get ID and new description
                    update_parts = parts[1].split(maxsplit=1)
                    if len(update_parts) < 2:
                        print("Error: Please provide both task ID and new description. Usage: update <id> <description>")
                    else:
                        try:
                            task_id = int(update_parts[0])
                            new_desc = update_parts[1]
                            result = app.update_task(task_id, new_desc)
                            print(result)
                        except ValueError:
                            print("Error: Task ID must be a number.")
            elif command == "delete":
                if len(parts) < 2:
                    print("Error: Please provide task ID. Usage: delete <id>")
                else:
                    try:
                        task_id = int(parts[1])
                        result = app.delete_task(task_id)
                        print(result)
                    except ValueError:
                        print("Error: Task ID must be a number.")
            elif command == "complete":
                if len(parts) < 2:
                    print("Error: Please provide task ID. Usage: complete <id>")
                else:
                    try:
                        task_id = int(parts[1])
                        result = app.mark_complete(task_id)
                        print(result)
                    except ValueError:
                        print("Error: Task ID must be a number.")
            elif command == "incomplete":
                if len(parts) < 2:
                    print("Error: Please provide task ID. Usage: incomplete <id>")
                else:
                    try:
                        task_id = int(parts[1])
                        result = app.mark_incomplete(task_id)
                        print(result)
                    except ValueError:
                        print("Error: Task ID must be a number.")
            else:
                print(f"Unknown command: {command}. Type 'help' for available commands.")
                
        except KeyboardInterrupt:
            print("\n\nReceived interrupt signal. Exiting...")
            break
        except EOFError:
            print("\n\nEnd of input received. Exiting...")
            break


if __name__ == "__main__":
    main()
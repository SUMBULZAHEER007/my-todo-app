# Phase I – Todo App

## Overview
A simple in-memory Python console Todo app that allows users to manage tasks through a command-line interface.

## Features
1. Add Task - Add tasks with title and optional description
2. View Tasks - Show all tasks with status (completed / pending)
3. Update Task - Update title or description of existing tasks
4. Delete Task - Delete tasks by ID
5. Mark Task as Complete / Incomplete - Change completion status of tasks

## Requirements
- Python 3.13+

## How to Run
1. Make sure you have Python 3.13+ installed
2. Clone or download this repository
3. Navigate to the project directory
4. Run the application:
   ```bash
   python todo_app_phase1.py
   ```

## Available Commands
- `add <title> [description]` - Add a new task
- `view` - View all tasks
- `update <id> <title> [desc]` - Update task title and/or description
- `delete <id]` - Delete a task
- `complete <id>` - Mark task as complete
- `incomplete <id>` - Mark task as incomplete
- `help` - Show help information
- `quit` - Exit the application

## Examples
```
> add Buy groceries
Task 1 added successfully.

> add Buy groceries "Milk, eggs, bread"
Task 2 added successfully.

> view
[○] 1: Buy groceries
[○] 2: Buy groceries - Milk, eggs, bread

> complete 1
Task 1 marked as complete.

> view
[✓] 1: Buy groceries
[○] 2: Buy groceries - Milk, eggs, bread

> update 2 Buy milk and eggs
Task 2 updated successfully.

> view
[✓] 1: Buy groceries
[○] 2: Buy milk and eggs - Milk, eggs, bread

> delete 1
Task 1 deleted successfully.

> view
[○] 2: Buy milk and eggs - Milk, eggs, bread

> quit
Thank you for using the Todo Application. Goodbye!
```

## Notes
- All data is stored in memory only and will be lost when the application exits
- Each task has a unique ID assigned automatically
- The application validates inputs and provides error messages for invalid commands or operations
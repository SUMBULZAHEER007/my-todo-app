# test_ai_endpoints.py
import requests
import json

# Base URL for the API
BASE_URL = "http://127.0.0.1:8000"

def test_chat_endpoint():
    """Test the chat endpoint"""
    print("Testing Chat Endpoint...")

    # First, let's create a few tasks to provide context
    todo_data = {"description": "Buy groceries", "completed": False}
    response = requests.post(f"{BASE_URL}/todos", json=todo_data)
    print(f"Created task: {response.json()}")

    todo_data = {"description": "Walk the dog", "completed": True}
    response = requests.post(f"{BASE_URL}/todos", json=todo_data)
    print(f"Created task: {response.json()}")

    # Now test the chat endpoint
    query = "What tasks have I completed?"
    response = requests.post(f"{BASE_URL}/api/chat", json={"query": query})

    if response.status_code == 200:
        print("Chat Endpoint Response:")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Error: {response.status_code} - {response.text}")


def test_task_summary():
    """Test the task summary endpoint"""
    print("\nTesting Task Summary Endpoint...")

    response = requests.post(f"{BASE_URL}/api/tasks/summary")

    if response.status_code == 200:
        print("Task Summary Response:")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Error: {response.status_code} - {response.text}")


def test_basic_todo_operations():
    """Test basic todo operations to ensure they still work"""
    print("\nTesting Basic Todo Operations...")

    # Test creating a task
    todo_data = {"description": "Test task for API", "completed": False}
    response = requests.post(f"{BASE_URL}/todos", json=todo_data)
    print(f"Created task: {response.json()}")

    # Test getting all tasks
    response = requests.get(f"{BASE_URL}/todos")
    print(f"All tasks: {response.json()}")

    # Get the ID of the task we just created
    if response.json():
        task_id = response.json()[0]['id']

        # Test updating the task
        update_data = {"description": "Updated test task", "completed": True}
        response = requests.put(f"{BASE_URL}/todos/{task_id}", json=update_data)
        print(f"Updated task: {response.json()}")

        # Test deleting the task
        response = requests.delete(f"{BASE_URL}/todos/{task_id}")
        print(f"Deleted task: Status {response.status_code}")


if __name__ == "__main__":
    print("Starting tests for Phase III AI Integration...")

    # Make sure the server is running before testing
    try:
        # Test basic functionality first
        test_basic_todo_operations()

        # Test AI endpoints
        test_chat_endpoint()
        test_task_summary()

        print("\nAll tests completed!")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Please make sure the FastAPI server is running on http://127.0.0.1:8000")
    except Exception as e:
        print(f"An error occurred during testing: {str(e)}")
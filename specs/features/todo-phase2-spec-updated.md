# Phase II Specification: Persistent API-Based Todo Application

## 1. Overview

### Purpose of Phase II
Phase II aims to evolve the existing in-memory console Todo application into a persistent, API-driven backend service. This phase maintains all functionality from Phase I while adding data persistence and a RESTful API interface to enable broader integration and multi-user access.

### What problems Phase II solves compared to Phase I
- **Data Loss**: Phase I data was lost when the application terminated; Phase II provides persistent storage that survives application restarts.
- **Limited Access**: Phase I was console-only; Phase II provides an API for programmatic access from multiple clients.
- **Scalability**: Phase I was single-user only; Phase II enables multi-user access through the API.
- **Integration**: Phase I couldn't integrate with other applications; Phase II provides a service that other applications can consume.

## 2. Changes from Phase I

### What remains the same
- Core task management functionality (create, read, update, delete, mark complete/incomplete)
- Task data structure (ID, description, completion status)
- Business logic for task operations
- Validation rules for task operations

### What is newly introduced
- Persistent storage mechanism to maintain data between application runs
- RESTful API endpoints for all task operations
- HTTP-based communication instead of console interaction
- Support for multiple concurrent users accessing the service
- JSON request/response format

## 3. Functional Requirements

### Create Todo
- The system shall allow users to create new todos via an API endpoint
- The system shall assign a unique identifier to each new todo automatically
- The system shall store the new todo in persistent storage
- The system shall return the created todo with its unique identifier

### Read Todos (list + single)
- The system shall provide an endpoint to retrieve all todos from persistent storage
- The system shall provide an endpoint to retrieve a specific todo by its unique identifier
- The system shall return todos in a structured format (JSON)

### Update Todo
- The system shall allow users to update the description of an existing todo via an API endpoint
- The system shall identify todos by their unique identifier
- The system shall update the todo in persistent storage
- The system shall return the updated todo

### Delete Todo
- The system shall allow users to delete a todo by its unique identifier via an API endpoint
- The system shall remove the todo from persistent storage
- The system shall return a confirmation of successful deletion

### Mark Todo complete / incomplete
- The system shall allow users to change the completion status of a todo via an API endpoint
- The system shall identify todos by their unique identifier
- The system shall update the completion status in persistent storage
- The system shall return the updated todo with its new status

## 4. Non-Functional Requirements

### Data persistence
- All todos must be stored in a persistent storage mechanism
- Data must survive application restarts and system failures
- Storage must maintain data integrity during concurrent access

### API-based interaction
- The system must provide RESTful API endpoints for all operations
- The system must handle multiple concurrent API requests
- The system must return appropriate HTTP status codes for all responses
- The system must use JSON format for request and response payloads

### Basic validation
- The system must validate incoming requests and return appropriate error responses
- The system must validate that required fields are present
- The system must validate that operations are performed on existing todos
- The system must prevent invalid data from being stored

## 5. Data Model (Conceptual)

### Todo
- Unique Identifier: A unique value to identify each todo (persisted)
- Description: The text describing what the todo is (persisted)
- Completion Status: Boolean value indicating if the todo is complete (true) or incomplete (false) (persisted)
- Creation Timestamp: When the todo was created (persisted)
- Update Timestamp: When the todo was last modified (persisted)

### Persistence concept
- Todos are stored in a persistent storage mechanism (file-based or database)
- Storage maintains data between application restarts
- Storage supports concurrent read/write operations safely

## 6. API Contract (High-Level)

### POST /todos
- Create a new todo
- Request intent: Provide todo description
- Response intent: Return created todo with unique identifier

### GET /todos
- Retrieve all todos
- Request intent: No specific parameters required
- Response intent: Return list of all todos

### GET /todos/{id}
- Retrieve a specific todo by ID
- Request intent: Provide unique identifier
- Response intent: Return specific todo details

### PUT /todos/{id}
- Update an existing todo
- Request intent: Provide unique identifier and updated description
- Response intent: Return updated todo

### PATCH /todos/{id}
- Update todo completion status
- Request intent: Provide unique identifier and completion status
- Response intent: Return updated todo

### DELETE /todos/{id}
- Delete a specific todo
- Request intent: Provide unique identifier
- Response intent: Confirm successful deletion

## 7. Acceptance Criteria

### Create Todo
- Given the API service is running
- When a POST request is made to /todos with a valid description
- Then a new todo should be created in persistent storage
- And the response should contain the new todo with a unique identifier
- And the HTTP status should indicate success

### Read Todos (list + single)
- Given there are todos in persistent storage
- When a GET request is made to /todos
- Then all todos should be returned in the response
- And the HTTP status should indicate success

- Given there is a specific todo in storage
- When a GET request is made to /todos/{id} with a valid ID
- Then the specific todo should be returned in the response
- And the HTTP status should indicate success

### Update Todo
- Given there is an existing todo in storage
- When a PUT request is made to /todos/{id} with updated information
- Then the todo should be updated in persistent storage
- And the response should contain the updated todo
- And the HTTP status should indicate success

### Delete Todo
- Given there is an existing todo in storage
- When a DELETE request is made to /todos/{id} with a valid ID
- Then the todo should be removed from persistent storage
- And the response should confirm successful deletion
- And the HTTP status should indicate success

### Mark Todo complete / incomplete
- Given there is an existing todo in storage
- When a PATCH request is made to /todos/{id} with completion status
- Then the todo's completion status should be updated in persistent storage
- And the response should contain the updated todo
- And the HTTP status should indicate success

## 8. Constraints

### Python-based backend
- The application must be implemented in Python 3.13+
- All backend logic must be written in Python
- Any frameworks or libraries used must be compatible with Python 3.13+

### Persistent storage required
- All data must persist between application restarts
- Storage mechanism must be reliable and maintain data integrity
- Storage must support concurrent access safely

### Free-tier and open-source tools only
- All dependencies must be open-source and free to use
- Any storage solution must be free-tier compatible
- Any frameworks or libraries must be open-source
- No commercial or paid services may be used
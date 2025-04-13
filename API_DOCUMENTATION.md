# ADHD Productivity Assistant API Documentation

## Overview

The ADHD Productivity Assistant API provides endpoints for task management, goal tracking, and AI-powered assistance. This documentation covers all available endpoints, their request/response formats, and usage examples.

## Base URL

```
http://127.0.0.1:8000
```

## Authentication

Currently, the API does not require authentication. In a production environment, authentication would be implemented.

## Endpoints

### Assistant API

#### Send a Message to the Assistant

```
POST /api/assistant/message
```

Send a message to the AI assistant and receive a response.

**Request Body:**

```json
{
  "message": "I need to finish my project by next Friday. Can you help me break it down into steps?"
}
```

**Response:**

```json
{
  "response": "I'll help you break down your project into manageable steps. Let me create a task for you with a deadline of next Friday. I'll also set up some check-ins to help you stay on track.",
  "status": "success"
}
```

**Example Usage (Postman):**

1. Create a new POST request to `http://127.0.0.1:8000/api/assistant/message`
2. Set the Content-Type header to `application/json`
3. In the request body, select "raw" and "JSON", then enter:
   ```json
   {
     "message": "I need to finish my project by next Friday. Can you help me break it down into steps?"
   }
   ```
4. Send the request

### Tasks API

#### Get All Tasks

```
GET /api/tasks
```

Retrieve all tasks from the system.

**Response:**

```json
{
  "tasks": [
    {
      "id": "1",
      "description": "Finish project",
      "steps": [
        {
          "description": "Research requirements",
          "status": "pending"
        },
        {
          "description": "Create outline",
          "status": "completed",
          "completed_at": "2023-04-12T15:30:00"
        }
      ],
      "created_at": "2023-04-12T10:00:00",
      "status": "in_progress"
    }
  ]
}
```

#### Get a Specific Task

```
GET /api/tasks/{task_id}
```

Retrieve a specific task by ID.

**Response:**

```json
{
  "task": {
    "id": "1",
    "description": "Finish project",
    "steps": [
      {
        "description": "Research requirements",
        "status": "pending"
      },
      {
        "description": "Create outline",
        "status": "completed",
        "completed_at": "2023-04-12T15:30:00"
      }
    ],
    "created_at": "2023-04-12T10:00:00",
    "status": "in_progress"
  }
}
```

#### Mark Task or Step as Complete

```
POST /api/tasks/{task_id}/complete
```

Mark a task or a specific step as complete.

**Request Body:**

```json
{
  "step_index": 0 // Optional: If not provided, marks the entire task as complete
}
```

**Response:**

```json
{
  "message": "Task updated successfully.",
  "status": "success"
}
```

### Goals API

#### Get All Goals

```
GET /api/goals
```

Retrieve all goals from the system.

**Response:**

```json
{
  "goals": [
    {
      "id": "1",
      "description": "Complete project by next Friday",
      "deadline": "2023-04-19T23:59:59",
      "status": "in_progress",
      "created_at": "2023-04-12T10:00:00"
    }
  ]
}
```

#### Get a Specific Goal

```
GET /api/goals/{goal_id}
```

Retrieve a specific goal by ID.

**Response:**

```json
{
  "goal": {
    "id": "1",
    "description": "Complete project by next Friday",
    "deadline": "2023-04-19T23:59:59",
    "status": "in_progress",
    "created_at": "2023-04-12T10:00:00"
  }
}
```

### Check-ins API

#### Get All Check-ins

```
GET /api/checkins
```

Retrieve all scheduled check-ins.

**Response:**

```json
{
  "checkins": [
    {
      "id": "1",
      "task_id": "1",
      "scheduled_time": "2023-04-13T10:00:00",
      "status": "pending",
      "created_at": "2023-04-12T10:00:00"
    }
  ]
}
```

#### Get a Specific Check-in

```
GET /api/checkins/{checkin_id}
```

Retrieve a specific check-in by ID.

**Response:**

```json
{
  "checkin": {
    "id": "1",
    "task_id": "1",
    "scheduled_time": "2023-04-13T10:00:00",
    "status": "pending",
    "created_at": "2023-04-12T10:00:00"
  }
}
```

## Testing with Postman

1. **Set up a new Postman collection:**

   - Create a new collection named "ADHD Productivity Assistant"
   - Set the base URL variable to `http://127.0.0.1:8000`

2. **Create requests for each endpoint:**

   - For POST requests, set the Content-Type header to `application/json`
   - For request bodies, use the raw JSON format as shown in the examples

3. **Test the Assistant API:**

   - Create a POST request to `/api/assistant/message`
   - Add a JSON body with a "message" field
   - Send the request and observe the AI's response

4. **Test other endpoints:**
   - Create GET requests for tasks, goals, and check-ins
   - Create POST requests for completing tasks

## Common Use Cases

### Breaking Down a Project

1. Send a message to the assistant describing your project and deadline
2. The assistant will create a task with steps and schedule check-ins
3. Use the tasks API to view and update your progress

### Setting Reminders

1. Ask the assistant to set reminders for important events
2. The assistant will create tasks with scheduled check-ins
3. Use the check-ins API to view your upcoming reminders

### Storing Information

1. Ask the assistant to remember important information
2. The assistant will store this in the long-term memory
3. Later, you can ask the assistant to recall this information

## Error Handling

The API returns appropriate HTTP status codes:

- 200: Success
- 400: Bad Request (invalid input)
- 404: Not Found
- 500: Server Error

Error responses include a message explaining what went wrong:

```json
{
  "error": "Task with ID 123 not found.",
  "status": "error"
}
```

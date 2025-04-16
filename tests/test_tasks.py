import pytest
from quart.testing import QuartClient


@pytest.mark.asyncio
async def test_get_tasks_empty(client: QuartClient) -> None:
    """Test getting tasks when there are none."""
    response = await client.get("/api/tasks/")
    assert response.status_code == 200
    data = await response.get_json()
    assert isinstance(data, list)
    assert len(data) == 0


@pytest.mark.asyncio
async def test_create_task(client: QuartClient) -> None:
    """Test creating a new task."""
    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "estimated_duration": 45,
    }

    response = await client.post("/api/tasks/", json=task_data)
    assert response.status_code == 201
    data = await response.get_json()
    assert data["title"] == "Test Task"
    assert data["description"] == "This is a test task"
    assert data["estimated_duration"] == 45
    assert data["status"] == "pending"
    assert data["id"] == 1


@pytest.mark.asyncio
async def test_get_task_by_id(client: QuartClient) -> None:
    """Test getting a specific task by ID."""
    # First create a task
    task_data = {"title": "Task to Retrieve"}
    create_response = await client.post("/api/tasks/", json=task_data)
    created_task = await create_response.get_json()
    task_id = created_task["id"]

    # Then retrieve it by ID
    response = await client.get(f"/api/tasks/{task_id}")
    assert response.status_code == 200
    data = await response.get_json()
    assert data["title"] == "Task to Retrieve"
    assert data["id"] == task_id


@pytest.mark.asyncio
async def test_update_task(client: QuartClient) -> None:
    """Test updating a task."""
    # First create a task
    task_data = {"title": "Original Task"}
    create_response = await client.post("/api/tasks/", json=task_data)
    created_task = await create_response.get_json()
    task_id = created_task["id"]

    # Then update it
    update_data = {"title": "Updated Task Title", "description": "Updated description"}
    response = await client.put(f"/api/tasks/{task_id}", json=update_data)
    assert response.status_code == 200
    data = await response.get_json()
    assert data["title"] == "Updated Task Title"
    assert data["description"] == "Updated description"


@pytest.mark.asyncio
async def test_start_task(client: QuartClient) -> None:
    """Test starting a task."""
    # First create a task
    task_data = {"title": "Task to Start"}
    create_response = await client.post("/api/tasks/", json=task_data)
    created_task = await create_response.get_json()
    task_id = created_task["id"]

    # Then start it
    response = await client.post(f"/api/tasks/{task_id}/start")
    assert response.status_code == 200
    data = await response.get_json()
    assert data["status"] == "in_progress"
    assert data["started_at"] is not None
    assert data["check_in_time"] is not None


@pytest.mark.asyncio
async def test_complete_task(client: QuartClient) -> None:
    """Test completing a task."""
    # First create a task
    task_data = {"title": "Task to Complete"}
    create_response = await client.post("/api/tasks/", json=task_data)
    created_task = await create_response.get_json()
    task_id = created_task["id"]

    # Then complete it
    response = await client.post(f"/api/tasks/{task_id}/complete")
    assert response.status_code == 200
    data = await response.get_json()
    assert data["status"] == "completed"
    assert data["completed_at"] is not None

from datetime import datetime

import pytest
from quart.testing import QuartClient


@pytest.mark.asyncio
async def test_get_goals_empty(client: QuartClient) -> None:
    """Test getting goals when there are none."""
    response = await client.get("/api/goals/")
    assert response.status_code == 200
    data = await response.get_json()
    assert "goals" in data
    assert len(data["goals"]) == 0


@pytest.mark.asyncio
async def test_create_goal(client: QuartClient) -> None:
    """Test creating a new goal."""
    goal_data = {
        "title": "Test Goal",
        "description": "This is a test goal",
        "deadline": (datetime.now().isoformat()),
    }

    response = await client.post("/api/goals/", json=goal_data)
    assert response.status_code == 201
    data = await response.get_json()
    assert data["title"] == "Test Goal"
    assert data["description"] == "This is a test goal"
    assert data["status"] == "pending"
    assert data["id"] == 1


@pytest.mark.asyncio
async def test_get_goal_by_id(client: QuartClient) -> None:
    """Test getting a specific goal by ID."""
    # First create a goal
    goal_data = {"title": "Goal to Retrieve"}
    create_response = await client.post("/api/goals/", json=goal_data)
    created_goal = await create_response.get_json()
    goal_id = created_goal["id"]

    # Then retrieve it by ID
    response = await client.get(f"/api/goals/{goal_id}")
    assert response.status_code == 200
    data = await response.get_json()
    assert data["title"] == "Goal to Retrieve"
    assert data["id"] == goal_id


@pytest.mark.asyncio
async def test_update_goal(client: QuartClient) -> None:
    """Test updating a goal."""
    # First create a goal
    goal_data = {"title": "Original Goal"}
    create_response = await client.post("/api/goals/", json=goal_data)
    created_goal = await create_response.get_json()
    goal_id = created_goal["id"]

    # Then update it
    update_data = {"title": "Updated Goal Title", "description": "Updated description"}
    response = await client.put(f"/api/goals/{goal_id}", json=update_data)
    assert response.status_code == 200
    data = await response.get_json()
    assert data["title"] == "Updated Goal Title"
    assert data["description"] == "Updated description"


@pytest.mark.asyncio
async def test_complete_goal(client: QuartClient) -> None:
    """Test marking a goal as completed."""
    # First create a goal
    goal_data = {"title": "Goal to Complete"}
    create_response = await client.post("/api/goals/", json=goal_data)
    created_goal = await create_response.get_json()
    goal_id = created_goal["id"]

    # Then complete it
    response = await client.post(f"/api/goals/{goal_id}/complete")
    assert response.status_code == 200
    data = await response.get_json()
    assert data["status"] == "completed"
    assert data["completed_at"] is not None

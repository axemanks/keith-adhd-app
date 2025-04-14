from typing import Dict, List, Optional, Union, Any
from quart import Blueprint, Response, request, jsonify
from datetime import datetime, timedelta

bp = Blueprint("tasks", __name__, url_prefix="/api/tasks")

# Type definition for a task
TaskType = Dict[str, Union[int, str, Optional[str]]]

# In-memory storage for tasks (will be replaced with database)
tasks: List[TaskType] = []


@bp.route("/", methods=["GET"])
async def get_tasks() -> Response:
    """Get all tasks."""
    return jsonify(tasks)


@bp.route("/", methods=["POST"])
async def create_task() -> tuple[Response, int]:
    """Create a new task."""
    data = await request.get_json()

    # Validate required fields
    if not data.get("title"):
        return jsonify({"error": "Title is required"}), 400

    # Create task object
    task = {
        "id": len(tasks) + 1,
        "title": data["title"],
        "description": data.get("description", ""),
        "estimated_duration": data.get("estimated_duration", 30),  # in minutes
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "started_at": None,
        "completed_at": None,
        "check_in_time": None,
    }

    tasks.append(task)
    return jsonify(task), 201


@bp.route("/<int:task_id>", methods=["GET"])
async def get_task(task_id: int) -> tuple[Response, int]:
    """Get a specific task by ID."""
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task), 200


@bp.route("/<int:task_id>", methods=["PUT"])
async def update_task(task_id: int) -> tuple[Response, int]:
    """Update a task."""
    task: Optional[TaskType] = next((t for t in tasks if t["id"] == task_id), None)
    if task is None:
        return jsonify({"error": "Task not found"}), 404

    data: Dict[str, Any] = await request.get_json()

    # Update task fields
    if "title" in data:
        task["title"] = data["title"]
    if "description" in data:
        task["description"] = data["description"]
    if "estimated_duration" in data:
        task["estimated_duration"] = data["estimated_duration"]
    if "status" in data:
        task["status"] = data["status"]
        if data["status"] == "in_progress" and not task["started_at"]:
            task["started_at"] = datetime.now().isoformat()
        elif data["status"] == "completed" and not task["completed_at"]:
            task["completed_at"] = datetime.now().isoformat()

    return jsonify(task), 200


@bp.route("/<int:task_id>/start", methods=["POST"])
async def start_task(task_id: int) -> tuple[Response, int]:
    """Start a task and schedule a check-in."""
    task: Optional[TaskType] = next((t for t in tasks if t["id"] == task_id), None)
    if task is None:
        return jsonify({"error": "Task not found"}), 404

    # Update task status
    task["status"] = "in_progress"
    task["started_at"] = datetime.now().isoformat()

    # Schedule check-in (for now, just set a time 30 minutes from now)
    # In a real implementation, this would use a scheduler like APScheduler
    check_in_time: datetime = datetime.now() + timedelta(minutes=30)
    task["check_in_time"] = check_in_time.isoformat()

    return jsonify(task), 200


@bp.route("/<int:task_id>/complete", methods=["POST"])
async def complete_task(task_id: int) -> tuple[Response, int]:
    """Mark a task as completed."""
    task: Optional[TaskType] = next((t for t in tasks if t["id"] == task_id), None)
    if task is None:
        return jsonify({"error": "Task not found"}), 404

    task["status"] = "completed"
    task["completed_at"] = datetime.now().isoformat()

    return jsonify(task), 200

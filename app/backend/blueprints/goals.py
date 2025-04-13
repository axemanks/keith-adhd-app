from datetime import datetime
from typing import Any, Dict, List, Tuple

from quart import Blueprint, Response, jsonify, request

bp = Blueprint("goals", __name__, url_prefix="/api/goals")

# In-memory storage for goals (will be replaced with database)
goals: List[Dict[str, Any]] = []


@bp.route("/", methods=["GET"])
async def get_goals() -> Tuple[Response, int]:
    """Get all goals."""
    return jsonify({"goals": goals}), 200


@bp.route("/", methods=["POST"])
async def create_goal() -> Tuple[Response, int]:
    """Create a new goal."""
    data = await request.get_json()

    # Validate required fields
    if not data.get("title"):
        return jsonify({"error": "Title is required"}), 400

    # Create goal object
    goal = {
        "id": len(goals) + 1,
        "title": data["title"],
        "description": data.get("description", ""),
        "deadline": data.get("deadline"),
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "completed_at": None,
        "tasks": [],  # List of task IDs associated with this goal
    }

    goals.append(goal)
    return jsonify(goal), 201


@bp.route("/<int:goal_id>", methods=["GET"])
async def get_goal(goal_id: int) -> Tuple[Response, int]:
    """Get a specific goal by ID."""
    goal = next((g for g in goals if g["id"] == goal_id), None)
    if goal is None:
        return jsonify({"error": "Goal not found"}), 404
    return jsonify(goal), 200


@bp.route("/<int:goal_id>", methods=["PUT"])
async def update_goal(goal_id: int) -> Tuple[Response, int]:
    """Update a goal."""
    goal = next((g for g in goals if g["id"] == goal_id), None)
    if goal is None:
        return jsonify({"error": "Goal not found"}), 404

    data = await request.get_json()

    # Update goal fields
    if "title" in data:
        goal["title"] = data["title"]
    if "description" in data:
        goal["description"] = data["description"]
    if "deadline" in data:
        goal["deadline"] = data["deadline"]
    if "status" in data:
        goal["status"] = data["status"]
        if data["status"] == "completed" and not goal["completed_at"]:
            goal["completed_at"] = datetime.now().isoformat()

    return jsonify(goal), 200


@bp.route("/<int:goal_id>/tasks", methods=["POST"])
async def add_task_to_goal(goal_id: int) -> Tuple[Response, int]:
    """Add a task to a goal."""
    goal = next((g for g in goals if g["id"] == goal_id), None)
    if goal is None:
        return jsonify({"error": "Goal not found"}), 404

    data = await request.get_json()
    task_id = data.get("task_id")

    if not task_id:
        return jsonify({"error": "Task ID is required"}), 400

    # Check if task already exists in goal
    if task_id in goal["tasks"]:
        return jsonify({"error": "Task already added to this goal"}), 400

    goal["tasks"].append(task_id)
    return jsonify(goal), 200


@bp.route("/<int:goal_id>/complete", methods=["POST"])
async def complete_goal(goal_id: int) -> Tuple[Response, int]:
    """Mark a goal as completed."""
    goal = next((g for g in goals if g["id"] == goal_id), None)
    if goal is None:
        return jsonify({"error": "Goal not found"}), 404

    goal["status"] = "completed"
    goal["completed_at"] = datetime.now().isoformat()

    return jsonify(goal), 200

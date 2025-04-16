from datetime import datetime
from typing import Any, Dict, List, Tuple, Union

from quart import Blueprint, Response, jsonify, request

bp = Blueprint("checkins", __name__, url_prefix="/api/checkins")

# In-memory storage for check-ins (will be replaced with database)
checkins: List[Dict[str, Any]] = []


@bp.route("/", methods=["GET"])
async def get_checkins() -> Response:
    """Get all check-ins."""
    return jsonify(checkins)


@bp.route("/", methods=["POST"])
async def create_checkin() -> Union[Response, Tuple[Response, int]]:
    """Create a new check-in."""
    data = await request.get_json()

    # Validate required fields
    if not data.get("task_id"):
        return jsonify({"error": "Task ID is required"}), 400

    # Create check-in object
    checkin = {
        "id": len(checkins) + 1,
        "task_id": data["task_id"],
        "status": data.get("status", "in_progress"),
        "notes": data.get("notes", ""),
        "created_at": datetime.now().isoformat(),
        "next_checkin_time": data.get("next_checkin_time"),
    }

    checkins.append(checkin)
    return jsonify(checkin), 201


@bp.route("/<int:checkin_id>", methods=["GET"])
async def get_checkin(checkin_id: int) -> Union[Response, Tuple[Response, int]]:
    """Get a specific check-in by ID."""
    checkin = next((c for c in checkins if c["id"] == checkin_id), None)
    if checkin is None:
        return jsonify({"error": "Check-in not found"}), 404
    return jsonify(checkin)


@bp.route("/task/<int:task_id>", methods=["GET"])
async def get_task_checkins(task_id: int) -> Response:
    """Get all check-ins for a specific task."""
    task_checkins = [c for c in checkins if c["task_id"] == task_id]
    return jsonify(task_checkins)


@bp.route("/<int:checkin_id>", methods=["PUT"])
async def update_checkin(checkin_id: int) -> Union[Response, Tuple[Response, int]]:
    """Update a check-in."""
    checkin = next((c for c in checkins if c["id"] == checkin_id), None)
    if checkin is None:
        return jsonify({"error": "Check-in not found"}), 404

    data = await request.get_json()

    # Update check-in fields
    if "status" in data:
        checkin["status"] = data["status"]
    if "notes" in data:
        checkin["notes"] = data["notes"]
    if "next_checkin_time" in data:
        checkin["next_checkin_time"] = data["next_checkin_time"]

    return jsonify(checkin)


@bp.route("/due", methods=["GET"])
async def get_due_checkins() -> Response:
    """Get all check-ins that are due now."""
    now = datetime.now().isoformat()
    due_checkins = [
        c for c in checkins if c.get("next_checkin_time") and c["next_checkin_time"] <= now
    ]
    return jsonify(due_checkins)

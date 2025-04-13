import json
import os
from datetime import datetime
from typing import Optional

from apscheduler.executors.pool import ThreadPoolExecutor  # type: ignore
from apscheduler.jobstores.memory import MemoryJobStore  # type: ignore
from apscheduler.schedulers.asyncio import AsyncIOScheduler  # type: ignore

# File paths for persistent storage
TASKS_FILE = "instance/tasks.json"
MEMORY_FILE = "instance/memory.json"

# Global scheduler variable
scheduler = None


def ensure_files_exist() -> None:  # type: ignore
    """Ensure that the JSON storage files exist."""
    os.makedirs("instance", exist_ok=True)

    if not os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'w') as f:
            json.dump({"tasks": []}, f)

    if not os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'w') as f:
            json.dump({"memories": {}}, f)


ensure_files_exist()


async def initialize_scheduler() -> AsyncIOScheduler:  # type: ignore
    """Initialize the scheduler in an async context."""
    global scheduler
    if scheduler is None:
        jobstores = {'default': MemoryJobStore()}
        executors = {'default': ThreadPoolExecutor(20)}
        job_defaults = {'coalesce': False, 'max_instances': 3}

        scheduler = AsyncIOScheduler(
            jobstores=jobstores, executors=executors, job_defaults=job_defaults
        )
        scheduler.start()
    return scheduler


async def schedule_goal(goal_description: str) -> str:
    """
    Break down a goal into steps and schedule them.
    Args:
        goal_description: Description of the goal to break down
    Returns:
        str: Response message
    """
    try:
        # Initialize scheduler if needed
        await initialize_scheduler()

        # Load existing tasks
        with open(TASKS_FILE, 'r') as f:
            data = json.load(f)

        # Create a new task
        task_id = str(len(data["tasks"]) + 1)
        new_task = {
            "id": task_id,
            "description": goal_description,
            "steps": [],
            "created_at": datetime.now().isoformat(),
            "status": "pending",
        }

        # Add the task
        data["tasks"].append(new_task)

        # Save the updated tasks
        with open(TASKS_FILE, 'w') as f:
            json.dump(data, f, indent=2)

        return f"Created new task with ID {task_id}. You can now add steps to this task."

    except Exception as e:
        return f"Error scheduling goal: {str(e)}"


async def mark_task_done(task_id: str, step_index: Optional[int] = None) -> str:
    """
    Mark a task or step as complete.
    Args:
        task_id: ID of the task
        step_index: Index of the step (if marking a step complete)
    Returns:
        str: Response message
    """
    try:
        with open(TASKS_FILE, 'r') as f:
            data = json.load(f)

        # Find the task
        task = next((t for t in data["tasks"] if t["id"] == task_id), None)
        if not task:
            return f"Task with ID {task_id} not found."

        if step_index is not None:
            # Mark step as complete
            if 0 <= step_index < len(task["steps"]):
                task["steps"][step_index]["status"] = "completed"
                task["steps"][step_index]["completed_at"] = datetime.now().isoformat()
            else:
                return f"Step index {step_index} out of range."
        else:
            # Mark entire task as complete
            task["status"] = "completed"
            task["completed_at"] = datetime.now().isoformat()

        # Save the updated tasks
        with open(TASKS_FILE, 'w') as f:
            json.dump(data, f, indent=2)

        return "Task updated successfully."

    except Exception as e:
        return f"Error marking task complete: {str(e)}"


async def store_memory(key: str, value: str) -> str:
    """
    Store a memory in the long-term memory.
    Args:
        key: Memory key
        value: Memory value
    Returns:
        str: Response message
    """
    try:
        with open(MEMORY_FILE, 'r') as f:
            data = json.load(f)

        # Store the memory
        data["memories"][key] = {"value": value, "created_at": datetime.now().isoformat()}

        # Save the updated memories
        with open(MEMORY_FILE, 'w') as f:
            json.dump(data, f, indent=2)

        return f"Memory stored successfully with key: {key}"

    except Exception as e:
        return f"Error storing memory: {str(e)}"


async def get_memory(key: str) -> str:
    """
    Retrieve a memory from long-term memory.
    Args:
        key: Memory key to retrieve
    Returns:
        str: Memory value or error message
    """
    try:
        with open(MEMORY_FILE, 'r') as f:
            data = json.load(f)

        memory = data["memories"].get(key)
        if memory:
            return f"Memory for key '{key}': {memory['value']}"
        else:
            return f"No memory found for key: {key}"

    except Exception as e:
        return f"Error retrieving memory: {str(e)}"


async def web_search(query: str) -> str:
    """
    Search the web for real-time information.
    Args:
        query: Search query
    Returns:
        str: Search results or error message
    """
    # Simple placeholder for web search functionality
    return f"Web search for '{query}' is not implemented yet. This feature will be added in a future update."

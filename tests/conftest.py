import sys
from pathlib import Path
from typing import Any

import pytest
from quart import Quart
from quart.testing import QuartCliRunner

from app.backend.app import create_app

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
async def app() -> Quart:
    """Create a Quart application for testing."""
    app = create_app({"TESTING": True})
    return app


@pytest.fixture
async def client(app: Quart) -> Any:  # Changed return type to Any
    """Create a Quart test client."""
    return app.test_client()


@pytest.fixture
async def runner(app: Quart) -> QuartCliRunner:
    """Create a test CLI runner."""
    return app.test_cli_runner()

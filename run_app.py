import os
import sys

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

if __name__ == "__main__":
    import asyncio

    import hypercorn.asyncio

    from app.backend.app import create_app

    app = create_app()

    config = hypercorn.Config()
    config.bind = ["127.0.0.1:8000"]
    config.use_reloader = True

    asyncio.run(hypercorn.asyncio.serve(app, config))

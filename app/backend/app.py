import os

from dotenv import load_dotenv
from quart import Quart, send_from_directory

# Load environment variables
load_dotenv()


def create_app(test_config=None):
    """Create and configure the Quart application."""
    app = Quart(__name__, static_folder="static", static_url_path="")

    # Default configuration
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev"),
        DATABASE=os.path.join(app.instance_path, "adhd_assistant.sqlite"),
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Register blueprints
    from blueprints import checkins, goals, tasks

    app.register_blueprint(tasks.bp)
    app.register_blueprint(goals.bp)
    app.register_blueprint(checkins.bp)

    # Serve static files
    @app.route("/assets/<path:filename>")
    async def serve_static(filename):
        return await send_from_directory(os.path.join(app.static_folder, "assets"), filename)

    # Serve the frontend index.html for all routes except /api
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    async def serve_frontend(path):
        # Don't serve frontend for API routes
        if path.startswith("api/"):
            return {"error": "API endpoint not found"}, 404

        # Serve the frontend index.html for all other routes
        return await send_from_directory(app.static_folder, "index.html")

    # API routes will be added here
    @app.route("/api/health")
    async def health_check():
        return {"status": "ok"}

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
    app.run(debug=True)

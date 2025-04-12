import os
from quart import Quart, render_template
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def create_app(test_config=None):
    """Create and configure the Quart application."""
    app = Quart(__name__, static_folder="static", template_folder="templates")

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

    # Simple route to test the app
    @app.route("/")
    async def index():
        return await render_template("index.html")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

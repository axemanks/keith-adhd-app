# ADHD Task Assistant Backend

This is the backend for the ADHD Task Assistant application. It provides API endpoints for managing tasks, goals, and check-ins for people with ADHD.

## Technologies

- Python 3.12
- Quart (async Flask-like framework)
- SQLite (for simplicity, can be upgraded to PostgreSQL later)

## Setup

1. Install dependencies:

   ```
   poetry install
   ```

2. Run the development server:
   ```
   poetry run python app.py
   ```

## API Endpoints

- `GET /`: Home page
- More endpoints will be added as the application develops

## Development

The backend is structured as follows:

- `app.py`: Main application entry point
- `templates/`: HTML templates
- `static/`: Static assets (CSS, JS, images)
- `instance/`: Instance-specific files (database, config)

## Testing

Run tests with:

```
poetry run pytest
```

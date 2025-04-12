# ADHD Task Assistant

A comprehensive task management application designed specifically for individuals with ADHD, helping them organize, prioritize, and complete tasks more effectively.

## Features

- Task creation, organization, and tracking
- Priority management
- Time estimation and tracking
- Progress visualization
- Customizable task categories
- Responsive design for desktop and mobile use

## Project Structure

```
adhd-task-assistant/
├── app/
│   ├── backend/         # Quart backend
│   └── frontend/        # React frontend
├── .vscode/            # VSCode configuration
├── pyproject.toml      # Poetry dependencies
└── README.md           # This file
```

## Prerequisites

- Python 3.9+
- Node.js 14+
- npm or yarn
- Poetry (Python package manager)
- Visual Studio Code (recommended)

## Setup

### Backend Setup

1. Install dependencies using Poetry:

   ```bash
   poetry install
   ```

2. Activate the virtual environment:
   ```bash
   poetry shell
   ```

### Frontend Setup

1. Navigate to the frontend directory:

   ```bash
   cd app/frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```
   or
   ```bash
   yarn install
   ```

## Running the Application

### Development Mode

#### Using VSCode (Recommended)

1. Open the project in VSCode
2. Press `F5` or select "Run and Debug" from the sidebar
3. Choose "Python: Quart" configuration
4. The backend server will start on `http://127.0.0.1:8000`

#### Using Terminal

1. Navigate to the backend directory:

   ```bash
   cd app/backend
   ```

2. Run the server using Poetry:
   ```bash
   poetry run hypercorn app:create_app() --bind 127.0.0.1:8000 --log-level debug
   ```

### Frontend Development

For local frontend development (only needed if you're working on the frontend code):

1. Open a new terminal and navigate to the frontend directory:

   ```bash
   cd app/frontend
   ```

2. Install dependencies (first time only):

   ```bash
   npm install
   ```

   or for a clean install:

   ```bash
   npm ci
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

Note: The frontend development server is only needed when actively developing the frontend. For regular use of the application, you only need to run the backend server.

### Backend API

The backend API will be available at:

- Health check: `http://127.0.0.1:8000/api/health`
- API endpoints: `http://127.0.0.1:8000/api/*`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

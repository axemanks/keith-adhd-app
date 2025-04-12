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
├── src/
│   ├── backend/         # FastAPI backend
│   └── frontend/        # React frontend
├── run.py               # Script to run the application
├── .gitignore           # Git ignore file
└── README.md            # This file
```

## Prerequisites

- Python 3.8+
- Node.js 14+
- npm or yarn
- Poetry (Python package manager)

## Setup

### Backend Setup

1. Navigate to the backend directory:

   ```
   cd src/backend
   ```

2. Install dependencies using Poetry:

   ```
   poetry install
   ```

3. Activate the virtual environment:
   ```
   poetry shell
   ```

### Frontend Setup

1. Navigate to the frontend directory:

   ```
   cd src/frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```
   or
   ```
   yarn install
   ```

## Running the Application

### Development Mode

To run both the backend and frontend in development mode:

```
python run.py dev
```

This will:

- Start the backend server
- Start the frontend development server
- Open the application in your default web browser

### Backend Only

To run only the backend server:

```
python run.py backend
```

### Production Build

To build the frontend for production:

```
python run.py build
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

#!/usr/bin/env python3
"""
Run script for the ADHD Task Assistant application.
This script starts the backend server and can also build the frontend.
"""
import os
import platform
import signal
import subprocess
import sys
import time
import webbrowser


def check_npm_installed():
    """Check if npm is installed."""
    try:
        subprocess.run(["npm", "--version"], check=True, capture_output=True)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False


def check_frontend_exists():
    """Check if the frontend directory exists."""
    return os.path.exists("src/frontend")


def check_backend_exists():
    """Check if the backend directory exists."""
    return os.path.exists("src/backend")


def run_backend():
    """Run the backend server."""
    print("Starting backend server...")
    os.chdir("src/backend")
    if platform.system() == "Windows":
        subprocess.run(["poetry", "run", "python", "app.py"], check=True)
    else:
        subprocess.run(["poetry", "run", "python", "app.py"], check=True)
    os.chdir("../..")


def build_frontend():
    """Build the frontend for production."""
    print("Building frontend...")
    os.chdir("src/frontend")
    subprocess.run(["npm", "install"], check=True)
    subprocess.run(["npm", "run", "build"], check=True)
    os.chdir("../..")


def dev_mode():
    """Run both backend and frontend in development mode."""
    print("Starting development mode...")

    # Start backend in a separate process
    backend_process = subprocess.Popen(
        ["python", "run.py", "backend"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        universal_newlines=True,
    )

    # Start frontend in a separate process
    os.chdir("src/frontend")
    frontend_process = subprocess.Popen(
        ["npm", "run", "dev"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        universal_newlines=True,
    )
    os.chdir("../..")

    # Open the frontend in a browser
    time.sleep(3)  # Give the frontend server time to start
    webbrowser.open("http://localhost:5173")

    # Function to handle Ctrl+C
    def signal_handler(sig, frame):
        print("\nShutting down servers...")
        backend_process.terminate()
        frontend_process.terminate()
        sys.exit(0)

    # Register the signal handler
    signal.signal(signal.SIGINT, signal_handler)

    # Print logs from both processes
    try:
        while True:
            # Print backend logs
            backend_line = backend_process.stdout.readline()
            if backend_line:
                print(f"[Backend] {backend_line.strip()}")

            # Print frontend logs
            frontend_line = frontend_process.stdout.readline()
            if frontend_line:
                print(f"[Frontend] {frontend_line.strip()}")

            # Check if processes have terminated
            if backend_process.poll() is not None or frontend_process.poll() is not None:
                break
    except KeyboardInterrupt:
        print("\nShutting down servers...")
        backend_process.terminate()
        frontend_process.terminate()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "build":
            build_frontend()
        elif command == "backend":
            run_backend()
        elif command == "dev":
            dev_mode()
        else:
            print(f"Unknown command: {command}")
            print("Available commands: build, backend, dev")
            sys.exit(1)
    else:
        # Default behavior: just run the backend
        run_backend()

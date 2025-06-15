#!/usr/bin/env python3
"""
Poker Helper Runner Script
This script checks for required dependencies, installs them if needed in a virtual environment,
and runs the poker helper application.
"""
import os
import sys
import subprocess
import venv
import shutil

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def check_venv_exists():
    """Check if virtual environment exists."""
    return os.path.exists('venv') and os.path.isdir('venv')

def create_venv():
    """Create a virtual environment."""
    print("Creating virtual environment...")
    venv.create('venv', with_pip=True)
    return True

def activate_venv():
    """Return the path to the virtual environment's Python executable."""
    if os.name == 'nt':  # Windows
        return os.path.join('venv', 'Scripts', 'python.exe')
    else:  # Unix/Linux/Mac
        return os.path.join('venv', 'bin', 'python')

def install_requirements(venv_python):
    """Install requirements using the virtual environment's pip."""
    print("Installing required packages...")
    requirements_file = 'requirements.txt'
    
    if not os.path.exists(requirements_file):
        print(f"Error: {requirements_file} not found!")
        return False
    
    try:
        subprocess.check_call([venv_python, '-m', 'pip', 'install', '-r', requirements_file])
        return True
    except subprocess.CalledProcessError:
        print("Failed to install requirements.")
        return False

def run_app(venv_python):
    """Run the Flask application using the virtual environment's Python."""
    print("Starting Poker Helper application...")
    try:
        # Run the app with the virtual environment's Python
        subprocess.check_call([venv_python, '-m', 'src.web.app'])
        return True
    except subprocess.CalledProcessError:
        print("Failed to start the application.")
        return False
    except KeyboardInterrupt:
        print("\nApplication stopped by user.")
        return True

def main():
    """Main function to run the script."""
    print("Poker Helper Setup and Runner")
    print("============================")
    
    # Check if we're in the right directory
    if not os.path.exists('src/web/app.py'):
        print("Error: src/web/app.py not found! Make sure you're running this script from the poker-helper directory.")
        return False
    
    # Check if virtual environment exists, create if it doesn't
    if not check_venv_exists():
        if not create_venv():
            print("Failed to create virtual environment.")
            return False
    
    # Get the path to the virtual environment's Python
    venv_python = activate_venv()
    
    # Install requirements
    if not install_requirements(venv_python):
        return False
    
    # Run the application
    return run_app(venv_python)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

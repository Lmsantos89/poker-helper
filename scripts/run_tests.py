#!/usr/bin/env python3
"""
Test Runner Script for Poker Helper
Runs all tests and generates coverage reports.
This script automatically uses the project's virtual environment if available.
"""
import os
import sys
import subprocess
import importlib.util
import unittest

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def get_venv_python():
    """Get the path to the virtual environment's Python executable."""
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    
    # Check for virtual environment in standard locations
    if os.path.exists(os.path.join(project_root, "venv", "bin", "python")):
        return os.path.join(project_root, "venv", "bin", "python")
    elif os.path.exists(os.path.join(project_root, "venv", "Scripts", "python.exe")):  # Windows
        return os.path.join(project_root, "venv", "Scripts", "python.exe")
    
    # If no virtual environment found, return the current Python executable
    return sys.executable

def check_dependency(package_name):
    """Check if a Python package is installed."""
    return importlib.util.find_spec(package_name) is not None

def install_package(package_name):
    """Install a Python package using pip in the virtual environment."""
    print(f"Installing {package_name}...")
    python_executable = get_venv_python()
    
    try:
        subprocess.check_call([python_executable, "-m", "pip", "install", package_name])
        return True
    except subprocess.CalledProcessError:
        print(f"Failed to install {package_name}.")
        return False

def run_tests_with_coverage():
    """Run all tests with coverage reporting."""
    # Check if coverage is installed
    if not check_dependency("coverage"):
        if not install_package("coverage"):
            print("Coverage is required to run tests with coverage reporting.")
            print("Try activating your virtual environment first:")
            print("  source venv/bin/activate  # On Linux/Mac")
            print("  venv\\Scripts\\activate    # On Windows")
            return False
    
    # Now we can import coverage
    try:
        import coverage
    except ImportError:
        # If we still can't import coverage, try to run the script with the virtual environment Python
        venv_python = get_venv_python()
        if venv_python != sys.executable:
            print(f"Restarting script with virtual environment Python: {venv_python}")
            os.execl(venv_python, venv_python, *sys.argv)
        else:
            print("Could not import coverage module. Please install it manually.")
            return False
    
    print("Running tests with coverage...")
    
    # Start coverage measurement
    cov = coverage.Coverage(
        source=["src"],
        omit=["*/__pycache__/*", "*/tests/*", "*/venv/*"]
    )
    cov.start()
    
    # Discover and run all tests
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover("tests", pattern="test_*.py")
    test_runner = unittest.TextTestRunner(verbosity=2)
    result = test_runner.run(test_suite)
    
    # Stop coverage measurement
    cov.stop()
    cov.save()
    
    # Report coverage results
    print("\nCoverage Report:")
    cov.report()
    
    # Generate HTML report
    html_dir = "htmlcov"
    print(f"\nGenerating HTML coverage report in {html_dir}...")
    cov.html_report(directory=html_dir)
    
    print(f"\nHTML coverage report is available at {os.path.abspath(html_dir)}/index.html")
    
    # Return True if all tests passed
    return len(result.failures) == 0 and len(result.errors) == 0

if __name__ == "__main__":
    success = run_tests_with_coverage()
    sys.exit(0 if success else 1)

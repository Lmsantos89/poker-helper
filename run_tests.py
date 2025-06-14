#!/usr/bin/env python3
"""
Run all unit tests for the poker helper application with coverage reporting.
"""
import unittest
import sys
import os
import coverage

def run_tests_with_coverage():
    """Run all tests with coverage reporting."""
    print("Running tests with coverage...\n")
    
    # Start coverage measurement
    cov = coverage.Coverage(
        source=['.'],
        omit=['*/__pycache__/*', '*/tests/*', '*/venv/*', 'run_*.py']
    )
    cov.start()
    
    try:
        # Import the modules to ensure they're covered
        import app
        import models
        import utils
        
        # Discover and run all tests
        test_loader = unittest.TestLoader()
        test_suite = test_loader.discover('tests', pattern='test_*.py')
        
        # Run the tests
        test_runner = unittest.TextTestRunner(verbosity=2)
        result = test_runner.run(test_suite)
        
        # Stop coverage measurement
        cov.stop()
        cov.save()
        
        # Print coverage report
        print("\nCoverage Summary:")
        cov.report()
        
        # Generate HTML report
        html_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'htmlcov')
        cov.html_report(directory=html_dir)
        print(f"\nHTML coverage report generated in: {html_dir}")
        
        # Exit with non-zero code if tests failed
        return result.wasSuccessful()
    except Exception as e:
        print(f"Error running tests with coverage: {e}")
        return False

if __name__ == '__main__':
    success = run_tests_with_coverage()
    sys.exit(not success)

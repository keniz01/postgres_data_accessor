#!/usr/bin/env python3
import unittest
import coverage
import sys
import os

def run_tests_with_coverage():
    # Start coverage measurement
    cov = coverage.Coverage()
    cov.start()

    # Add the src directory to Python path
    src_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src')
    sys.path.insert(0, src_path)

    # Discover and run tests
    loader = unittest.TestLoader()
    tests_dir = os.path.dirname(os.path.abspath(__file__))
    suite = loader.discover(tests_dir)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Stop coverage measurement
    cov.stop()
    cov.save()

    # Report coverage in terminal
    print("\nCoverage Report:")
    cov.report()

    # Generate HTML report
    cov.html_report()

    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_tests_with_coverage()
    sys.exit(0 if success else 1)

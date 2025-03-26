"""
Entry point module for running the package as a script.

This module allows 'python -m securepass' to work as expected.
"""

# Import the main function to serve as the entry point
from securepass.cli import main

if __name__ == "__main__":
    import sys
    sys.exit(main())
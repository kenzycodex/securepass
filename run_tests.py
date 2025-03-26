#!/usr/bin/env python
"""
Run tests for SecurePass with dynamic discovery and platform awareness.

This script automatically discovers all test modules and runs them with the
appropriate platform markers. It also handles coverage reporting without
requiring a .coveragerc file.
"""

import os
import sys
import subprocess
import argparse
import importlib.util
import glob
import re


def discover_test_modules():
    """Dynamically discover all test modules in the tests directory."""
    test_files = glob.glob(os.path.join("tests", "test_*.py"))
    test_modules = []
    
    for test_file in test_files:
        # Extract module name from file path (e.g., "tests/test_generator.py" -> "generator")
        module_name = os.path.basename(test_file)[5:-3]  # Remove "test_" prefix and ".py" suffix
        test_modules.append(module_name)
    
    return sorted(test_modules)


def get_platform_markers():
    """Get the appropriate platform markers for pytest."""
    if sys.platform == "win32":
        return "not (linux or macos)"
    elif sys.platform == "darwin":
        return "not (windows or linux)"
    elif sys.platform.startswith("linux"):
        return "not (windows or macos)"
    else:
        return ""


def find_required_packages():
    """Find any packages needed for testing but not installed."""
    required_packages = {
        "pytest": "pytest",
        "pytest-cov": "pytest-cov",
        "pytest-mock": "pytest-mock"
    }
    
    missing_packages = []
    for package, import_name in required_packages.items():
        if importlib.util.find_spec(import_name) is None:
            missing_packages.append(package)
    
    return missing_packages


def install_missing_packages(packages):
    """Install missing packages required for testing."""
    if not packages:
        return
    
    print(f"Installing required testing packages: {', '.join(packages)}")
    subprocess.run([sys.executable, "-m", "pip", "install"] + packages)


def main():
    """Run tests with dynamic discovery and appropriate configuration."""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Run SecurePass tests")
    parser.add_argument("--all", action="store_true", help="Run all tests regardless of platform")
    parser.add_argument("--coverage", action="store_true", help="Generate coverage report")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--module", "-m", help="Run specific test module(s), comma-separated")
    parser.add_argument("--install-deps", action="store_true", help="Install required test dependencies")
    args = parser.parse_args()

    # Install missing dependencies if requested or needed
    if args.install_deps or (args.coverage and importlib.util.find_spec("pytest_cov") is None):
        missing_packages = find_required_packages()
        if missing_packages:
            install_missing_packages(missing_packages)
    
    # Discover available test modules
    available_modules = discover_test_modules()
    print(f"Available test modules: {', '.join(available_modules)}")
    
    # Get platform-specific markers
    platform_marker = get_platform_markers()
    
    # Build the test command
    cmd = ["pytest"]
    
    # Add platform marker if not running all tests
    if platform_marker and not args.all:
        cmd.append(f"-m={platform_marker}")
    
    # Add verbose flag
    if args.verbose:
        cmd.append("-v")
    
    # Add coverage flags
    if args.coverage:
        cmd.extend(["--cov=securepass", "--cov-report=term-missing"])
    
    # Add specific module(s) if requested
    if args.module:
        requested_modules = [m.strip() for m in args.module.split(",")]
        module_paths = []
        
        for module in requested_modules:
            if module in available_modules:
                module_paths.append(f"tests/test_{module}.py")
            elif f"test_{module}.py" in [os.path.basename(f) for f in glob.glob(os.path.join("tests", "test_*.py"))]:
                module_paths.append(f"tests/test_{module}.py")
            else:
                print(f"Warning: Test module '{module}' not found in {available_modules}")
        
        if module_paths:
            cmd.extend(module_paths)
    
    # Print the command
    print(f"Running: {' '.join(cmd)}")
    
    # Run the tests
    subprocess.run(cmd)


if __name__ == "__main__":
    main()
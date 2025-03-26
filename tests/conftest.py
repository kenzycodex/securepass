"""
Configuration and fixtures for pytest.

This module contains all the pytest configuration, fixtures, and helper
functions used across the test suite.
"""

import pytest
import sys
import os
import subprocess
from unittest.mock import patch, MagicMock


def pytest_configure(config):
    """Configure pytest with custom markers."""
    # Platform-specific markers
    config.addinivalue_line(
        "markers", "windows: mark test as Windows-only"
    )
    config.addinivalue_line(
        "markers", "macos: mark test as macOS-only"
    )
    config.addinivalue_line(
        "markers", "linux: mark test as Linux-only"
    )
    
    # Feature-specific markers
    config.addinivalue_line(
        "markers", "clipboard: mark tests that interact with the clipboard"
    )
    config.addinivalue_line(
        "markers", "generator: mark tests for password generation"
    )
    config.addinivalue_line(
        "markers", "cli: mark tests for command-line interface"
    )
    
    # Exclude platform-specific branches from coverage
    # by adding comments like: # pragma: no cover [platform]
    if hasattr(config, "option") and hasattr(config.option, "cov_config"):
        if not config.option.cov_config:
            # Add dynamic coverage exclusions
            exclude_lines = [
                "pragma: no cover",
                "def __repr__",
                "raise NotImplementedError",
                "if __name__ == .__main__.:",
                "pass",
                "raise ImportError",
                "except ImportError:",
                "except FileNotFoundError:",
            ]
            
            # Add platform-specific exclusions
            current_platform = get_platform()
            if current_platform == "windows":
                exclude_lines.extend([
                    "if sys\\.platform != \"win32\":",
                    "if sys\\.platform == \"darwin\":",
                    "if sys\\.platform\\.startswith\\(\"linux\"\\):",
                ])
            elif current_platform == "macos":
                exclude_lines.extend([
                    "if sys\\.platform == \"win32\":",
                    "if sys\\.platform != \"darwin\":",
                    "if sys\\.platform\\.startswith\\(\"linux\"\\):",
                ])
            elif current_platform == "linux":
                exclude_lines.extend([
                    "if sys\\.platform == \"win32\":",
                    "if sys\\.platform == \"darwin\":",
                    "if not sys\\.platform\\.startswith\\(\"linux\"\\):",
                ])
            
            # Set up dynamic coverage configuration
            config.option._coveragerc = {
                "run": {
                    "source": ["securepass"],
                    "omit": ["*/site-packages/*", "*/distutils/*", "tests/*", "setup.py"],
                },
                "report": {
                    "exclude_lines": exclude_lines,
                }
            }


def get_platform():
    """Get the current platform as a string."""
    if sys.platform == "win32":
        return "windows"
    elif sys.platform == "darwin":
        return "macos"
    elif sys.platform.startswith("linux"):
        return "linux"
    else:
        return "unknown"


@pytest.fixture
def platform():
    """Return the current platform as a string."""
    return get_platform()


@pytest.fixture
def on_windows():
    """Fixture to check if running on Windows."""
    return sys.platform == "win32"


@pytest.fixture
def on_macos():
    """Fixture to check if running on macOS."""
    return sys.platform == "darwin"


@pytest.fixture
def on_linux():
    """Fixture to check if running on Linux."""
    return sys.platform.startswith("linux")


@pytest.fixture
def mock_clipboard_methods():
    """Mock all clipboard methods to simplify testing."""
    patchers = []
    
    # Import module paths dynamically to avoid import errors
    try:
        import securepass.clipboard
        
        # Mock clipboard utility functions
        modules_to_patch = [
            'securepass.clipboard.pyperclip.pyperclip_copy',
            'securepass.clipboard.copyq.copyq_copy',
            'securepass.clipboard.xclip.xclip_copy',
            'securepass.clipboard.wlclip.wlclip_copy',
            'securepass.clipboard.powershell.powershell_copy',
            'securepass.clipboard.pbcopy.pbcopy_copy',
        ]
        
        for module_path in modules_to_patch:
            try:
                patchers.append(patch(module_path, return_value=None))
            except (ImportError, AttributeError):
                # Skip patching if module doesn't exist
                pass
    except ImportError:
        # If the securepass.clipboard module isn't importable, don't patch anything
        pass
    
    # Start all patchers
    mocks = [patcher.start() for patcher in patchers]
    
    yield mocks
    
    # Stop all patchers
    for patcher in patchers:
        try:
            patcher.stop()
        except RuntimeError:
            # Ignore errors when stopping patchers that weren't started
            pass


@pytest.fixture
def secure_temp_dir(tmpdir):
    """Create a secure temporary directory with controlled permissions."""
    # Set more restrictive permissions on temporary directory
    if sys.platform != "win32":  # Skip on Windows where chmod works differently
        os.chmod(tmpdir, 0o700)  # rwx for owner only
    
    return tmpdir


@pytest.fixture
def command_exists():
    """Check if a command exists on the system."""
    def _exists(command):
        """Check if the given command exists in the PATH."""
        try:
            # Use 'where' on Windows, 'which' on Unix-like systems
            which_cmd = 'where' if sys.platform == 'win32' else 'which'
            subprocess.run(
                [which_cmd, command],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
                text=True
            )
            return True
        except (subprocess.SubprocessError, FileNotFoundError):
            return False
    
    return _exists
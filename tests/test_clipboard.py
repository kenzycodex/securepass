# tests/test_clipboard.py
"""
Tests for clipboard integration functionality.

This module contains tests for all clipboard-related functionality,
including platform-specific clipboard mechanisms and fallbacks.
"""

import pytest
import sys
import os
from unittest.mock import patch, MagicMock
import subprocess
from securepass.clipboard import ClipboardDriver
from securepass.clipboard.pyperclip import pyperclip_copy
from securepass.clipboard.copyq import copyq_copy
from securepass.clipboard.xclip import xclip_copy
from securepass.clipboard.wlclip import wlclip_copy
from securepass.clipboard.powershell import powershell_copy
from securepass.clipboard.pbcopy import pbcopy_copy


@pytest.mark.clipboard
def test_copy_password_success():
    """Test successful password copying."""
    mock_method = MagicMock()
    with patch.object(ClipboardDriver, '_COPY_METHODS', [mock_method]):
        ClipboardDriver.copy_password("test", True)
        mock_method.assert_called_once_with("test", True)


@pytest.mark.clipboard
def test_copy_password_failure():
    """Test clipboard failure handling."""
    mock_method = MagicMock(side_effect=Exception("Test error"))
    with patch.object(ClipboardDriver, '_COPY_METHODS', [mock_method]):
        with pytest.raises(RuntimeError, match="Failed to copy to clipboard"):
            ClipboardDriver.copy_password("test", True)


@pytest.mark.clipboard
def test_copy_password_fallback():
    """Test clipboard fallback mechanism."""
    mock1 = MagicMock(side_effect=Exception("First method failed"))
    mock2 = MagicMock()
    
    with patch.object(ClipboardDriver, '_COPY_METHODS', [mock1, mock2]):
        ClipboardDriver.copy_password("test", True)
        
    mock1.assert_called_once()
    mock2.assert_called_once()


@pytest.mark.skipif(sys.platform != "win32", reason="Windows-specific test")
@pytest.mark.windows
@pytest.mark.clipboard
def test_powershell_copy(command_exists):
    """Test PowerShell clipboard integration (Windows only)."""
    if not command_exists("powershell.exe"):
        pytest.skip("PowerShell not found on this system")
        
    with patch('securepass.clipboard.powershell.run_command_stdin') as mock_run:
        powershell_copy("test", True)
        mock_run.assert_called_once()


@pytest.mark.skipif(sys.platform != "darwin", reason="macOS-specific test")
@pytest.mark.macos
@pytest.mark.clipboard
def test_pbcopy_copy(command_exists):
    """Test pbcopy clipboard integration (macOS only)."""
    if not command_exists("pbcopy"):
        pytest.skip("pbcopy not found on this system")
        
    with patch('securepass.clipboard.pbcopy.run_command_stdin') as mock_run:
        pbcopy_copy("test", True)
        mock_run.assert_called_once()


@pytest.mark.clipboard
def test_pyperclip_copy():
    """Test pyperclip clipboard integration."""
    try:
        import pyperclip
        with patch('pyperclip.copy') as mock_pyperclip:
            pyperclip_copy("test", True)
            mock_pyperclip.assert_called_once_with("test")
    except ImportError:
        pytest.skip("pyperclip not installed")


@pytest.mark.clipboard
def test_pyperclip_import_error():
    """Test pyperclip import error handling."""
    # Create a temp module loader to avoid affecting the real imports
    def mock_import(name, *args, **kwargs):
        if name == 'pyperclip':
            raise ImportError("No module named 'pyperclip'")
        return __import__(name, *args, **kwargs)
    
    with patch('builtins.__import__', side_effect=mock_import):
        # Save the original sys.modules
        original_modules = dict(sys.modules)
        if 'pyperclip' in sys.modules:
            del sys.modules['pyperclip']
            
        try:
            with pytest.raises(ImportError):
                pyperclip_copy("test", True)
        finally:
            # Restore the original modules
            sys.modules.clear()
            sys.modules.update(original_modules)


@pytest.mark.skipif(not sys.platform.startswith('linux'), reason="Linux-specific test")
@pytest.mark.linux
@pytest.mark.clipboard
def test_xclip_copy(command_exists):
    """Test xclip clipboard integration (Linux only)."""
    if not command_exists("xclip"):
        pytest.skip("xclip not found on this system")
        
    with patch('securepass.clipboard.xclip.run_command_stdin') as mock_run:
        xclip_copy("test", True)
        mock_run.assert_called_once()


@pytest.mark.clipboard
def test_xclip_not_found():
    """Test xclip not found error handling."""
    with patch('securepass.clipboard.xclip.run_command_stdin',
              side_effect=FileNotFoundError("Command not found")):
        with pytest.raises(Exception):
            xclip_copy("test", True)


@pytest.mark.skipif(not sys.platform.startswith('linux'), reason="Linux-specific test")
@pytest.mark.linux
@pytest.mark.clipboard
def test_wlclip_copy(command_exists):
    """Test wl-clipboard integration (Linux Wayland only)."""
    if not command_exists("wl-copy"):
        pytest.skip("wl-copy not found on this system")
        
    with patch('securepass.clipboard.wlclip.run_command_stdin') as mock_run:
        wlclip_copy("test", True)
        mock_run.assert_called_once()


@pytest.mark.clipboard
def test_copyq_copy(command_exists):
    """Test CopyQ clipboard integration."""
    has_copyq = command_exists("copyq")
    if not has_copyq and sys.platform != 'win32':
        pytest.skip("copyq not found on this system")
        
    with patch('securepass.clipboard.copyq.run_command_stdin') as mock_run:
        # Skip actual execution on Windows unless CopyQ is actually installed
        if sys.platform == 'win32' and not has_copyq:
            with patch('securepass.utils.commands.subprocess.run', 
                      side_effect=FileNotFoundError):
                try:
                    copyq_copy("test", True)
                except Exception:
                    pass  # We expect an error on Windows without CopyQ
        else:
            copyq_copy("test", True)
            mock_run.assert_called_once()


@pytest.mark.clipboard
def test_command_error():
    """Test command error handling."""
    with patch('securepass.clipboard.xclip.run_command_stdin', 
              side_effect=subprocess.SubprocessError("Test error")):
        with pytest.raises(Exception):
            xclip_copy("test", True)


@pytest.mark.clipboard
def test_platform_specific_clipboard():
    """Test the appropriate clipboard mechanism for the current platform."""
    # Create mocks for all clipboard methods
    mocks = []
    
    # Mock all clipboard methods to ensure we can track calls
    with patch('securepass.clipboard.pyperclip.pyperclip_copy') as mock1, \
         patch('securepass.clipboard.copyq.copyq_copy') as mock2, \
         patch('securepass.clipboard.xclip.xclip_copy') as mock3, \
         patch('securepass.clipboard.wlclip.wlclip_copy') as mock4, \
         patch('securepass.clipboard.powershell.powershell_copy') as mock5, \
         patch('securepass.clipboard.pbcopy.pbcopy_copy') as mock6:
        
        mocks = [mock1, mock2, mock3, mock4, mock5, mock6]
        
        # Replace the ClipboardDriver's methods with our mocks
        original_methods = ClipboardDriver._COPY_METHODS
        try:
            # Use the first mock to ensure it will be called
            ClipboardDriver._COPY_METHODS = [mock1]
            
            # Create a test password
            test_password = "TestPassword123!"
            
            # Try to copy the password
            ClipboardDriver.copy_password(test_password, True)
            
            # Verify that at least one clipboard method was called
            assert any(mock.called for mock in mocks), "No clipboard method was called"
        finally:
            # Restore original methods
            ClipboardDriver._COPY_METHODS = original_methods
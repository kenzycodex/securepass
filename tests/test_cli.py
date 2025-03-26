import pytest
import sys
from unittest.mock import patch, MagicMock
import subprocess
from securepass.clipboard import ClipboardDriver
from securepass.clipboard.pyperclip import pyperclip_copy
from securepass.clipboard.copyq import copyq_copy
from securepass.clipboard.xclip import xclip_copy
from securepass.clipboard.wlclip import wlclip_copy
from securepass.clipboard.powershell import powershell_copy
from securepass.clipboard.pbcopy import pbcopy_copy


def test_copy_password_success():
    """Test successful password copying."""
    mock_method = MagicMock()
    with patch.object(ClipboardDriver, '_COPY_METHODS', [mock_method]):
        ClipboardDriver.copy_password("test", True)
        mock_method.assert_called_once_with("test", True)


def test_copy_password_failure():
    """Test clipboard failure handling."""
    mock_method = MagicMock(side_effect=Exception("Test error"))
    with patch.object(ClipboardDriver, '_COPY_METHODS', [mock_method]):
        with pytest.raises(RuntimeError, match="Failed to copy to clipboard"):
            ClipboardDriver.copy_password("test", True)


def test_copy_password_fallback():
    """Test clipboard fallback mechanism."""
    mock1 = MagicMock(side_effect=Exception("First method failed"))
    mock2 = MagicMock()
    
    with patch.object(ClipboardDriver, '_COPY_METHODS', [mock1, mock2]):
        ClipboardDriver.copy_password("test", True)
        
    mock1.assert_called_once()
    mock2.assert_called_once()


# Note this test is skipped unless on Windows
@pytest.mark.skipif(sys.platform != "win32", reason="Windows-specific test")
def test_powershell_copy():
    """Test PowerShell clipboard integration (Windows only)."""
    with patch('securepass.clipboard.powershell.run_command_stdin') as mock_run:
        powershell_copy("test", True)
        mock_run.assert_called_once()


# Note this test is skipped unless on macOS
@pytest.mark.skipif(sys.platform != "darwin", reason="macOS-specific test")
def test_pbcopy_copy():
    """Test pbcopy clipboard integration (macOS only)."""
    with patch('securepass.clipboard.pbcopy.run_command_stdin') as mock_run:
        pbcopy_copy("test", True)
        mock_run.assert_called_once()


def test_pyperclip_copy():
    """Test pyperclip clipboard integration."""
    with patch('pyperclip.copy') as mock_pyperclip:
        pyperclip_copy("test", True)
        mock_pyperclip.assert_called_once_with("test")


def test_pyperclip_import_error():
    """Test pyperclip import error handling."""
    with patch('builtins.__import__', side_effect=ImportError("No module named 'pyperclip'")):
        with pytest.raises(ImportError):
            # We need to use a fresh local function to test the import error
            # since the module is already imported in the test file
            from securepass.clipboard.pyperclip import pyperclip_copy as fresh_copy
            fresh_copy("test", True)


def test_xclip_copy():
    """Test xclip clipboard integration."""
    with patch('securepass.clipboard.xclip.run_command_stdin') as mock_run:
        xclip_copy("test", True)
        mock_run.assert_called_once()


def test_xclip_not_found():
    """Test xclip not found error."""
    with patch('securepass.clipboard.xclip.run_command_stdin', side_effect=FileNotFoundError("Command not found")):
        with pytest.raises(Exception):
            xclip_copy("test", True)


def test_wlclip_copy():
    """Test wl-clipboard integration."""
    with patch('securepass.clipboard.wlclip.run_command_stdin') as mock_run:
        wlclip_copy("test", True)
        mock_run.assert_called_once()


def test_copyq_copy():
    """Test CopyQ clipboard integration."""
    with patch('securepass.clipboard.copyq.run_command_stdin') as mock_run:
        copyq_copy("test", True)
        mock_run.assert_called_once()


def test_command_error():
    """Test command error handling."""
    with patch('securepass.clipboard.xclip.run_command_stdin', side_effect=subprocess.SubprocessError("Test error")):
        with pytest.raises(Exception):
            xclip_copy("test", True)
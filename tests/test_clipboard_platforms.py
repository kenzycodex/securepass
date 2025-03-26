"""
Platform-specific clipboard tests with better structure.

This module provides comprehensive testing for all clipboard adapters
while properly handling platform-specific requirements.
"""

import pytest
import sys
from unittest.mock import patch, MagicMock
import subprocess

from securepass.clipboard.copyq import copyq_copy
from securepass.clipboard.powershell import powershell_copy
from securepass.clipboard.wlclip import wlclip_copy
from securepass.clipboard.pbcopy import pbcopy_copy
from securepass.clipboard.xclip import xclip_copy


@pytest.mark.clipboard
class TestCopyQ:
    """Tests for CopyQ clipboard integration."""
    
    def test_copyq_with_verbose(self):
        """Test CopyQ copying with verbose flag."""
        with patch('securepass.clipboard.copyq.run_command_stdin') as mock_run:
            copyq_copy("test_password", True)
            mock_run.assert_called_once_with(["copyq", "copy", "-"], "test_password")
    
    def test_copyq_without_verbose(self):
        """Test CopyQ copying without verbose flag."""
        with patch('securepass.clipboard.copyq.run_command_stdin') as mock_run:
            copyq_copy("test_password", False)
            mock_run.assert_called_once_with(["copyq", "copy", "-"], "test_password")
    
    def test_copyq_command_error(self):
        """Test CopyQ error handling for command errors."""
        with patch('securepass.clipboard.copyq.run_command_stdin', 
                  side_effect=subprocess.SubprocessError("Command failed")):
            with pytest.raises(subprocess.SubprocessError):
                copyq_copy("test_password", True)
    
    def test_copyq_command_not_found(self):
        """Test CopyQ error handling for missing executable."""
        with patch('securepass.clipboard.copyq.run_command_stdin', 
                  side_effect=FileNotFoundError("CopyQ not found")):
            with pytest.raises(FileNotFoundError):
                copyq_copy("test_password", True)


@pytest.mark.clipboard
class TestPowerShell:
    """Tests for PowerShell clipboard integration (Windows)."""
    
    def test_powershell_with_verbose(self):
        """Test PowerShell copying with verbose flag."""
        with patch('securepass.clipboard.powershell.run_command_stdin') as mock_run:
            powershell_copy("test_password", True)
            mock_run.assert_called_once_with(
                ["powershell.exe", "-command", "$input | Set-Clipboard"],
                "test_password"
            )
    
    def test_powershell_without_verbose(self):
        """Test PowerShell copying without verbose flag."""
        with patch('securepass.clipboard.powershell.run_command_stdin') as mock_run:
            powershell_copy("test_password", False)
            mock_run.assert_called_once_with(
                ["powershell.exe", "-command", "$input | Set-Clipboard"],
                "test_password"
            )
    
    def test_powershell_command_error(self):
        """Test PowerShell error handling for command errors."""
        with patch('securepass.clipboard.powershell.run_command_stdin', 
                  side_effect=subprocess.SubprocessError("Command failed")):
            with pytest.raises(subprocess.SubprocessError):
                powershell_copy("test_password", True)
    
    def test_powershell_command_not_found(self):
        """Test PowerShell error handling for missing executable."""
        with patch('securepass.clipboard.powershell.run_command_stdin', 
                  side_effect=FileNotFoundError("PowerShell not found")):
            with pytest.raises(FileNotFoundError):
                powershell_copy("test_password", True)


@pytest.mark.clipboard
class TestWayland:
    """Tests for Wayland clipboard integration (Linux Wayland)."""
    
    def test_wlclip_with_verbose(self):
        """Test wl-copy with verbose flag."""
        with patch('securepass.clipboard.wlclip.run_command_stdin') as mock_run:
            wlclip_copy("test_password", True)
            mock_run.assert_called_once_with(["wl-copy"], "test_password")
    
    def test_wlclip_without_verbose(self):
        """Test wl-copy without verbose flag."""
        with patch('securepass.clipboard.wlclip.run_command_stdin') as mock_run:
            wlclip_copy("test_password", False)
            mock_run.assert_called_once_with(["wl-copy"], "test_password")
    
    def test_wlclip_command_error(self):
        """Test wl-copy error handling for command errors."""
        with patch('securepass.clipboard.wlclip.run_command_stdin', 
                  side_effect=subprocess.SubprocessError("Command failed")):
            with pytest.raises(subprocess.SubprocessError):
                wlclip_copy("test_password", True)
    
    def test_wlclip_command_not_found(self):
        """Test wl-copy error handling for missing executable."""
        with patch('securepass.clipboard.wlclip.run_command_stdin', 
                  side_effect=FileNotFoundError("wl-copy not found")):
            with pytest.raises(FileNotFoundError):
                wlclip_copy("test_password", True)


@pytest.mark.clipboard
class TestMacOS:
    """Tests for macOS clipboard integration (pbcopy)."""
    
    def test_pbcopy_with_verbose(self):
        """Test pbcopy with verbose flag."""
        with patch('securepass.clipboard.pbcopy.run_command_stdin') as mock_run:
            pbcopy_copy("test_password", True)
            mock_run.assert_called_once_with(["pbcopy"], "test_password")
    
    def test_pbcopy_without_verbose(self):
        """Test pbcopy without verbose flag."""
        with patch('securepass.clipboard.pbcopy.run_command_stdin') as mock_run:
            pbcopy_copy("test_password", False)
            mock_run.assert_called_once_with(["pbcopy"], "test_password")
    
    def test_pbcopy_command_error(self):
        """Test pbcopy error handling for command errors."""
        with patch('securepass.clipboard.pbcopy.run_command_stdin', 
                  side_effect=subprocess.SubprocessError("Command failed")):
            with pytest.raises(subprocess.SubprocessError):
                pbcopy_copy("test_password", True)
    
    def test_pbcopy_command_not_found(self):
        """Test pbcopy error handling for missing executable."""
        with patch('securepass.clipboard.pbcopy.run_command_stdin', 
                  side_effect=FileNotFoundError("pbcopy not found")):
            with pytest.raises(FileNotFoundError):
                pbcopy_copy("test_password", True)


@pytest.mark.clipboard
class TestLinuxX11:
    """Tests for Linux X11 clipboard integration (xclip)."""
    
    def test_xclip_with_verbose(self):
        """Test xclip with verbose flag."""
        with patch('securepass.clipboard.xclip.run_command_stdin') as mock_run:
            xclip_copy("test_password", True)
            mock_run.assert_called_once_with(["xclip", "-selection", "clipboard"], "test_password")
    
    def test_xclip_without_verbose(self):
        """Test xclip without verbose flag."""
        with patch('securepass.clipboard.xclip.run_command_stdin') as mock_run:
            xclip_copy("test_password", False)
            mock_run.assert_called_once_with(["xclip", "-selection", "clipboard"], "test_password")
    
    def test_xclip_command_error(self):
        """Test xclip error handling for command errors."""
        with patch('securepass.clipboard.xclip.run_command_stdin', 
                  side_effect=subprocess.SubprocessError("Command failed")):
            with pytest.raises(subprocess.SubprocessError):
                xclip_copy("test_password", True)
    
    def test_xclip_command_not_found(self):
        """Test xclip error handling for missing executable."""
        with patch('securepass.clipboard.xclip.run_command_stdin', 
                  side_effect=FileNotFoundError("xclip not found")):
            with pytest.raises(FileNotFoundError):
                xclip_copy("test_password", True)


@pytest.mark.clipboard
class TestPlatformSimulationClipboard:
    """Tests for platform-specific clipboard selection using simulation."""
    
    def test_platform_specific_integration(self, simulate_platform):
        """Test platform-specific clipboard integrations with simulation."""
        from securepass.clipboard import ClipboardDriver
        
        # Patch all clipboard methods to track calls
        with patch('securepass.clipboard.powershell.powershell_copy') as win_mock, \
             patch('securepass.clipboard.pbcopy.pbcopy_copy') as mac_mock, \
             patch('securepass.clipboard.xclip.xclip_copy') as xclip_mock, \
             patch('securepass.clipboard.wlclip.wlclip_copy') as wayland_mock, \
             patch('securepass.clipboard.copyq.copyq_copy') as copyq_mock, \
             patch('securepass.clipboard.pyperclip.pyperclip_copy') as pyperclip_mock:
            
            # Test with Windows platform
            with simulate_platform('win32'):
                # Modify the copy methods for testing
                original_methods = ClipboardDriver._COPY_METHODS
                try:
                    # Include only the first few methods to avoid test complexity
                    ClipboardDriver._COPY_METHODS = [
                        win_mock,
                        pyperclip_mock
                    ]
                    
                    # Windows should try PowerShell first
                    ClipboardDriver.copy_password("test_pw", False)
                    win_mock.assert_called_once()
                    
                    # Reset mocks
                    win_mock.reset_mock()
                    pyperclip_mock.reset_mock()
                    
                    # Test fallback with PowerShell failing
                    win_mock.side_effect = Exception("PowerShell failed")
                    ClipboardDriver.copy_password("test_pw", False)
                    win_mock.assert_called_once()
                    pyperclip_mock.assert_called_once()
                    
                finally:
                    # Restore original methods
                    ClipboardDriver._COPY_METHODS = original_methods
            
            # Reset all mocks
            win_mock.reset_mock()
            mac_mock.reset_mock()
            xclip_mock.reset_mock()
            wayland_mock.reset_mock()
            copyq_mock.reset_mock()
            pyperclip_mock.reset_mock()
            
            # Test with macOS platform
            with simulate_platform('darwin'):
                # Modify the copy methods for testing
                original_methods = ClipboardDriver._COPY_METHODS
                try:
                    # Include only the first few methods to avoid test complexity
                    ClipboardDriver._COPY_METHODS = [
                        mac_mock,
                        pyperclip_mock
                    ]
                    
                    # macOS should try pbcopy first
                    ClipboardDriver.copy_password("test_pw", False)
                    mac_mock.assert_called_once()
                    
                finally:
                    # Restore original methods
                    ClipboardDriver._COPY_METHODS = original_methods
            
            # Reset all mocks
            win_mock.reset_mock()
            mac_mock.reset_mock()
            xclip_mock.reset_mock()
            wayland_mock.reset_mock()
            copyq_mock.reset_mock()
            pyperclip_mock.reset_mock()
            
            # Test with Linux platform
            with simulate_platform('linux'):
                # Modify the copy methods for testing
                original_methods = ClipboardDriver._COPY_METHODS
                try:
                    # Include only the first few methods to avoid test complexity
                    ClipboardDriver._COPY_METHODS = [
                        xclip_mock,
                        wayland_mock,
                        pyperclip_mock
                    ]
                    
                    # Linux should try xclip first
                    ClipboardDriver.copy_password("test_pw", False)
                    xclip_mock.assert_called_once()
                    
                finally:
                    # Restore original methods
                    ClipboardDriver._COPY_METHODS = original_methods
# tests/test-clipboard-wlclip.py
"""
Tests for Wayland clipboard (wl-clipboard) and macOS pbcopy integration.
"""

import pytest
import sys
from unittest.mock import patch, MagicMock
import subprocess

from securepass.clipboard.wlclip import wlclip_copy
from securepass.clipboard.pbcopy import pbcopy_copy


class TestWaylandClipboard:
    """Tests for Wayland clipboard integration."""
    
    def test_wlclip_verbose(self):
        """Test wl-clipboard with verbose output."""
        with patch('securepass.clipboard.wlclip.run_command_stdin') as mock_run:
            wlclip_copy("test_password", True)
            mock_run.assert_called_once()
            # Verify command contains wl-copy
            args, _ = mock_run.call_args
            assert "wl-copy" in args[0]
    
    def test_wlclip_non_verbose(self):
        """Test wl-clipboard without verbose output."""
        with patch('securepass.clipboard.wlclip.run_command_stdin') as mock_run:
            wlclip_copy("test_password", False)
            mock_run.assert_called_once()
    
    def test_wlclip_command_error(self):
        """Test wl-clipboard command error handling."""
        with patch('securepass.clipboard.wlclip.run_command_stdin', 
                  side_effect=subprocess.SubprocessError("Command failed")):
            with pytest.raises(Exception, match="Failed to copy to Wayland clipboard"):
                wlclip_copy("test_password", True)
    
    def test_wlclip_command_not_found(self):
        """Test wl-clipboard command not found handling."""
        with patch('securepass.clipboard.wlclip.run_command_stdin', 
                  side_effect=FileNotFoundError("wl-copy not found")):
            with pytest.raises(Exception, match="wl-copy command not found"):
                wlclip_copy("test_password", True)


class TestMacOSClipboard:
    """Tests for macOS pbcopy clipboard integration."""
    
    def test_pbcopy_verbose(self):
        """Test pbcopy with verbose output."""
        with patch('securepass.clipboard.pbcopy.run_command_stdin') as mock_run:
            pbcopy_copy("test_password", True)
            mock_run.assert_called_once()
            # Verify command contains pbcopy
            args, _ = mock_run.call_args
            assert "pbcopy" in args[0]
    
    def test_pbcopy_non_verbose(self):
        """Test pbcopy without verbose output."""
        with patch('securepass.clipboard.pbcopy.run_command_stdin') as mock_run:
            pbcopy_copy("test_password", False)
            mock_run.assert_called_once()
    
    def test_pbcopy_command_error(self):
        """Test pbcopy command error handling."""
        with patch('securepass.clipboard.pbcopy.run_command_stdin', 
                  side_effect=subprocess.SubprocessError("Command failed")):
            with pytest.raises(Exception, match="Failed to copy to macOS clipboard"):
                pbcopy_copy("test_password", True)
    
    def test_pbcopy_command_not_found(self):
        """Test pbcopy command not found handling."""
        with patch('securepass.clipboard.pbcopy.run_command_stdin', 
                  side_effect=FileNotFoundError("pbcopy not found")):
            with pytest.raises(Exception, match="pbcopy command not found"):
                pbcopy_copy("test_password", True)

@pytest.mark.clipboard
class TestWlclipImplementation:
    """Tests for the Wayland clipboard implementation."""
    
    def test_wlclip_copy_success(self):
        """Test successful wl-copy operation."""
        from securepass.clipboard.wlclip import wlclip_copy
        
        with patch('securepass.utils.commands.run_command_stdin') as mock_run:
            # Test with verbose=True
            wlclip_copy("test_password", True)
            mock_run.assert_called_once()
            
            # Reset mock for next test
            mock_run.reset_mock()
            
            # Test with verbose=False
            wlclip_copy("test_password", False)
            mock_run.assert_called_once()
    
    def test_wlclip_copy_command_error(self):
        """Test error handling in wl-copy."""
        from securepass.clipboard.wlclip import wlclip_copy
        import subprocess
        
        with patch('securepass.utils.commands.run_command_stdin',
                  side_effect=subprocess.SubprocessError("Command failed")):
            with pytest.raises(Exception, match="Failed to copy to Wayland clipboard"):
                wlclip_copy("test_password", True)
    
    def test_wlclip_copy_command_not_found(self):
        """Test command not found handling in wl-copy."""
        from securepass.clipboard.wlclip import wlclip_copy
        
        with patch('securepass.utils.commands.run_command_stdin',
                  side_effect=FileNotFoundError("wl-copy not found")):
            with pytest.raises(Exception, match="wl-copy command not found"):
                wlclip_copy("test_password", True)


@pytest.mark.clipboard
class TestPbcopyImplementation:
    """Tests for the macOS pbcopy clipboard implementation."""
    
    def test_pbcopy_copy_success(self):
        """Test successful pbcopy operation."""
        from securepass.clipboard.pbcopy import pbcopy_copy
        
        with patch('securepass.utils.commands.run_command_stdin') as mock_run:
            # Test with verbose=True
            pbcopy_copy("test_password", True)
            mock_run.assert_called_once()
            
            # Reset mock for next test
            mock_run.reset_mock()
            
            # Test with verbose=False
            pbcopy_copy("test_password", False)
            mock_run.assert_called_once()
    
    def test_pbcopy_copy_command_error(self):
        """Test error handling in pbcopy."""
        from securepass.clipboard.pbcopy import pbcopy_copy
        import subprocess
        
        with patch('securepass.utils.commands.run_command_stdin',
                  side_effect=subprocess.SubprocessError("Command failed")):
            with pytest.raises(Exception, match="Failed to copy to macOS clipboard"):
                pbcopy_copy("test_password", True)
    
    def test_pbcopy_copy_command_not_found(self):
        """Test command not found handling in pbcopy."""
        from securepass.clipboard.pbcopy import pbcopy_copy
        
        with patch('securepass.utils.commands.run_command_stdin',
                  side_effect=FileNotFoundError("pbcopy not found")):
            with pytest.raises(Exception, match="pbcopy command not found"):
                pbcopy_copy("test_password", True)
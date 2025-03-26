# tests/test_clipboard_powerq.py
"""
Tests for PowerShell and CopyQ clipboard integration.
"""

import pytest
import sys
from unittest.mock import patch, MagicMock
import subprocess

from securepass.clipboard.powershell import powershell_copy
from securepass.clipboard.copyq import copyq_copy


class TestPowerShellClipboard:
    """Tests for PowerShell clipboard integration."""
    
    def test_powershell_verbose(self):
        """Test PowerShell clipboard with verbose output."""
        with patch('securepass.clipboard.powershell.run_command_stdin') as mock_run:
            powershell_copy("test_password", True)
            mock_run.assert_called_once()
            # Verify command contains powershell
            args, _ = mock_run.call_args
            assert "powershell" in args[0][0].lower()
    
    def test_powershell_non_verbose(self):
        """Test PowerShell clipboard without verbose output."""
        with patch('securepass.clipboard.powershell.run_command_stdin') as mock_run:
            powershell_copy("test_password", False)
            mock_run.assert_called_once()
    
    def test_powershell_command_error(self):
        """Test PowerShell clipboard command error handling."""
        with patch('securepass.clipboard.powershell.run_command_stdin', 
                  side_effect=subprocess.SubprocessError("Command failed")):
            with pytest.raises(Exception, match="Failed to copy to Windows clipboard"):
                powershell_copy("test_password", True)
    
    def test_powershell_command_not_found(self):
        """Test PowerShell clipboard command not found handling."""
        with patch('securepass.clipboard.powershell.run_command_stdin', 
                  side_effect=FileNotFoundError("powershell not found")):
            with pytest.raises(Exception, match="PowerShell command not found"):
                powershell_copy("test_password", True)


class TestCopyQClipboard:
    """Tests for CopyQ clipboard integration."""
    
    def test_copyq_verbose(self):
        """Test CopyQ clipboard with verbose output."""
        with patch('securepass.clipboard.copyq.run_command_stdin') as mock_run:
            copyq_copy("test_password", True)
            mock_run.assert_called_once()
            # Verify command contains copyq
            args, _ = mock_run.call_args
            assert "copyq" in args[0][0].lower()
    
    def test_copyq_non_verbose(self):
        """Test CopyQ clipboard without verbose output."""
        with patch('securepass.clipboard.copyq.run_command_stdin') as mock_run:
            copyq_copy("test_password", False)
            mock_run.assert_called_once()
    
    def test_copyq_command_error(self):
        """Test CopyQ clipboard command error handling."""
        with patch('securepass.clipboard.copyq.run_command_stdin', 
                  side_effect=subprocess.SubprocessError("Command failed")):
            with pytest.raises(Exception, match="Failed to copy to CopyQ clipboard"):
                copyq_copy("test_password", True)
    
    def test_copyq_command_not_found(self):
        """Test CopyQ clipboard command not found handling."""
        with patch('securepass.clipboard.copyq.run_command_stdin', 
                  side_effect=FileNotFoundError("copyq not found")):
            with pytest.raises(Exception, match="CopyQ command not found"):
                copyq_copy("test_password", True)

@pytest.mark.clipboard
class TestPowerShellImplementation:
    """Tests for the Windows PowerShell clipboard implementation."""
    
    def test_powershell_copy_success(self):
        """Test successful PowerShell clipboard operation."""
        from securepass.clipboard.powershell import powershell_copy
        
        with patch('securepass.utils.commands.run_command_stdin') as mock_run:
            # Test with verbose=True
            powershell_copy("test_password", True)
            mock_run.assert_called_once()
            
            # Reset mock for next test
            mock_run.reset_mock()
            
            # Test with verbose=False
            powershell_copy("test_password", False)
            mock_run.assert_called_once()
    
    def test_powershell_copy_command_error(self):
        """Test error handling in PowerShell."""
        from securepass.clipboard.powershell import powershell_copy
        import subprocess
        
        with patch('securepass.utils.commands.run_command_stdin',
                  side_effect=subprocess.SubprocessError("Command failed")):
            with pytest.raises(Exception, match="Failed to copy to Windows clipboard"):
                powershell_copy("test_password", True)
    
    def test_powershell_copy_command_not_found(self):
        """Test command not found handling in PowerShell."""
        from securepass.clipboard.powershell import powershell_copy
        
        with patch('securepass.utils.commands.run_command_stdin',
                  side_effect=FileNotFoundError("PowerShell not found")):
            with pytest.raises(Exception, match="PowerShell command not found"):
                powershell_copy("test_password", True)


@pytest.mark.clipboard
class TestCopyQImplementation:
    """Tests for the CopyQ clipboard implementation."""
    
    def test_copyq_copy_success(self):
        """Test successful CopyQ clipboard operation."""
        from securepass.clipboard.copyq import copyq_copy
        
        with patch('securepass.utils.commands.run_command_stdin') as mock_run:
            # Test with verbose=True
            copyq_copy("test_password", True)
            mock_run.assert_called_once()
            
            # Reset mock for next test
            mock_run.reset_mock()
            
            # Test with verbose=False
            copyq_copy("test_password", False)
            mock_run.assert_called_once()
    
    def test_copyq_copy_command_error(self):
        """Test error handling in CopyQ."""
        from securepass.clipboard.copyq import copyq_copy
        import subprocess
        
        with patch('securepass.utils.commands.run_command_stdin',
                  side_effect=subprocess.SubprocessError("Command failed")):
            with pytest.raises(Exception, match="Failed to copy to CopyQ clipboard"):
                copyq_copy("test_password", True)
    
    def test_copyq_copy_command_not_found(self):
        """Test command not found handling in CopyQ."""
        from securepass.clipboard.copyq import copyq_copy
        
        with patch('securepass.utils.commands.run_command_stdin',
                  side_effect=FileNotFoundError("CopyQ not found")):
            with pytest.raises(Exception, match="CopyQ command not found"):
                copyq_copy("test_password", True)
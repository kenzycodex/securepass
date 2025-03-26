import pytest
import subprocess
import sys
import io
from unittest.mock import patch, MagicMock
from securepass.utils.vprint import vprint, vprint_if
from securepass.utils.commands import run_command_stdin


def test_vprint(capsys):
    """Test verbose print function."""
    # Test with verbose=True
    vprint(True, "test message")
    captured = capsys.readouterr()
    assert "test message" in captured.err
    
    # Test with verbose=False
    vprint(False, "test message")
    captured = capsys.readouterr()
    assert captured.err == ""
    
    # Test with additional arguments
    vprint(True, "test", "additional", file=sys.stdout)
    captured = capsys.readouterr()
    assert "test additional" in captured.out


def test_vprint_attribute(capsys):
    """Test vprint.vprint attribute function."""
    # Test with verbose=True
    vprint.vprint(True, "test message")
    captured = capsys.readouterr()
    assert "test message" in captured.err
    
    # Test with verbose=False
    vprint.vprint(False, "test message")
    captured = capsys.readouterr()
    assert captured.err == ""


def test_vprint_if():
    """Test vprint_if function."""
    # Use StringIO instead of capsys for more reliable testing
    test_file = io.StringIO()
    
    # Test with condition=True
    result = vprint_if(True, "test message", file=test_file)
    assert result is True
    assert "test message" in test_file.getvalue()
    
    # Clear the StringIO for the next test
    test_file = io.StringIO()
    
    # Test with condition=False
    result = vprint_if(False, "test message", file=test_file)
    assert result is False
    assert test_file.getvalue() == ""


def test_run_command_stdin():
    """Test run_command_stdin function."""
    # Platform-specific test command
    command = ["echo"] if sys.platform != "win32" else ["cmd", "/c", "echo"]
    
    # Mock subprocess.run to avoid actual command execution
    mock_run = MagicMock()
    with patch('subprocess.run', mock_run):
        run_command_stdin(command, "test input")
        mock_run.assert_called_once()


def test_run_command_stdin_error():
    """Test run_command_stdin error handling."""
    # Test with CalledProcessError
    with patch('subprocess.run', side_effect=subprocess.CalledProcessError(1, ["test"], stderr="error")):
        with pytest.raises(subprocess.SubprocessError):
            run_command_stdin(["test"], "input")
    
    # Test with FileNotFoundError
    with patch('subprocess.run', side_effect=FileNotFoundError):
        with pytest.raises(subprocess.SubprocessError):
            run_command_stdin(["nonexistent_command"], "input")
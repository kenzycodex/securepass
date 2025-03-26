import subprocess
from typing import List


def run_command_stdin(command: List[str], stdin: str) -> None:
    """Run a command with stdin input.
    
    Args:
        command: Command to run as list of strings
        stdin: Input to pass to command's stdin
        
    Raises:
        subprocess.SubprocessError: If command fails
    """
    try:
        # Explicitly pass text=True to ensure string input 
        # and encode/decode handled correctly
        result = subprocess.run(
            command,
            input=stdin,  # Use string directly
            capture_output=True,
            text=True,  # Ensure text mode
            check=True
        )
    except subprocess.CalledProcessError as e:
        # Modify to ensure it raises SubprocessError for any command failure
        raise subprocess.SubprocessError(
            f"Command failed: {e.cmd}\n"
            f"Return code: {e.returncode}\n"
            f"Error output: {e.stderr.strip()}"
        )
    except FileNotFoundError:
        # Explicitly raise SubprocessError for non-existent commands
        raise subprocess.SubprocessError(f"Command not found: {command}")
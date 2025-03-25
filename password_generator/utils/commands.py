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
        subprocess.run(
            command,
            input=stdin.encode(),
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except subprocess.CalledProcessError as e:
        raise subprocess.SubprocessError(
            f"Command failed: {e.cmd}\n"
            f"Return code: {e.returncode}\n"
            f"Error output: {e.stderr.decode().strip()}"
        )
from password_generator.utils.vprint import vprint
from password_generator.utils.commands import run_command_stdin


def powershell_copy(string: str, verbose: bool = False) -> None:
    """Copy string to clipboard using PowerShell (Windows).
    
    Args:
        string: String to copy
        verbose: Show verbose output
    """
    try:
        run_command_stdin(
            ["powershell.exe", "-command", "$input | Set-Clipboard"],
            string
        )
        vprint(verbose, "[SUCCESS] Copied to clipboard using PowerShell")
    except FileNotFoundError:
        vprint(verbose, "[WARNING] PowerShell not found")
        raise
    except Exception as e:
        vprint(verbose, f"[ERROR] PowerShell failed: {str(e)}")
        raise
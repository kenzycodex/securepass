#securepass/clipboard/pbcopy.py
from securepass.utils.vprint import vprint
from securepass.utils.commands import run_command_stdin


def pbcopy_copy(string: str, verbose: bool = False) -> None:
    """Copy string to clipboard using pbcopy (macOS).
    
    Args:
        string: String to copy
        verbose: Show verbose output
    """
    try:
        run_command_stdin(["pbcopy"], string)
        vprint(verbose, "[SUCCESS] Copied to clipboard using pbcopy")
    except FileNotFoundError:
        vprint(verbose, "[WARNING] pbcopy not found")
        raise
    except Exception as e:
        vprint(verbose, f"[ERROR] pbcopy failed: {str(e)}")
        raise
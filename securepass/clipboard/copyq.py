#securepass/clipboard/copyq.py
from securepass.utils.vprint import vprint
from securepass.utils.commands import run_command_stdin


def copyq_copy(string: str, verbose: bool = False) -> None:
    """Copy string to clipboard using CopyQ.
    
    Args:
        string: String to copy
        verbose: Show verbose output
    """
    try:
        run_command_stdin(["copyq", "copy", "-"], string)
        vprint(verbose, "[SUCCESS] Copied to clipboard using CopyQ")
    except FileNotFoundError:
        vprint(verbose, "[WARNING] CopyQ not found")
        raise
    except Exception as e:
        vprint(verbose, f"[ERROR] CopyQ failed: {str(e)}")
        raise
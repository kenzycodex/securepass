#securepass/clipboard/xclip.py
from securepass.utils.vprint import vprint
from securepass.utils.commands import run_command_stdin


def xclip_copy(string: str, verbose: bool = False) -> None:
    """Copy string to clipboard using xclip (Linux X11).
    
    Args:
        string: String to copy
        verbose: Show verbose output
    """
    try:
        run_command_stdin(["xclip", "-selection", "clipboard"], string)
        vprint(verbose, "[SUCCESS] Copied to clipboard using xclip")
    except FileNotFoundError:
        vprint(verbose, "[WARNING] xclip not found")
        raise
    except Exception as e:
        vprint(verbose, f"[ERROR] xclip failed: {str(e)}")
        raise
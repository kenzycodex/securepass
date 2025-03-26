#securepass/clipboard/pyperclip.py
from securepass.utils.vprint import vprint

def import_pyperclip():
    """Safely import pyperclip."""
    try:
        import pyperclip
        return pyperclip
    except ImportError as e:
        raise ImportError(f"Pyperclip not installed: {str(e)}")

def pyperclip_copy(string: str, verbose: bool = False) -> None:
    """Copy string to clipboard using Pyperclip.

    Args:
        string: String to copy
        verbose: Show verbose output
    """
    try:
        pyperclip = import_pyperclip()
        pyperclip.copy(string)
        vprint(verbose, "[SUCCESS] Copied to clipboard using Pyperclip")
    except ImportError as e:
        vprint(verbose, f"[WARNING] {str(e)}")
        raise
    except Exception as e:
        vprint(verbose, f"[ERROR] Pyperclip failed: {str(e)}")
        raise
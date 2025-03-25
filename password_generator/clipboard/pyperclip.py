from password_generator.utils.vprint import vprint


def pyperclip_copy(string: str, verbose: bool = False) -> None:
    """Copy string to clipboard using Pyperclip.
    
    Args:
        string: String to copy
        verbose: Show verbose output
    """
    try:
        import pyperclip
        pyperclip.copy(string)
        vprint(verbose, "[SUCCESS] Copied to clipboard using Pyperclip")
    except ImportError:
        vprint(verbose, "[WARNING] Pyperclip not installed")
        raise
    except Exception as e:
        vprint(verbose, f"[ERROR] Pyperclip failed: {str(e)}")
        raise
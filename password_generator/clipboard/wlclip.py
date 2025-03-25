from password_generator.utils.vprint import vprint
from password_generator.utils.commands import run_command_stdin


def wlclip_copy(string: str, verbose: bool = False) -> None:
    """Copy string to clipboard using wl-clipboard (Wayland).
    
    Args:
        string: String to copy
        verbose: Show verbose output
    """
    try:
        run_command_stdin(["wl-copy"], string)
        vprint(verbose, "[SUCCESS] Copied to clipboard using wl-clipboard")
    except FileNotFoundError:
        vprint(verbose, "[WARNING] wl-copy not found")
        raise
    except Exception as e:
        vprint(verbose, f"[ERROR] wl-clipboard failed: {str(e)}")
        raise
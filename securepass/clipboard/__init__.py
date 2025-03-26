#securepass/clipboard/__init__.py
import sys
from typing import List, Callable
from .pyperclip import pyperclip_copy
from .copyq import copyq_copy
from .xclip import xclip_copy
from .wlclip import wlclip_copy
from .powershell import powershell_copy
from .pbcopy import pbcopy_copy


class ClipboardDriver:
    _COPY_METHODS: List[Callable[[str, bool], None]] = [
        pyperclip_copy,
        copyq_copy,
        xclip_copy,
        wlclip_copy,
        powershell_copy,
        pbcopy_copy,
    ]

    @staticmethod
    def copy_password(password: str, verbose: bool = False) -> None:
        """Copy password to clipboard using available methods.
        
        Args:
            password: Password to copy
            verbose: Whether to print verbose output
            
        Raises:
            RuntimeError: If no clipboard method succeeded
        """
        success = False
        for method in ClipboardDriver._COPY_METHODS:
            try:
                method(password, verbose)
                success = True
                break
            except Exception as e:
                if verbose:
                    print(f"[DEBUG] Clipboard method failed: {str(e)}", file=sys.stderr)
                continue

        if not success:
            raise RuntimeError("Failed to copy to clipboard - no available method worked")
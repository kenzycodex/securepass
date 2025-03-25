"""A secure password generator with cross-platform clipboard support.

This package provides:
- PasswordGenerator: For generating secure random passwords
- ClipboardDriver: For copying passwords to clipboard across platforms
"""

__version__ = "1.0.0"
__all__ = ["PasswordGenerator", "ClipboardDriver"]

from .generator import PasswordGenerator
from .clipboard import ClipboardDriver
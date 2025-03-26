"""
SecurePass: A secure password generator with cross-platform clipboard support.

This package provides:
- PasswordGenerator: For generating secure random passwords
- ClipboardDriver: For copying passwords to clipboard across platforms
- CLI interface: Command-line tool for quick password generation
"""

__version__ = "1.0.0"
__all__ = ["PasswordGenerator", "ClipboardDriver"]

from .generator import PasswordGenerator
from .clipboard import ClipboardDriver

try:
    from .compatibility import install_aliases
    install_aliases()
except ImportError:
    pass  # Compatibility module not essential
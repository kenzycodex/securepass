"""
Verbose Print Utility

Provides controlled output for debugging and user feedback.
"""

import sys
from typing import Any, TextIO, Optional

def vprint(
    verbose: bool,
    message: Any,
    *args: Any,
    file: Optional[TextIO] = None,
    **kwargs: Any
) -> None:
    """Conditionally print messages based on verbosity.
    
    Args:
        verbose: If True, print the message
        message: Message to print (can be any printable object)
        *args: Positional arguments to pass to print()
        file: Output stream (default: stderr)
        **kwargs: Keyword arguments to pass to print()
    """
    # Default to stderr if no file is specified
    if file is None:
        file = sys.stderr
    
    if verbose:
        # Ensure output is a string and goes to the specified file
        print(str(message), *args, file=file, **kwargs)

# Create a function with the same signature as vprint 
# that can be called as vprint.vprint()
def _vprint_internal(
    verbose: bool,
    message: Any,
    *args: Any,
    file: Optional[TextIO] = None,
    **kwargs: Any
) -> None:
    """Internal implementation of vprint for attribute access."""
    # Default to stderr if no file is specified
    if file is None:
        file = sys.stderr
    
    if verbose:
        # Ensure output is a string and goes to the specified file
        print(str(message), *args, file=file, **kwargs)

# Attach the implementation as an attribute
vprint.vprint = _vprint_internal

def vprint_if(
    condition: bool,
    message: Any,
    *args: Any,
    file: TextIO = sys.stderr,
    **kwargs: Any
) -> bool:
    """Print message if condition is True and return the condition.
    
    Useful for one-liners that need conditional printing.
    """
    if condition:
        print(message, *args, file=file, **kwargs)
    return condition
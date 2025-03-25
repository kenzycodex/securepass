import sys
from typing import Any


def vprint(verbose: bool, message: Any, **kwargs) -> None:
    """Conditionally print a message if verbose is True.
    
    Args:
        verbose: Whether to print the message
        message: Message to print
        kwargs: Additional arguments to pass to print()
    """
    if verbose:
        print(message, file=sys.stderr, **kwargs)
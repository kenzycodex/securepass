"""
Compatibility module for backwards compatibility.

This module creates aliases to support the transition from 'password_generator'
to 'securepass' as the package name.
"""

import sys
import importlib.util
import warnings

def is_module_available(module_name):
    """Check if a module can be imported."""
    return importlib.util.find_spec(module_name) is not None

def install_aliases():
    """Install aliases for backward compatibility.
    
    This function creates aliases from the old module names to the new ones
    to ensure that existing code and entry points continue to work.
    """
    # Only add aliases if the original module doesn't exist
    if not is_module_available('password_generator'):
        # First, ensure all securepass modules are imported
        import securepass
        
        # Import all necessary submodules to ensure they're in sys.modules
        try:
            import securepass.cli
        except ImportError:
            pass
            
        try:
            import securepass.generator
        except ImportError:
            pass
            
        try:
            import securepass.clipboard
        except ImportError:
            pass
            
        try:
            import securepass.utils
        except ImportError:
            pass
        
        # Create module aliases only for modules that exist
        sys.modules['password_generator'] = sys.modules['securepass']
        
        if 'securepass.cli' in sys.modules:
            sys.modules['password_generator.cli'] = sys.modules['securepass.cli']
            
        if 'securepass.generator' in sys.modules:
            sys.modules['password_generator.generator'] = sys.modules['securepass.generator']
            
        if 'securepass.clipboard' in sys.modules:
            sys.modules['password_generator.clipboard'] = sys.modules['securepass.clipboard']
            
        if 'securepass.utils' in sys.modules:
            sys.modules['password_generator.utils'] = sys.modules['securepass.utils']
            
        # Create deprecated alias classes
        class PasswordGenerator:
            """Compatibility class for password_generator.PasswordGenerator."""
            
            def __new__(cls, *args, **kwargs):
                from securepass.generator import PasswordGenerator as RealPasswordGenerator
                warnings.warn(
                    "password_generator.PasswordGenerator is deprecated; "
                    "use securepass.PasswordGenerator instead",
                    DeprecationWarning, stacklevel=2
                )
                return RealPasswordGenerator(*args, **kwargs)
        
        # Add classes to the old module namespace
        sys.modules['password_generator'].PasswordGenerator = PasswordGenerator
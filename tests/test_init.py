"""
Tests for the package initialization module.
"""

import pytest
import sys
import importlib
from unittest.mock import patch, MagicMock
import warnings

# Ensure we don't affect the existing modules
@pytest.fixture
def clean_modules():
    """Fixture to temporarily clean up modules for testing."""
    # Save the original modules
    original_modules = dict(sys.modules)
    
    # Yield control back to the test
    yield
    
    # Restore original modules after test
    for module_name in list(sys.modules.keys()):
        if module_name not in original_modules:
            del sys.modules[module_name]
    
    # Explicitly restore any replaced modules
    for module_name, module in original_modules.items():
        sys.modules[module_name] = module


class TestPackageInit:
    """Tests for package initialization functionality."""
    
    def test_version_attribute(self):
        """Test that __version__ attribute exists."""
        import securepass
        assert hasattr(securepass, '__version__')
        assert isinstance(securepass.__version__, str)
    
    def test_author_attribute(self):
        """Test that __author__ attribute exists."""
        import securepass
        assert hasattr(securepass, '__author__')
        assert isinstance(securepass.__author__, str)
    
    def test_passwordgenerator_import(self):
        """Test that PasswordGenerator is importable from the package root."""
        import securepass
        assert hasattr(securepass, 'PasswordGenerator')
        from securepass import PasswordGenerator
        assert PasswordGenerator is not None
    
    def test_clipboarddriver_import(self):
        """Test that ClipboardDriver is importable from the package root."""
        import securepass
        assert hasattr(securepass, 'ClipboardDriver')
        from securepass import ClipboardDriver
        assert ClipboardDriver is not None
    
    def test_main_function_import(self, clean_modules):
        """Test that main function is importable from the package root."""
        # Force reimport of the module
        if 'securepass' in sys.modules:
            del sys.modules['securepass']
        
        # Mock the cli module
        with patch.dict('sys.modules', {'securepass.cli': MagicMock()}):
            # Create a mock for the main function
            mock_main = MagicMock(return_value=0)
            sys.modules['securepass.cli'].main = mock_main
            
            # Import the package
            import securepass
            
            # Check that the main function is accessible
            assert hasattr(securepass, 'main')
            
            # Call the main function and check if the mock was called
            securepass.main()
            mock_main.assert_called_once()
    
    def test_compatibility_installation(self, clean_modules):
        """Test that compatibility aliases are installed on import."""
        # Clear modules
        if 'securepass' in sys.modules:
            del sys.modules['securepass']
        if 'securepass.compatibility' in sys.modules:
            del sys.modules['securepass.compatibility']
        
        # Mock the compatibility module
        mock_compat = MagicMock()
        mock_install_aliases = MagicMock()
        mock_compat.install_aliases = mock_install_aliases
        
        with patch.dict('sys.modules', {'securepass.compatibility': mock_compat}):
            # Import the package
            import securepass
            
            # Check that install_aliases was called
            mock_install_aliases.assert_called_once()
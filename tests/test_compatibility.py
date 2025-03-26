"""
Tests for the backward compatibility module.
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


class TestCompatibilityModule:
    """Tests for compatibility functionality."""
    
    def test_is_module_available_true(self):
        """Test is_module_available when module exists."""
        from securepass.compatibility import is_module_available
        
        # sys module should definitely exist
        assert is_module_available('sys') is True
    
    def test_is_module_available_false(self):
        """Test is_module_available when module doesn't exist."""
        from securepass.compatibility import is_module_available
        
        # This module should not exist
        assert is_module_available('definitely_not_a_real_module_name') is False
    
    def test_install_aliases_with_no_existing_module(self, clean_modules):
        """Test installing aliases when original module doesn't exist."""
        # Make sure password_generator isn't in sys.modules
        if 'password_generator' in sys.modules:
            del sys.modules['password_generator']
        
        # Mock the module finding to always return None for password_generator
        with patch('importlib.util.find_spec', lambda name: None if name == 'password_generator' else MagicMock()):
            # Import the compat module and trigger the install
            from securepass.compatibility import install_aliases
            install_aliases()
            
            # Check if aliases were created
            assert 'password_generator' in sys.modules
            assert sys.modules['password_generator'] == sys.modules['securepass']
    
    def test_install_aliases_with_existing_module(self, clean_modules):
        """Test installing aliases when original module exists."""
        # Create a dummy password_generator module
        sys.modules['password_generator'] = MagicMock()
        
        # Mock the module finding to return a spec for password_generator
        with patch('importlib.util.find_spec', return_value=MagicMock()):
            # Import the compat module and trigger the install
            from securepass.compatibility import install_aliases
            install_aliases()
            
            # Check that the existing module wasn't replaced
            assert 'password_generator' in sys.modules
            assert sys.modules['password_generator'] != sys.modules.get('securepass', None)
    
    def test_deprecated_password_generator_class(self, clean_modules):
        """Test the deprecated PasswordGenerator compatibility class."""
        # Make sure password_generator isn't in sys.modules
        if 'password_generator' in sys.modules:
            del sys.modules['password_generator']
        
        # Mock out necessary components
        with patch('importlib.util.find_spec', lambda name: None if name == 'password_generator' else MagicMock()):
            # Mock the real PasswordGenerator
            mock_generator = MagicMock()
            with patch('securepass.generator.PasswordGenerator', mock_generator):
                # Import and install aliases
                from securepass.compatibility import install_aliases
                install_aliases()
                
                # Now try to use the deprecated class
                with warnings.catch_warnings(record=True) as recorded_warnings:
                    # Make sure warnings are always triggered
                    warnings.simplefilter('always')
                    
                    # Try to instantiate the deprecated class
                    password_generator = sys.modules['password_generator'].PasswordGenerator()
                    
                    # Verify a deprecation warning was issued
                    assert len(recorded_warnings) > 0
                    assert issubclass(recorded_warnings[0].category, DeprecationWarning)
                    assert "deprecated" in str(recorded_warnings[0].message)
                    
                    # Verify the real generator was called
                    mock_generator.assert_called_once()
    
    def test_submodule_aliasing(self, clean_modules):
        """Test the aliasing of submodules."""
        # Make sure password_generator isn't in sys.modules
        if 'password_generator' in sys.modules:
            del sys.modules['password_generator']
        
        # Mock out necessary components
        with patch('importlib.util.find_spec', lambda name: None if name == 'password_generator' else MagicMock()):
            # Set up our securepass modules
            sys.modules['securepass'] = MagicMock()
            sys.modules['securepass.cli'] = MagicMock()
            sys.modules['securepass.generator'] = MagicMock()
            
            # Import and install aliases
            from securepass.compatibility import install_aliases
            install_aliases()
            
            # Check if submodule aliases were created
            assert 'password_generator.cli' in sys.modules
            assert 'password_generator.generator' in sys.modules
            assert sys.modules['password_generator.cli'] == sys.modules['securepass.cli']
            assert sys.modules['password_generator.generator'] == sys.modules['securepass.generator']
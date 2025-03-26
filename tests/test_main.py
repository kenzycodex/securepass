"""
Tests for the __main__ module execution entry point.

These tests ensure that the __main__ module correctly serves as an 
entry point for direct module execution.
"""

import pytest
import sys
import os
from unittest.mock import patch


def test_main_module_execution():
    """Test that __main__.py properly calls main function."""
    with patch('securepass.cli.main', return_value=42) as mock_main:
        with patch('sys.exit') as mock_exit:
            # Get the path to the __main__.py file
            main_file = os.path.join(
                os.path.dirname(os.path.dirname(__file__)),
                'securepass',
                '__main__.py'
            )
            
            # Create a namespace for execution
            namespace = {'__name__': '__main__'}
            
            # Read the file contents
            with open(main_file, 'r') as f:
                content = f.read()
            
            # Execute the file contents in this namespace
            exec(content, namespace)
            
            # Verify main was called
            mock_main.assert_called_once()
            
            # Verify exit was called with correct return value
            mock_exit.assert_called_once_with(42)
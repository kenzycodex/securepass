import pytest
import string
import random
from unittest.mock import patch, MagicMock
from securepass.generator import PasswordGenerator


def test_password_length():
    """Test password length is as specified."""
    password = PasswordGenerator.generate_password(20)
    assert len(password) == 20


def test_charset_selection():
    """Test charset selection works correctly."""
    # Alphanumeric charset
    alnum = PasswordGenerator.generate_password(20, "alnum")
    assert alnum.isalnum()
    
    # Letters only charset
    letters = PasswordGenerator.generate_password(20, "letters")
    assert all(c.isalpha() for c in letters)
    
    # Digits only charset
    digits = PasswordGenerator.generate_password(20, "digits")
    assert all(c.isdigit() for c in digits)


def test_invalid_charset():
    """Test invalid charset raises ValueError."""
    with pytest.raises(ValueError, match="Invalid charset"):
        PasswordGenerator.generate_password(10, "invalid")


def test_invalid_length():
    """Test invalid length raises ValueError."""
    # Test too short length
    with pytest.raises(ValueError, match="Invalid password length"):
        PasswordGenerator.generate_password(0)
    
    # Test too long length
    with pytest.raises(ValueError, match="Invalid password length"):
        PasswordGenerator.generate_password(129)


def test_empty_charset():
    """Test empty charset raises ValueError."""
    # Mock the charsets dict to simulate empty charset
    original_charsets = PasswordGenerator.charsets
    try:
        PasswordGenerator.charsets = {"empty": ""}
        with pytest.raises(ValueError, match="Selected charset is empty"):
            PasswordGenerator.generate_password(10, "empty")
    finally:
        PasswordGenerator.charsets = original_charsets


def test_password_generation():
    """Test password generation includes required character types."""
    password = PasswordGenerator.generate_password(20)
    assert len(password) == 20
    assert any(c.isupper() for c in password)
    assert any(c.islower() for c in password)
    assert any(c.isdigit() for c in password)
    assert any(c in string.punctuation for c in password)


def test_system_random_failure():
    """Test exception handling for SystemRandom failure."""
    # Create a custom mock class to replace SystemRandom
    mock_random = MagicMock()
    mock_random.return_value.choice.side_effect = Exception("Test error")
    
    with patch('random.SystemRandom', mock_random):
        with pytest.raises(RuntimeError, match="Failed to generate password"):
            PasswordGenerator.generate_password(10)


def test_min_length_guarantees():
    """Test that even minimal length passwords meet requirements."""
    # Test with minimal length = 8
    password = PasswordGenerator.generate_password(8)
    assert len(password) == 8
    
    # Test guarantee of all character types for full charset
    # (This might be implementation-specific based on how you handle short passwords)
    if PasswordGenerator.charsets["full"] == string.ascii_letters + string.digits + string.punctuation:
        assert any(c.isupper() for c in password)
        assert any(c.islower() for c in password)
        assert any(c.isdigit() for c in password)
import random
import string
from typing import Literal


class PasswordGenerator:
    # Add charsets as a class attribute
    charsets = {
        "full": string.ascii_letters + string.digits + string.punctuation,
        "alnum": string.ascii_letters + string.digits,
        "letters": string.ascii_letters,
        "digits": string.digits,
    }

    @staticmethod
    def generate_password(
        length: int = 20,
        charset: Literal["full", "alnum", "letters", "digits"] = "full",
    ) -> str:
        """Generate a secure random password.
        
        Args:
            length: Length of the password (8-128 characters)
            charset: Character set to use
            
        Returns:
            Generated password string
            
        Raises:
            ValueError: If invalid charset is provided or length is out of range
        """
        # Add explicit length validation
        if length < 8 or length > 128:
            raise ValueError(f"Invalid password length. Must be between 8 and 128 characters. Got {length}")

        if charset not in PasswordGenerator.charsets:
            raise ValueError(f"Invalid charset: {charset}")

        characters = PasswordGenerator.charsets[charset]
        
        if not characters:
            raise ValueError("Selected charset is empty")

        try:
            secure_random = random.SystemRandom()
            
            # For "full" charset, ensure at least one of each character type if length is sufficient
            if charset == "full" and length >= 4:
                # Generate base password with guaranteed character types
                password = [
                    secure_random.choice(string.ascii_uppercase),  # One uppercase
                    secure_random.choice(string.ascii_lowercase),  # One lowercase
                    secure_random.choice(string.digits),          # One digit
                    secure_random.choice(string.punctuation)      # One special char
                ]
                
                # Fill the rest randomly
                password.extend(secure_random.choice(characters) for _ in range(length - 4))
                
                # Shuffle to avoid predictable pattern
                secure_random.shuffle(password)
                return ''.join(password)
            else:
                # Standard random generation for other charsets
                return "".join(secure_random.choice(characters) for _ in range(length))
                
        except Exception as e:
            raise RuntimeError(f"Failed to generate password: {str(e)}")
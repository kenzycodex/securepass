import random
import string
from typing import Literal


class PasswordGenerator:
    @staticmethod
    def generate_password(
        length: int = 20,
        charset: Literal["full", "alnum", "letters", "digits"] = "full",
    ) -> str:
        """Generate a secure random password.
        
        Args:
            length: Length of the password
            charset: Character set to use
            
        Returns:
            Generated password string
            
        Raises:
            ValueError: If invalid charset is provided
        """
        charsets = {
            "full": string.ascii_letters + string.digits + string.punctuation,
            "alnum": string.ascii_letters + string.digits,
            "letters": string.ascii_letters,
            "digits": string.digits,
        }

        if charset not in charsets:
            raise ValueError(f"Invalid charset: {charset}")

        characters = charsets[charset]
        
        if not characters:
            raise ValueError("Selected charset is empty")

        try:
            return "".join(random.SystemRandom().choice(characters) for _ in range(length))
        except Exception as e:
            raise RuntimeError(f"Failed to generate password: {str(e)}")
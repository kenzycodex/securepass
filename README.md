# SecurePass

A secure, cross-platform password generator with clipboard integration.

![Python Versions](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Test Coverage](https://img.shields.io/badge/coverage-71%25-yellow)

## Features

- Generate secure random passwords with customizable parameters
- Cross-platform clipboard integration (Windows, macOS, Linux)
- Multiple clipboard backend support (PowerShell, pbcopy, xclip, wl-copy, CopyQ, pyperclip)
- Command-line interface for quick password generation
- Comprehensive test suite with platform-specific tests
- Backward compatibility with previous `password_generator` package

## Installation

```bash
# Install from PyPI
pip install securepass

# Or install from source
git clone https://github.com/yourusername/securepass.git
cd securepass
pip install -e .
```

## Usage

### Command Line

```bash
# Generate a 16-character alphanumeric password
passgen -l 16 -c alnum

# Generate a password with all character types and copy to clipboard
passgen -l 20 -c all --copy

# Generate a password with verbose output
passgen -l 12 -c special -v
```

### Python API

```python
from securepass import PasswordGenerator, ClipboardDriver

# Create a password generator
generator = PasswordGenerator()

# Generate a secure password
password = generator.generate(length=16, char_types="alnum")
print(f"Generated password: {password}")

# Copy password to clipboard
ClipboardDriver.copy_password(password, secure=True)
```

## Configuration

The following character types are supported:

- `alpha`: Lowercase and uppercase letters
- `alnum`: Letters and numbers
- `digit`: Numbers only
- `lower`: Lowercase letters only
- `upper`: Uppercase letters only
- `special`: Special characters only
- `all`: All character types

## Clipboard Support

SecurePass provides cross-platform clipboard support with multiple backends:

| Platform | Supported Backends |
|----------|-------------------|
| Windows  | PowerShell, pyperclip, CopyQ |
| macOS    | pbcopy, pyperclip, CopyQ |
| Linux    | xclip, wl-copy, pyperclip, CopyQ |

The clipboard system automatically tries different methods until it finds one that works on your system.

## Development

### Setting up the development environment

```bash
# Clone the repository
git clone https://github.com/yourusername/securepass.git
cd securepass

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .

# Install development dependencies
pip install pytest pytest-cov pytest-mock
```

### Running tests

The project includes a comprehensive test suite with platform-specific tests:

```bash
# Run all tests appropriate for your platform
python run_tests.py

# Run tests with coverage report
python run_tests.py --coverage

# Run specific test modules
python run_tests.py --module clipboard,generator
```

### Refreshing the package installation

If you encounter issues with the package installation or entry points, you can use the refresh script:

```bash
python refresh_package.py
```

## Compatibility

SecurePass provides backward compatibility with the previous `password_generator` package. Old import statements and class names should continue to work but will raise deprecation warnings:

```python
# Old import (will work but shows deprecation warning)
from password_generator import PasswordGenerator

# New import (recommended)
from securepass import PasswordGenerator
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create a feature branch
3. Add your changes
4. Run tests to ensure they pass
5. Submit a pull request

## Acknowledgments

- Thanks to all the contributors who have helped improve this project.
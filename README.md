# 🔒 SecurePass - Advanced Password Generator

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Tests](https://img.shields.io/github/actions/workflow/status/kenzycodex/securepass/tests.yml?label=tests)
![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)

A secure, cross-platform password generator with clipboard integration and advanced features.

## ✨ Features

- 🔐 Generate cryptographically secure passwords using `random.SystemRandom()`
- 📋 Automatic clipboard copying with multiple fallback methods
- 🖥️ Cross-platform support (Windows, macOS, Linux)
- ⚙️ Multiple character sets:
  - `full`: Letters, numbers, and symbols (default)
  - `alnum`: Only letters and numbers
  - `letters`: Only letters
  - `digits`: Only numbers
- 📏 Customizable password length (8-128 characters)
- 🔍 Verbose mode for debugging
- 🚫 Exclude similar characters (e.g., 1, l, I)
- 🛡️ No password history or logging

## 📦 Installation

```bash
pip install securepass
```

For development:
```bash
git clone https://github.com/kenzycodex/securepass.git
cd securepass
pip install -e ".[dev]"
```

## 🚀 Usage

### Command Line
```bash
passgen --length 20 --charset full -v
```

### Python API
```python
from securepass import PasswordGenerator

# Generate password
password = PasswordGenerator.generate(
    length=16,
    charset="full",
    exclude_similar=True
)
```

## 🛠️ Development

### Running Tests
```bash
pytest tests/ --cov=securepass --cov-report=term-missing
```

### Code Formatting
```bash
black .
flake8
mypy .
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m "Add amazing feature"`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📜 License

MIT - See [LICENSE](LICENSE) for details.

## Future Feature Ideas

1. **Password Strength Meter**:
   - Implement zxcvbn or similar algorithm
   - Add entropy calculation

2. **Password History**:
   - Optional encrypted local storage
   - Temporary memory-only history

3. **Advanced Options**:
   ```python
   PasswordGenerator.generate(
       length=16,
       min_uppercase=2,
       min_digits=2,
       min_special=1,
       exclude_chars="l1O0"
   )
   ```

4. **GUI Version**:
   - Tkinter simple interface
   - PyQt advanced interface

5. **Browser Extension**:
   - Generate passwords directly in browser
   - Auto-fill forms

6. **API Server**:
   - REST endpoint for password generation
   - Rate limiting and authentication

7. **Password Analysis**:
   - Check against haveibeenpwned API
   - Similarity checker for existing passwords
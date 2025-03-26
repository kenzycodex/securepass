"""SecurePass setup script."""

from setuptools import setup, find_packages

setup(
    name="securepass",
    version="1.0.0",
    description="A secure, cross-platform password generator with clipboard integration",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Kenzy Codex",
    author_email="kenzycodex@example.com",
    license="MIT",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'passgen=securepass.cli:main',
        ],
    },
    python_requires=">=3.8",
    install_requires=[
        "click>=8.0.0",
        "pyperclip>=1.8.0",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Security",
        "Topic :: Utilities",
    ],
    keywords=["password", "generator", "security", "cryptography", "clipboard"],
    zip_safe=False,  # This helps with development mode
)
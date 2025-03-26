"""
Script to refresh the package installation and fix entry points.
"""

import subprocess
import sys
import os
import shutil

def main():
    """Refresh the package installation."""
    print("Refreshing package installation...")
    
    # Uninstall existing packages
    subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y", "securepass"], 
                   capture_output=True)
    subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y", "strong-password-generator"], 
                  capture_output=True)
    
    # Install in development mode
    subprocess.run([sys.executable, "-m", "pip", "install", "-e", "."], check=True)
    
    # Validate installation
    result = subprocess.run([sys.executable, "-m", "pip", "show", "securepass"], 
                           capture_output=True, text=True)
    print(result.stdout)
    
    # Check if entry point was created correctly
    scripts_dir = os.path.join(os.path.dirname(sys.executable), 'Scripts')
    passgen_exe = os.path.join(scripts_dir, 'passgen.exe')
    
    if os.path.exists(passgen_exe):
        print(f"Entry point created successfully at: {passgen_exe}")
    else:
        print(f"Entry point not found at: {passgen_exe}")
        
        # Create manual entry point
        if sys.platform == 'win32':
            create_windows_entry_point(scripts_dir)
        else:
            create_unix_entry_point(scripts_dir)
    
    print("\nTry running: passgen -l 16 -c alnum -v")
    print("Or: python -m securepass.cli -l 16 -c alnum -v")

def create_windows_entry_point(scripts_dir):
    """Create a manual entry point script for Windows."""
    print("Creating manual entry point for Windows...")
    
    # Ensure the directory exists
    os.makedirs(scripts_dir, exist_ok=True)
    
    # Create a .py file
    py_script = os.path.join(scripts_dir, 'passgen.py')
    with open(py_script, 'w') as f:
        f.write("""#!/usr/bin/env python
# Generated manually by refresh_package.py
import sys
from securepass.cli import main
if __name__ == '__main__':
    sys.exit(main())
""")
    
    # Create a .bat file
    bat_script = os.path.join(scripts_dir, 'passgen.bat')
    with open(bat_script, 'w') as f:
        f.write(f"""@echo off
"{sys.executable}" "{py_script}" %*
""")
    
    print(f"Created entry point scripts at:")
    print(f"  - {py_script}")
    print(f"  - {bat_script}")

def create_unix_entry_point(scripts_dir):
    """Create a manual entry point script for Unix-like systems."""
    print("Creating manual entry point for Unix...")
    
    # Ensure the directory exists
    os.makedirs(scripts_dir, exist_ok=True)
    
    script_path = os.path.join(scripts_dir, 'passgen')
    with open(script_path, 'w') as f:
        f.write(f"""#!/usr/bin/env python
# Generated manually by refresh_package.py
import sys
from securepass.cli import main
if __name__ == '__main__':
    sys.exit(main())
""")
    
    # Make executable
    os.chmod(script_path, 0o755)
    print(f"Created entry point script at: {script_path}")

if __name__ == "__main__":
    main()
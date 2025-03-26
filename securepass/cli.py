#!/usr/bin/env python3
"""
Secure Password Generator CLI Tool

Generates cryptographically secure passwords and copies them to clipboard.
"""

import click
import sys
from typing import Optional

from securepass.generator import PasswordGenerator
from securepass.clipboard import ClipboardDriver
from securepass.utils.vprint import vprint

@click.command()
@click.option('-l', '--length', default=20, type=click.IntRange(8, 128), help='Password length (8-128 characters)')
@click.option('-c', '--charset', 
              type=click.Choice(['full', 'alnum', 'letters', 'digits', 'special', 'all']), 
              default='full', 
              help='Character set to use')
@click.option('-v', '--verbose', is_flag=True, help='Enable verbose output')
@click.option('--copy/--no-copy', default=True, help='Enable/disable clipboard copying')
def cli(length: int, charset: str, verbose: bool, copy: bool) -> str:
    """Generate secure passwords and optionally copy to clipboard."""
    try:
        # Use built-in click echo for verbose output to ensure it's captured
        if verbose:
            click.echo(f"Generating {length}-character password using {charset} charset", err=True)
        
        # Map 'special' and 'all' to 'full' for backward compatibility
        generator_charset = charset
        if charset in ['special', 'all']:
            generator_charset = 'full'
            if verbose:
                click.echo(f"Note: '{charset}' charset maps to 'full' charset", err=True)
        
        password = PasswordGenerator.generate_password(length, generator_charset)
        
        if copy:
            try:
                ClipboardDriver.copy_password(password, verbose)
                if verbose:
                    click.echo("Password copied to clipboard successfully", err=True)
            except RuntimeError as e:
                if verbose:
                    click.echo(f"Clipboard error: {str(e)}", err=True)
                print("Password was generated but not copied to clipboard", file=sys.stderr)
        
        # Output the password
        click.echo(f"Generated {length}-character password using {charset} charset")
        click.echo(f"Generated Password: {password}")
        return password
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

def main() -> int:
    """Main entry point for the CLI tool."""
    try:
        cli()
        return 0
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return 1

def parse_args(args: Optional[list[str]] = None) -> click.Context:
    """Parse command line arguments (for compatibility with existing tests)."""
    from click.testing import CliRunner
    runner = CliRunner()
    result = runner.invoke(cli, args=args)
    return result

if __name__ == "__main__":
    sys.exit(main())
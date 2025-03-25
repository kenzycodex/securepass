import argparse
import sys
from password_generator.generator import PasswordGenerator
from password_generator.clipboard import ClipboardDriver


def main():
    parser = argparse.ArgumentParser(
        description="Generate strong passwords and copy to clipboard",
        prog="passgen"  # Added program name
    )

    parser.add_argument(
        "-l", "--length",
        type=int,
        default=20,
        help="Length of password (default: 20)",
    )
    parser.add_argument(
        "-c", "--charset",
        choices=["full", "alnum", "letters", "digits"],
        default="full",
        help="Character set (default: full)",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    parser.add_argument(
        "--no-copy",
        action="store_true",
        help="Don't copy password to clipboard",
    )

    args = parser.parse_args()

    try:
        password = PasswordGenerator.generate_password(args.length, args.charset)
        print(f"Generated Password: {password}")

        if not args.no_copy:
            ClipboardDriver.copy_password(password, args.verbose)
            print("Password copied to clipboard.")
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
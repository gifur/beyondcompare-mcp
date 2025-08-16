#!/usr/bin/env python3
"""
HelloWorld30 CLI - Command Line Interface
Greeting service supporting 30 languages
"""

import json
import argparse
import sys
from pathlib import Path
from typing import Optional, Dict, Any


class HelloWorld30CLI:
    """Command line interface for HelloWorld30 greeting service."""

    def __init__(self):
        """Initialize CLI with language data."""
        self.languages_file = Path(__file__).parent / "languages.json"
        self.languages = self._load_languages()

    def _load_languages(self) -> Dict[str, Any]:
        """Load language data from JSON file."""
        try:
            with open(self.languages_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('languages', {})
        except FileNotFoundError:
            print(f"Error: Language file not found: {self.languages_file}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in language file: {e}")
            sys.exit(1)

    def get_greeting(self, language: str, name: Optional[str] = None) -> str:
        """Get greeting in specified language.

        Args:
            language: Language name or code
            name: Optional name to include in greeting

        Returns:
            Formatted greeting string
        """
        # Normalize language input
        lang_key = language.lower()

        # Try to find language by name or code
        lang_data = None
        for key, data in self.languages.items():
            if (key == lang_key or
                data.get('code', '').lower() == lang_key or
                data.get('name', '').lower() == lang_key):
                lang_data = data
                break

        if not lang_data:
            available = list(self.languages.keys())
            raise ValueError(f"Language '{language}' not supported. Available: {available}")

        greeting = lang_data['hello']

        if name:
            return f"{greeting}, {name}!"
        else:
            return f"{greeting}, World!"

    def list_languages(self) -> None:
        """Display all available languages."""
        print("Available languages:")
        print("-" * 50)

        for key, data in sorted(self.languages.items()):
            code = data.get('code', '??')
            name = data.get('name', key.title())
            hello = data.get('hello', '???')
            print(f"{name:<15} ({code:>2}) - {hello}")

        print(f"\nTotal: {len(self.languages)} languages supported")

    def interactive_mode(self) -> None:
        """Run interactive greeting mode."""
        print("🌍 HelloWorld30 Interactive Mode")
        print("Type 'quit' to exit, 'list' to show languages")
        print("-" * 40)

        while True:
            try:
                user_input = input("\nEnter language and name (e.g., 'spanish Sandra'): ").strip()

                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("Goodbye! 👋")
                    break

                if user_input.lower() in ['list', 'languages', 'l']:
                    self.list_languages()
                    continue

                if not user_input:
                    continue

                parts = user_input.split(' ', 1)
                language = parts[0]
                name = parts[1] if len(parts) > 1 else None

                greeting = self.get_greeting(language, name)
                print(f"✨ {greeting}")

            except ValueError as e:
                print(f"❌ Error: {e}")
            except KeyboardInterrupt:
                print("\n\nGoodbye! 👋")
                break
            except EOFError:
                print("\n\nGoodbye! 👋")
                break


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="HelloWorld30 - Greetings in 30 languages",
        epilog="Examples:\n"
               "  %(prog)s --lang spanish --name Sandra\n"
               "  %(prog)s -l ja -n Claude\n"
               "  %(prog)s --list\n"
               "  %(prog)s --interactive",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '-l', '--lang', '--language',
        help='Language for greeting (name or code)'
    )

    parser.add_argument(
        '-n', '--name',
        help='Name to include in greeting (default: World)'
    )

    parser.add_argument(
        '--list', '--languages',
        action='store_true',
        help='List all available languages'
    )

    parser.add_argument(
        '-i', '--interactive',
        action='store_true',
        help='Start interactive mode'
    )

    parser.add_argument(
        '--version',
        action='version',
        version='HelloWorld30 CLI v1.0.0'
    )

    args = parser.parse_args()

    # Initialize CLI
    cli = HelloWorld30CLI()

    try:
        # Handle different modes
        if args.list:
            cli.list_languages()
        elif args.interactive:
            cli.interactive_mode()
        elif args.lang:
            greeting = cli.get_greeting(args.lang, args.name)
            print(greeting)
        else:
            # Default: show help and interactive prompt
            parser.print_help()
            print("\n" + "="*50)
            response = input("Start interactive mode? (y/N): ")
            if response.lower() in ['y', 'yes']:
                cli.interactive_mode()

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()

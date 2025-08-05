# Contributing to Beyond Compare MCP

Thank you for your interest in contributing to the Beyond Compare MCP project! We welcome contributions from the community to help improve this project.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally
   ```bash
   git clone https://github.com/yourusername/beyondcompare-mcp.git
   cd beyondcompare-mcp
   ```
3. **Set up the development environment**
   ```bash
   # Create a virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install development dependencies
   pip install -e ".[dev]"
   ```

## Development Workflow

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow the code style (see below)
   - Write tests for new features
   - Update documentation as needed

3. **Run tests**
   ```bash
   # Run all tests
   pytest
   
   # Run with coverage
   pytest --cov=beyondcompare_mcp
   ```

4. **Format and lint your code**
   ```bash
   # Auto-format code
   black .
   isort .
   
   # Check for type errors
   mypy beyondcompare_mcp
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "Your detailed description of changes"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request** on GitHub

## Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) for Python code
- Use [Black](https://black.readthedocs.io/) for code formatting
- Use [isort](https://pycqa.github.io/isort/) for import sorting
- Use [Google-style docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
- Keep lines under 88 characters (Black's default)

## Testing

- Write tests for all new functionality
- Ensure all tests pass before submitting a PR
- Use descriptive test method names (e.g., `test_compare_files_identical`)
- Mock external dependencies in unit tests

## Documentation

- Update the README.md for significant changes
- Add docstrings for all public functions and classes
- Document any new environment variables
- Update the CHANGELOG.md for user-facing changes

## Reporting Issues

When reporting issues, please include:

1. Steps to reproduce the issue
2. Expected behavior
3. Actual behavior
4. Environment details (OS, Python version, Beyond Compare version)
5. Any relevant error messages or logs

## Code of Conduct

This project adheres to the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).

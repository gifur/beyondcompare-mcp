# Security Policy

## Supported Versions

We provide security updates for the following versions of Beyond Compare MCP:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security vulnerability, please report it responsibly.

### How to Report

1. **DO NOT** create a public GitHub issue for security vulnerabilities
2. Email security reports to: [your-email@domain.com]
3. Include the following information:
   - Description of the vulnerability
   - Steps to reproduce the issue
   - Potential impact assessment
   - Suggested fix (if available)

### What to Expect

- **Acknowledgment**: We will acknowledge receipt within 48 hours
- **Initial Assessment**: We will provide an initial assessment within 5 business days
- **Resolution Timeline**: Critical vulnerabilities will be addressed within 30 days
- **Disclosure**: We follow responsible disclosure practices

### Security Considerations

#### Beyond Compare Integration
- The MCP server executes Beyond Compare as an external process
- File paths are validated to prevent directory traversal attacks
- Temporary script files are created in secure directories with appropriate permissions

#### Data Handling
- No user data is permanently stored by the MCP server
- Temporary files are cleaned up after operations
- File comparisons are performed locally on the user's machine

#### Network Security
- The MCP server operates via stdio protocol (no network exposure)
- All communication is through Claude Desktop's secure MCP protocol
- No external network requests are made during normal operation

#### File System Access
- The server only accesses files explicitly specified by the user
- Beyond Compare executable path is validated before execution
- Script directory permissions are restricted to the current user

### Security Best Practices for Users

1. **Beyond Compare Installation**: Ensure Beyond Compare is installed from official sources
2. **File Permissions**: Review file permissions before running comparisons
3. **Script Directory**: Use a dedicated directory for temporary scripts
4. **Regular Updates**: Keep Beyond Compare and the MCP server updated

### Known Security Considerations

- The MCP server requires file system access to function properly
- Beyond Compare executable must be trusted as it processes user files
- Temporary script files may contain file paths (cleaned up automatically)

### Changelog of Security Updates

- **v0.1.0**: Initial release with basic security measures
  - Input validation for file paths
  - Secure temporary file handling
  - Process isolation for Beyond Compare execution

---

For general questions about security practices, please refer to our [Contributing Guidelines](CONTRIBUTING.md) or create a public issue for non-sensitive security discussions.

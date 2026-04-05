# HelloWorld30 🌍

A professional greeting service supporting 30 languages - perfect for testing MCP server development pipelines.

## Overview

HelloWorld30 is a simple yet comprehensive application that provides greeting services in 30 different languages. It features both CLI and REST API interfaces, making it an ideal target for testing MCP (Model Context Protocol) server wrapper development.

## Features

### 🌐 Language Support
- **30 Languages**: English, Spanish, French, German, Italian, Portuguese, Russian, Japanese, Chinese, Korean, Arabic, Hindi, Dutch, Swedish, Norwegian, Danish, Finnish, Polish, Czech, Hungarian, Greek, Turkish, Hebrew, Thai, Vietnamese, Indonesian, Malay, Swahili, Romanian, Ukrainian
- **Multiple Access Methods**: Language name, language code, or native script
- **Personalized Greetings**: Include names in greetings

### 🖥️ CLI Interface
- Interactive and non-interactive modes
- Language listing and discovery
- Flexible input parsing
- Professional error handling

### 🌐 REST API
- FastAPI-based modern API
- OpenAPI documentation (Swagger UI)
- Multiple endpoint formats
- JSON request/response
- Health monitoring

## Installation

```bash
# Clone or download the HelloWorld30 directory
cd HelloWorld30

# Install dependencies
pip install -r requirements.txt
```

## Usage

### CLI Interface

```bash
# Basic greeting
python cli.py --lang spanish --name Sandra
# Output: Hola, Sandra!

# Using language codes
python cli.py -l ja -n Claude
# Output: こんにちは, Claude!

# List all languages
python cli.py --list

# Interactive mode
python cli.py --interactive
```

### REST API Server

```bash
# Start the server
python server.py

# Server runs on http://localhost:8000
```

#### API Endpoints

```bash
# Get greeting via query parameters
curl "http://localhost:8000/hello?lang=french&name=Claude"

# Get greeting via JSON POST
curl -X POST "http://localhost:8000/hello" \
     -H "Content-Type: application/json" \
     -d '{"language": "japanese", "name": "Sandra"}'

# List all languages
curl "http://localhost:8000/languages"

# Get specific language info
curl "http://localhost:8000/languages/spanish"

# Health check
curl "http://localhost:8000/health"
```

#### API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Examples

### Response Format

```json
{
  "greeting": "Bonjour, Claude!",
  "language": "French",
  "language_code": "fr",
  "name": "Claude"
}
```

### Language List

```json
{
  "total": 30,
  "languages": [
    {
      "code": "en",
      "name": "English",
      "hello": "Hello"
    },
    {
      "code": "es",
      "name": "Spanish",
      "hello": "Hola"
    }
  ]
}
```

## Language Support

| Language | Code | Native Greeting |
|----------|------|----------------|
| English | en | Hello |
| Spanish | es | Hola |
| French | fr | Bonjour |
| German | de | Hallo |
| Italian | it | Ciao |
| Portuguese | pt | Olá |
| Russian | ru | Привет |
| Japanese | ja | こんにちは |
| Chinese | zh | 你好 |
| Korean | ko | 안녕하세요 |
| Arabic | ar | مرحبا |
| Hindi | hi | नमस्ते |
| Dutch | nl | Hallo |
| Swedish | sv | Hej |
| Norwegian | no | Hei |
| Danish | da | Hej |
| Finnish | fi | Hei |
| Polish | pl | Cześć |
| Czech | cs | Ahoj |
| Hungarian | hu | Szia |
| Greek | el | Γεια σου |
| Turkish | tr | Merhaba |
| Hebrew | he | שלום |
| Thai | th | สวัสดี |
| Vietnamese | vi | Xin chào |
| Indonesian | id | Halo |
| Malay | ms | Hello |
| Swahili | sw | Hujambo |
| Romanian | ro | Salut |
| Ukrainian | uk | Привіт |

## Testing

```bash
# Run basic functionality test
python cli.py --lang english --name Test
# Expected: Hello, Test!

# Test API server
python server.py &
curl "http://localhost:8000/hello?lang=spanish&name=API"
# Expected: {"greeting": "Hola, API!", ...}
```

## Error Handling

The application provides comprehensive error handling:

- **Invalid Language**: Clear error message with available options
- **Missing Files**: Graceful failure with helpful messages
- **API Errors**: HTTP status codes with detailed error responses
- **CLI Errors**: User-friendly error messages and exit codes

## Development

### Project Structure
```
HelloWorld30/
├── cli.py              # Command-line interface
├── server.py           # REST API server
├── languages.json      # Language data (30 languages)
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

### Adding New Languages

Edit `languages.json` and add new language entries:

```json
{
  "newlanguage": {
    "code": "xx",
    "name": "New Language",
    "hello": "Native Greeting"
  }
}
```

## Use Cases

### Perfect for MCP Server Testing
HelloWorld30 serves as an ideal target application for testing MCP server development pipelines:

- **Simple but realistic API surface**
- **Multiple interaction patterns** (CLI + REST)
- **Professional structure** like real applications
- **Comprehensive error handling**
- **Well-documented endpoints**
- **Easy to understand and verify**

### MCP Server Wrapper Potential
A HelloWorld30 MCP server could provide tools like:
- `get_greeting(language, name)` - Generate personalized greeting
- `list_languages()` - Get all supported languages
- `get_language_info(language)` - Language details
- `translate_greeting(from_lang, to_lang, name)` - Convert greetings

## Technical Specifications

- **Python**: 3.8+ compatible
- **Framework**: FastAPI for REST API
- **CLI**: Native argparse with rich features
- **Data**: JSON-based language storage
- **Encoding**: Full UTF-8 support for international characters
- **API**: OpenAPI 3.0 compliant
- **Error Handling**: HTTP status codes and descriptive messages

## Version

- **Current Version**: 1.0.0
- **Created**: August 2025
- **Authors**: Sandra & Claude
- **Purpose**: MCP server development pipeline testing

## License

MIT License - Feel free to use this for testing, learning, and development purposes.

---

**Perfect for testing your MCP server development pipeline!** 🚀

Ready to wrap this app with a professional MCP server? Let's test that industrial development process!

# Develop Copilit

A lightweight development copilot assistant that provides code completion, analysis, and template generation capabilities through a RESTful API.

## Features

- **Code Completion**: Get intelligent code completion suggestions based on context
- **Code Analysis**: Analyze code for patterns, issues, and complexity
- **Template Generation**: Generate code templates for functions, classes, and common patterns
- **Multi-language Support**: Currently supports Python and JavaScript
- **RESTful API**: Easy-to-use HTTP API endpoints

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/23rf46yh23/develop_copilit.git
cd develop_copilit
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Create and configure environment variables:
```bash
cp .env.example .env
# Edit .env with your preferred settings
```

## Usage

### Starting the Server

Run the application:
```bash
python run.py
```

Or using the module:
```bash
python -m src.app
```

The server will start on `http://0.0.0.0:5000` by default.

### API Endpoints

#### Health Check
```bash
GET /health
```

Returns the health status of the service.

**Response:**
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "service": "develop_copilit"
}
```

#### API Information
```bash
GET /api/v1/info
```

Returns API version and available features.

#### Code Completion
```bash
POST /api/v1/complete
Content-Type: application/json

{
  "code": "def hello",
  "language": "python",
  "cursor_position": 10
}
```

**Response:**
```json
{
  "completions": [
    {"text": "def", "type": "keyword", "description": "python keyword"},
    ...
  ],
  "suggestions": ["    pass"]
}
```

#### Code Analysis
```bash
POST /api/v1/analyze
Content-Type: application/json

{
  "code": "def hello():\n    print('world')",
  "language": "python"
}
```

**Response:**
```json
{
  "analysis": {
    "language": "python",
    "lines": 2,
    "functions": ["hello"],
    "classes": [],
    "imports": [],
    "issues": []
  },
  "refactoring_suggestions": []
}
```

#### Template Generation
```bash
POST /api/v1/template
Content-Type: application/json

{
  "type": "function",
  "language": "python",
  "name": "my_function",
  "params": "x, y"
}
```

**Response:**
```json
{
  "template": "def my_function(x, y):\n    pass"
}
```

### Example Usage with curl

```bash
# Health check
curl http://localhost:5000/health

# Code completion
curl -X POST http://localhost:5000/api/v1/complete \
  -H "Content-Type: application/json" \
  -d '{"code": "def test", "language": "python"}'

# Code analysis
curl -X POST http://localhost:5000/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"code": "def hello():\n    print(\"world\")", "language": "python"}'

# Template generation
curl -X POST http://localhost:5000/api/v1/template \
  -H "Content-Type: application/json" \
  -d '{"type": "function", "language": "python", "name": "test_func", "params": "x, y"}'
```

## Development

### Running Tests

Run all tests:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=src --cov-report=html
```

Run specific test file:
```bash
pytest tests/test_app.py
```

### Project Structure

```
develop_copilit/
├── src/
│   ├── __init__.py
│   ├── app.py              # Main Flask application
│   ├── config.py           # Configuration management
│   └── copilit/
│       ├── __init__.py
│       ├── completion.py   # Code completion logic
│       └── analyzer.py     # Code analysis logic
├── tests/
│   ├── __init__.py
│   ├── test_app.py         # Application tests
│   ├── test_completion.py  # Completion tests
│   ├── test_analyzer.py    # Analyzer tests
│   └── test_config.py      # Configuration tests
├── requirements.txt        # Python dependencies
├── setup.py               # Package setup
├── pytest.ini             # Pytest configuration
├── .env.example           # Example environment variables
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

### Supported Languages

- Python
- JavaScript

More languages can be added by extending the `CodeCompleter` and `CodeAnalyzer` classes.

## Configuration

The application can be configured using environment variables or a `.env` file:

- `FLASK_ENV`: Environment (development/production/testing)
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 5000)
- `API_VERSION`: API version (default: v1)
- `LOG_LEVEL`: Logging level (default: INFO)

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the MIT License.

## Author

23rf46yh23 (jonghyunkim@g.seoultech.ac.kr)

## Acknowledgments

- Built with Flask
- Inspired by modern code completion tools
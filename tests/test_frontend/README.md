# Frontend Tests

This directory contains unit tests for the PaddleCoach frontend components.

## Test Structure

```
test_frontend/
├── test_ui_services.py    # Tests for UI service layer
├── test_app.py            # Tests for Flask application
└── README.md             # This file
```

## Running Tests

### Run All Tests

```bash
# From project root
python -m pytest tests/test_frontend/

# Or using unittest
python -m unittest discover tests/test_frontend/
```

### Run Specific Test File

```bash
python tests/test_frontend/test_ui_services.py
```

### Run with Coverage

```bash
pip install pytest-cov
pytest tests/test_frontend/ --cov=src/frontend --cov-report=html
```

## Test Categories

### UI Services Tests (`test_ui_services.py`)

Tests for backend service layer:
- **UIDataService**: Data fetching and formatting
- **StatsBot**: Natural language query processing
- **ElevenLabsClient**: TTS audio generation
- **Integration**: Cross-component interactions

### Flask App Tests (`test_app.py`)

Tests for Flask application:
- Route handling
- API endpoints
- WebSocket events
- Error handling

*Note: Flask app tests require test client setup and are marked as placeholders.*

## Test Data

Tests use mock data by default. To test with real data:
1. Ensure database is running
2. Set test environment variables
3. Run integration tests

## Writing New Tests

### Example Test Case

```python
import unittest
from src.frontend.ui_services.stats_bot import StatsBot

class TestNewFeature(unittest.TestCase):
    def setUp(self):
        self.bot = StatsBot()
    
    def test_feature(self):
        result = self.bot.some_method()
        self.assertEqual(result, expected_value)
```

### Test Naming Convention

- Test files: `test_<module>.py`
- Test classes: `Test<ClassName>`
- Test methods: `test_<feature_description>`

## Dependencies

Install test dependencies:
```bash
pip install pytest pytest-cov unittest-xml-reporting
```

## Continuous Integration

Tests are run automatically on:
- Pull requests
- Commits to main branch
- Nightly builds

## Coverage Goals

- Overall coverage: 80%+
- Critical paths: 95%+
- UI services: 85%+

## Known Issues

- Flask app tests require app instance
- ElevenLabs tests mock API calls (no API key needed)
- Some integration tests need full stack

## Future Improvements

- [ ] Add end-to-end tests with Selenium
- [ ] Implement Flask test client tests
- [ ] Add performance benchmarks
- [ ] Mock external API dependencies
- [ ] Add WebSocket testing

## Contact

For test-related questions:
- Check main project documentation
- Review test examples above
- Contact: Rakshit (Frontend Lead)

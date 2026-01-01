# Tests for LittleWorld

## Test Structure

```
tests/
  unit/                    # Unit tests (isolated components)
    test_config/
      fixtures/            # Test YAML files
      test_utils.py       # Tests for load_config()
      test_models.py       # Tests for Pydantic models
      test_env_expansion.py # Tests for env var expansion
  
  integration/            # Integration tests (multiple components)
    (integration tests to be added)
```

## Running Tests

### Install test dependencies
```bash
uv sync --extra dev
```

### Run all tests
```bash
uv run pytest
```

### Run only unit tests
```bash
uv run pytest tests/unit/
```

### Run only integration tests
```bash
uv run pytest tests/integration/
```

### Run specific test file
```bash
uv run pytest tests/unit/test_config/test_utils.py
```

### Run specific test
```bash
uv run pytest tests/unit/test_config/test_utils.py::TestLoadConfig::test_load_valid_yaml
```

### Run with coverage
```bash
uv run pytest --cov=src --cov-report=html
```

## Test Categories

### Unit Tests (`tests/unit/`)
Test individual functions/classes in isolation:
- **test_config/test_utils.py**: Tests the `load_config()` function
- **test_config/test_models.py**: Tests Pydantic model validation
- **test_config/test_env_expansion.py**: Tests environment variable expansion

### Integration Tests (`tests/integration/`)
Test multiple components working together:
- Config → World initialization
- Config → Character creation
- Full workflow tests
- (To be implemented)

## Writing New Tests

### Unit Test Example
```python
def test_something():
    # Arrange - set up test data
    test_data = {...}
    
    # Act - call the function
    result = function_under_test(test_data)
    
    # Assert - check the result
    assert result == expected_value
```

### Integration Test Example
```python
def test_config_to_world_integration():
    # Arrange - load config
    config = load_config(test_file)
    
    # Act - create world with config
    world = World(config)
    
    # Assert - verify world was created correctly
    assert world.config == config
    assert len(world.characters) > 0
```

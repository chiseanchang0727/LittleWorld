"""
Tests for environment variable expansion in config loading.
"""
import os
from pathlib import Path
import pytest
from src.config.utils import load_config


class TestEnvironmentVariableExpansion:
    """Test environment variable expansion functionality."""
    
    def test_expand_single_env_var(self, monkeypatch):
        """Test expanding a single environment variable."""
        # Arrange
        test_value = "expanded_value_123"
        monkeypatch.setenv("TEST_VAR", test_value)
        
        # Create temporary YAML file with env var
        import tempfile
        import yaml
        
        test_data = {
            "window": {"width": 800, "height": 600},
            "game": {"fps": 60},
            "characters": {
                "test_char": {
                    "name": "Test",
                    "llm": {
                        "type": "openai",
                        "version": "gpt-4o",
                        "api_key": "${TEST_VAR}"
                    }
                }
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(test_data, f)
            temp_file = Path(f.name)
        
        try:
            # Act
            config = load_config(temp_file)
            
            # Assert
            assert config.characters is not None
            char_config = config.characters["test_char"]
            assert char_config["llm"]["api_key"] == test_value
        finally:
            temp_file.unlink()
    
    def test_expand_multiple_env_vars(self, monkeypatch):
        """Test expanding multiple environment variables in one file."""
        # Arrange
        monkeypatch.setenv("API_KEY", "key123")
        monkeypatch.setenv("MODEL_VERSION", "gpt-4o")
        
        import tempfile
        import yaml
        
        test_data = {
            "window": {"width": 800},
            "characters": {
                "test": {
                    "name": "Test",
                    "llm": {
                        "type": "openai",
                        "version": "${MODEL_VERSION}",
                        "api_key": "${API_KEY}"
                    }
                }
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(test_data, f)
            temp_file = Path(f.name)
        
        try:
            # Act
            config = load_config(temp_file)
            
            # Assert
            char_config = config.characters["test"]
            assert char_config["llm"]["api_key"] == "key123"
            assert char_config["llm"]["version"] == "gpt-4o"
        finally:
            temp_file.unlink()
    
    def test_env_var_not_set_keeps_literal(self, monkeypatch):
        """Test that unset env vars remain as literal strings."""
        # Arrange - ensure env var is not set
        monkeypatch.delenv("NONEXISTENT_VAR", raising=False)
        
        import tempfile
        import yaml
        
        test_data = {
            "window": {"width": 800},
            "characters": {
                "test": {
                    "name": "Test",
                    "llm": {
                        "type": "openai",
                        "version": "gpt-4o",
                        "api_key": "${NONEXISTENT_VAR}"
                    }
                }
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(test_data, f)
            temp_file = Path(f.name)
        
        try:
            # Act
            config = load_config(temp_file)
            
            # Assert - expandvars keeps literal if var doesn't exist
            char_config = config.characters["test"]
            # os.path.expandvars returns the literal string if var doesn't exist
            assert char_config["llm"]["api_key"] == "${NONEXISTENT_VAR}"
        finally:
            temp_file.unlink()
    
    def test_mixed_literal_and_env_var(self, monkeypatch):
        """Test mixing literal strings and environment variables."""
        # Arrange
        monkeypatch.setenv("PREFIX", "sk-")
        
        import tempfile
        import yaml
        
        test_data = {
            "window": {"width": 800},
            "characters": {
                "test": {
                    "name": "Test",
                    "llm": {
                        "type": "openai",
                        "version": "gpt-4o",
                        "api_key": "${PREFIX}actual_key_part"
                    }
                }
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(test_data, f)
            temp_file = Path(f.name)
        
        try:
            # Act
            config = load_config(temp_file)
            
            # Assert
            char_config = config.characters["test"]
            assert char_config["llm"]["api_key"] == "sk-actual_key_part"
        finally:
            temp_file.unlink()


"""
Tests for config.utils module.
"""
import os
import tempfile
from pathlib import Path
import pytest
from src.config.utils import load_config
from src.config.models.little_world_config import LittleWorldConfig


class TestLoadConfig:
    """Test load_config function."""
    
    def test_load_valid_yaml(self):
        """Test loading a valid YAML configuration file."""
        # Arrange
        test_file = Path(__file__).parent / "fixtures" / "valid_config.yaml"
        
        # Act
        config = load_config(test_file)
        
        # Assert
        assert isinstance(config, LittleWorldConfig)
        assert config.window.width == 1000
        assert config.window.height == 800
        assert config.colors.ground == (100, 200, 100)
        assert config.character.radius == 25
        assert config.character.speed == 10
        assert config.game.fps == 30
    
    def test_load_defaults_when_file_missing(self):
        """Test that defaults are used when config file doesn't exist."""
        # Arrange
        non_existent_file = Path("/non/existent/path/config.yaml")
        
        # Act
        config = load_config(non_existent_file)
        
        # Assert
        assert isinstance(config, LittleWorldConfig)
        assert config.window.width == 800  # Default value
        assert config.window.height == 600  # Default value
        assert config.game.fps == 60  # Default value
    
    def test_load_with_default_path(self, monkeypatch):
        """Test loading with default path (when config_filepath is None)."""
        # This test is tricky because it depends on the actual settings.yaml
        # We'll test that it doesn't crash and returns a valid config
        config = load_config()
        assert isinstance(config, LittleWorldConfig)
    
    def test_load_minimal_config(self):
        """Test loading a minimal configuration with only some fields."""
        # Arrange
        test_file = Path(__file__).parent / "fixtures" / "minimal_config.yaml"
        
        # Act
        config = load_config(test_file)
        
        # Assert
        assert isinstance(config, LittleWorldConfig)
        assert config.window.width == 640
        assert config.window.height == 480
        # Other fields should use defaults
        assert config.game.fps == 60  # Default
    
    def test_load_with_invalid_extension(self):
        """Test that invalid file extension raises ValueError."""
        # Arrange
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
            temp_file = Path(f.name)
            f.write(b"some content")
        
        try:
            # Act & Assert
            with pytest.raises(ValueError, match="Unsupported file extension"):
                load_config(temp_file)
        finally:
            # Cleanup
            temp_file.unlink()
    
    def test_load_with_invalid_yaml(self):
        """Test that invalid YAML falls back to defaults."""
        # Arrange
        with tempfile.NamedTemporaryFile(mode='w', suffix=".yaml", delete=False) as f:
            temp_file = Path(f.name)
            f.write("invalid: yaml: content: [unclosed")
        
        try:
            # Act
            config = load_config(temp_file)
            
            # Assert - should return defaults on error
            assert isinstance(config, LittleWorldConfig)
            assert config.window.width == 800  # Default
        finally:
            # Cleanup
            temp_file.unlink()
    
    def test_environment_variable_expansion(self, monkeypatch):
        """Test that environment variables are expanded correctly."""
        # Arrange
        test_api_key = "expanded_api_key_12345"
        monkeypatch.setenv("TEST_API_KEY", test_api_key)
        
        test_file = Path(__file__).parent / "fixtures" / "config_with_env_vars.yaml"
        
        # Act
        config = load_config(test_file)
        
        # Assert
        assert isinstance(config, LittleWorldConfig)
        assert config.characters is not None
        assert "test_ai" in config.characters
        ai_config = config.characters["test_ai"]
        assert ai_config["llm"]["api_key"] == test_api_key
    
    def test_character_configs_loaded(self):
        """Test that character instance configs are loaded correctly."""
        # Arrange
        test_file = Path(__file__).parent / "fixtures" / "valid_config.yaml"
        
        # Act
        config = load_config(test_file)
        
        # Assert
        assert config.characters is not None
        assert "test_player" in config.characters
        assert "test_ai" in config.characters
        
        # Check player config
        player_config = config.characters["test_player"]
        assert player_config["name"] == "Test Player"
        assert "llm" not in player_config or player_config.get("llm") is None
        
        # Check AI config
        ai_config = config.characters["test_ai"]
        assert ai_config["name"] == "Test AI"
        assert ai_config["llm"]["type"] == "openai"
        assert ai_config["llm"]["version"] == "gpt-4o"
        assert ai_config["llm"]["api_key"] == "test_api_key_12345"


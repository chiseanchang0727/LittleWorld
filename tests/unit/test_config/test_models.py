"""
Tests for config models (Pydantic validation).
"""
import pytest
from pydantic import ValidationError
from src.config.models.little_world_config import (
    LittleWorldConfig,
    WindowConfig,
    ColorsConfig,
    CharacterConfig,
    GameConfig,
)
from src.config.models.character_config import LLMConfig, CharacterInstanceConfig


class TestWindowConfig:
    """Test WindowConfig model."""
    
    def test_valid_window_config(self):
        """Test creating a valid WindowConfig."""
        config = WindowConfig(width=1920, height=1080)
        assert config.width == 1920
        assert config.height == 1080
    
    def test_window_config_defaults(self):
        """Test WindowConfig default values."""
        config = WindowConfig()
        assert config.width == 800
        assert config.height == 600
    
    def test_window_config_invalid_type(self):
        """Test that invalid types are rejected."""
        with pytest.raises(ValidationError):
            WindowConfig(width="not_a_number", height=600)


class TestColorsConfig:
    """Test ColorsConfig model."""
    
    def test_valid_colors_config(self):
        """Test creating a valid ColorsConfig."""
        config = ColorsConfig(
            ground=(255, 0, 0),
            player=(0, 255, 0),
            ai_character=(0, 0, 255)
        )
        assert config.ground == (255, 0, 0)
        assert config.player == (0, 255, 0)
        assert config.ai_character == (0, 0, 255)
    
    def test_colors_config_defaults(self):
        """Test ColorsConfig default values."""
        config = ColorsConfig()
        assert config.ground == (144, 238, 144)
        assert config.player == (219, 112, 147)
    
    def test_colors_config_invalid_tuple_length(self):
        """Test that invalid color tuples are rejected."""
        with pytest.raises(ValidationError):
            ColorsConfig(ground=(255, 0))  # Too short
        
        with pytest.raises(ValidationError):
            ColorsConfig(ground=(255, 0, 0, 255))  # Too long


class TestCharacterConfig:
    """Test CharacterConfig model."""
    
    def test_valid_character_config(self):
        """Test creating a valid CharacterConfig."""
        config = CharacterConfig(radius=30, speed=8)
        assert config.radius == 30
        assert config.speed == 8
    
    def test_character_config_defaults(self):
        """Test CharacterConfig default values."""
        config = CharacterConfig()
        assert config.radius == 20
        assert config.speed == 5


class TestGameConfig:
    """Test GameConfig model."""
    
    def test_valid_game_config(self):
        """Test creating a valid GameConfig."""
        config = GameConfig(fps=120)
        assert config.fps == 120
    
    def test_game_config_defaults(self):
        """Test GameConfig default values."""
        config = GameConfig()
        assert config.fps == 60


class TestLittleWorldConfig:
    """Test LittleWorldConfig model."""
    
    def test_valid_full_config(self):
        """Test creating a valid LittleWorldConfig with all fields."""
        config = LittleWorldConfig(
            window=WindowConfig(width=1920, height=1080),
            colors=ColorsConfig(ground=(255, 0, 0)),
            character=CharacterConfig(radius=30),
            game=GameConfig(fps=120)
        )
        assert config.window.width == 1920
        assert config.colors.ground == (255, 0, 0)
        assert config.character.radius == 30
        assert config.game.fps == 120
    
    def test_config_defaults(self):
        """Test LittleWorldConfig default values."""
        config = LittleWorldConfig()
        assert config.window.width == 800
        assert config.game.fps == 60
        assert config.characters is None
    
    def test_config_with_characters(self):
        """Test LittleWorldConfig with character instances."""
        config = LittleWorldConfig(
            characters={
                "player_a": {"name": "Player A"},
                "ai_a": {
                    "name": "AI A",
                    "llm": {
                        "type": "openai",
                        "version": "gpt-4o",
                        "api_key": "test_key"
                    }
                }
            }
        )
        assert config.characters is not None
        assert "player_a" in config.characters
        assert "ai_a" in config.characters


class TestLLMConfig:
    """Test LLMConfig model."""
    
    def test_valid_llm_config(self):
        """Test creating a valid LLMConfig."""
        config = LLMConfig(
            type="openai",
            version="gpt-4o",
            api_key="sk-test123"
        )
        assert config.type == "openai"
        assert config.version == "gpt-4o"
        assert config.api_key == "sk-test123"
    
    def test_llm_config_missing_fields(self):
        """Test that missing required fields raise ValidationError."""
        with pytest.raises(ValidationError):
            LLMConfig(type="openai")  # Missing version and api_key


class TestCharacterInstanceConfig:
    """Test CharacterInstanceConfig model."""
    
    def test_valid_character_instance_config(self):
        """Test creating a valid CharacterInstanceConfig."""
        llm_config = LLMConfig(
            type="openai",
            version="gpt-4o",
            api_key="sk-test123"
        )
        config = CharacterInstanceConfig(
            name="Test Character",
            llm=llm_config
        )
        assert config.name == "Test Character"
        assert config.llm is not None
        assert config.llm.type == "openai"
    
    def test_character_instance_config_without_llm(self):
        """Test CharacterInstanceConfig without LLM (for player characters)."""
        config = CharacterInstanceConfig(name="Player Character")
        assert config.name == "Player Character"
        assert config.llm is None
    
    def test_character_instance_config_missing_name(self):
        """Test that missing name raises ValidationError."""
        with pytest.raises(ValidationError):
            CharacterInstanceConfig()


"""
Factory for creating character instances with proper configuration.
"""
from typing import Optional
from config import LittleWorldConfig, CharacterConfig, load_config
from .base import PlayerCharacter, AICharacter


class CharacterFactory:
    """Factory for creating characters with dependency injection."""
    
    def __init__(self, config: Optional[LittleWorldConfig] = None):
        """
        Initialize factory with config.
        
        Args:
            config: Configuration object. If None, loads from YAML.
        """
        self.config = config or load_config()
    
    def create_player(
        self,
        x: float,
        y: float,
        color: Optional[tuple[int, int, int]] = None,
    ) -> PlayerCharacter:
        """
        Create a player character.
        
        Args:
            x: Initial x position
            y: Initial y position
            color: Character color. If None, uses config default.
            
        Returns:
            PlayerCharacter instance
        """
        return PlayerCharacter(
            x=x,
            y=y,
            config=self.config,
            color=color,
        )
    
    def create_ai(
        self,
        x: float,
        y: float,
        color: Optional[tuple[int, int, int]] = None,
        character_config: Optional[CharacterConfig] = None,
    ) -> AICharacter:
        """
        Create an AI character.
        
        Args:
            x: Initial x position
            y: Initial y position
            color: Character color. If None, uses config default.
            character_config: Character-specific config. If None, uses config default.
            
        Returns:
            AICharacter instance
        """
        return AICharacter(
            x=x,
            y=y,
            config=self.config,
            color=color,
            character_config=character_config,
        )


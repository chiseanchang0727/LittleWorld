"""
Character class for player_a.
"""
from config import CharacterInstanceConfig, LittleWorldConfig
from character import PlayerCharacter


class PlayerA(PlayerCharacter):
    """Player A character."""
    
    def __init__(
        self,
        config: LittleWorldConfig,
        x: float,
        y: float,
    ):
        """
        Initialize Player A character.
        
        Args:
            config: LittleWorldConfig object
            x: Initial x position
            y: Initial y position
        """
        # Look up player character instance config
        player_name = "Player A"
        if config.characters and "player_a" in config.characters:
            char_data = config.characters["player_a"]
            try:
                player_char_config = CharacterInstanceConfig(**char_data)
                player_name = player_char_config.name
            except Exception:
                pass
        
        # Initialize parent class
        super().__init__(x, y, config=config)
        self.name = player_name

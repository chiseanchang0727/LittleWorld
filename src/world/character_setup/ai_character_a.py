"""
Character class for ai_character_a.
"""
from config import CharacterInstanceConfig, LittleWorldConfig
from character import AICharacter


class AICharacterA(AICharacter):
    """AI Character A."""
    
    def __init__(
        self,
        config: LittleWorldConfig,
        world_ref,
        x: float,
        y: float,
    ):
        """
        Initialize AI Character A.
        
        Args:
            config: LittleWorldConfig object
            world_ref: Reference to World instance
            x: Initial x position
            y: Initial y position
        """
        # Look up AI character instance config
        vision_radius = None
        ai_char_name = "AI Character A"
        if config.characters and "ai_character_a" in config.characters:
            char_data = config.characters["ai_character_a"]
            try:
                ai_char_config = CharacterInstanceConfig(**char_data)
                vision_radius = ai_char_config.vision_radius
                ai_char_name = ai_char_config.name
            except Exception:
                pass
        
        # Initialize parent class
        super().__init__(
            x, y,
            config=config,
            vision_radius=vision_radius,
            world=world_ref,
        )
        self.name = ai_char_name

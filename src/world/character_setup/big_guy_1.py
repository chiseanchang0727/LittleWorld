"""
Character class for big_guy_1.
"""
from config import CharacterInstanceConfig, LittleWorldConfig
from character import AICharacter
from personality import load_personality
from language_model.llm_base_engine import BaseAIModelEngine


class BigGuyOne(AICharacter):
    """Big Guy 1 character."""
    
    def __init__(
        self,
        config: LittleWorldConfig,
        world_ref,
        x: float,
        y: float,
    ):
        """
        Initialize Big Guy 1 character.
        
        Args:
            config: LittleWorldConfig object
            world_ref: Reference to World instance
            x: Initial x position
            y: Initial y position
        """
        # Look up character instance config
        vision_radius = None
        char_name = "Big Guy 1"
        personality_file_path = None
        llm_config = None
        
        if config.characters and "big_guy_1" in config.characters:
            char_data = config.characters["big_guy_1"]
            try:
                char_config = CharacterInstanceConfig(**char_data)
                vision_radius = char_config.vision_radius
                char_name = char_config.name
                llm_config = char_config.llm
                # Get personality file path from raw data
                personality_file_path = char_data.get("personality")
            except Exception:
                pass
        
        # Load personality from file if path is provided
        personality = None
        if personality_file_path:
            try:
                personality = load_personality(personality_file_path)
            except Exception:
                # If loading fails, continue without personality
                pass
        
        # Create BaseAIModelEngine if both llm_config and personality are available
        model = None
        if llm_config and personality:
            try:
                model = BaseAIModelEngine(
                    config=llm_config,
                    personality_prompt=personality
                )
            except Exception as e:
                # If model creation fails, log and continue without model
                print(f"Warning: Failed to create LLM model for {char_name}: {e}")
                model = None
        
        # Initialize parent class
        super().__init__(
            x, y,
            config=config,
            vision_radius=vision_radius,
            world=world_ref,
            model=model,
            personality=personality,
        )
        self.name = char_name
    
    async def test_what_i_see(self, world_state):
        """
        Test method: Ask the character what they see based on world_state.
        
        Args:
            world_state: WorldState object containing observation data
            
        Returns:
            Response from the model describing what the character saw
        """
        if self.model is None:
            return "No model available"
        
        # Format world_state as text
        observation_dict = world_state.to_structured_dict() if world_state else {}
        world_state_text = f"""World State:
- My position: {observation_dict.get('observer_position', 'unknown')}
- Visible characters: {len(observation_dict.get('visible_characters', []))}
"""
        
        if observation_dict.get('visible_characters'):
            for char in observation_dict['visible_characters']:
                world_state_text += f"- {char['name']} ({char['character_type']}) at {char['distance']:.1f} pixels {char['direction']} from me\n"
        
        # Call model with world_state
        messages = {"world_state": world_state_text, "input_messages": ""}
        response = await self.model.basic_answering(messages)
        
        return response
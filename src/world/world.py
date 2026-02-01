"""
Main World class for managing the game world, game loop, and character interactions.
"""
import pygame
from typing import Optional
from config import LittleWorldConfig, load_config
from character import Character, AICharacter
from .world_state import WorldState, VisibleCharacter, WorldBounds, calculate_distance, calculate_direction
from .world_setup import setup_pygame
from .character_setup import PlayerA, AICharacterA, BigGuyOne
from .dialogue import render_dialogue_bubble
import asyncio


class World:
    def __init__(self, config: LittleWorldConfig | None = None):
        """
        Initialize world.
        
        Args:
            config: Configuration object. If None, loads from YAML.
        """
        # Load config if not provided (dependency injection)
        if config is None:
            config = load_config()
        self.config = config
        
        # Setup pygame (window, screen, clock)
        self.screen, self.clock = setup_pygame(config)
        self.running = True
        
        # Create characters using character classes
        self.player = PlayerA(
            config,
            config.window.width // 4,
            config.window.height // 2,
        )
        
        self.ai_character = AICharacterA(
            config,
            self,
            3 * config.window.width // 4,
            config.window.height // 2,
        )
        
        # Create BigGuyOne character
        self.big_guy = BigGuyOne(
            config,
            self,
            config.window.width // 2,
            config.window.height // 2,
        )
        
        # List of all characters
        self.characters = [self.player, self.ai_character, self.big_guy]
        
        # Dialogue bubble storage
        self.dialogue_text = None
        self.dialogue_character = None
        
        # Call test method after initialization
        self._init_test_observation()

    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def get_world_state_for(self, character: Character, vision_radius: float) -> WorldState:
        """
        Get world state observation for a specific character.
        
        Args:
            character: The character requesting the observation
            vision_radius: Vision radius in pixels
            
        Returns:
            WorldState object with structured observation data
        """
        observer_x, observer_y = character.x, character.y
        
        # Find visible characters (within vision radius, excluding self)
        visible_chars = []
        for other_char in self.characters:
            if other_char is character:
                continue
            
            distance = calculate_distance(observer_x, observer_y, other_char.x, other_char.y)
            if distance <= vision_radius:
                relative_x = other_char.x - observer_x
                relative_y = other_char.y - observer_y
                direction = calculate_direction(relative_x, relative_y)
                
                # Determine character type
                char_type = "player" if isinstance(other_char, type(self.player)) else "ai"
                char_name = getattr(other_char, 'name', f"{char_type}_character")
                
                visible_chars.append(VisibleCharacter(
                    name=char_name,
                    character_type=char_type,
                    relative_x=relative_x,
                    relative_y=relative_y,
                    distance=distance,
                    direction=direction
                ))
        
        # Calculate world bounds
        world_bounds = WorldBounds(
            distance_to_north=observer_y,
            distance_to_south=self.config.window.height - observer_y,
            distance_to_east=self.config.window.width - observer_x,
            distance_to_west=observer_x,
            world_width=self.config.window.width,
            world_height=self.config.window.height
        )
        
        return WorldState(
            observer_position=(observer_x, observer_y),
            vision_radius=vision_radius,
            visible_characters=visible_chars,
            world_bounds=world_bounds
        )

    def update(self):
        """Update world state"""
        # Handle player input
        keys = pygame.key.get_pressed()
        self.player.handle_input(keys)
        
        # Update AI character - pass world state (passive mode)
        if isinstance(self.ai_character, AICharacter):
            world_state = self.get_world_state_for(self.ai_character, self.ai_character.vision_radius)
            self.ai_character.update(world_state=world_state)
        else:
            self.ai_character.update()

    def _init_test_observation(self):
        """Initialize and call test observation for BigGuyOne."""
        async def test_observation():
            if hasattr(self.big_guy, 'model') and self.big_guy.model:
                world_state = self.get_world_state_for(self.big_guy, self.big_guy.vision_radius)
                response = await self.big_guy.test_what_i_see(world_state)
                # Extract text from response (handle different response types)
                if hasattr(response, 'content'):
                    self.dialogue_text = response.content
                elif isinstance(response, str):
                    self.dialogue_text = response
                else:
                    self.dialogue_text = str(response)
                self.dialogue_character = self.big_guy
        
        # Run async function
        try:
            asyncio.run(test_observation())
        except Exception as e:
            print(f"Error in test observation: {e}")
            self.dialogue_text = f"Error: {e}"
            self.dialogue_character = self.big_guy

    def render(self):
        """Render the world"""
        # Fill screen with ground color
        self.screen.fill(self.config.colors.ground)
        
        # Render all characters
        for character in self.characters:
            character.render(self.screen)
        
        # Render dialogue bubble if there's dialogue text
        if self.dialogue_text and self.dialogue_character:
            render_dialogue_bubble(
                self.screen,
                self.dialogue_text,
                self.dialogue_character.x,
                self.dialogue_character.y,
            )
        
        # Update display
        pygame.display.flip()

    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(self.config.game.fps)
        
        pygame.quit()

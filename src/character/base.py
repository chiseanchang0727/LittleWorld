import pygame
import random
from typing import Optional
from config import LittleWorldConfig, CharacterConfig, ColorsConfig, WindowConfig
from decisions import Decision, ActionType


class Character:
    """Base character class"""
    def __init__(
        self,
        x: float,
        y: float,
        color: tuple[int, int, int],
        config: LittleWorldConfig,
        character_config: Optional[CharacterConfig] = None,
        window_config: Optional[WindowConfig] = None,
    ):
        """
        Initialize character.
        
        Args:
            x: Initial x position
            y: Initial y position
            color: Character color (RGB tuple)
            config: Configuration object (required, dependency injection)
            character_config: Character-specific config. If None, uses config.character
            window_config: Window config. If None, uses config.window
        """
        self.x = x
        self.y = y
        self.color = color
        self.config = config
        
        # Use provided character config or default from main config
        self.character_config = character_config or config.character
        self.window_config = window_config or config.window
        
        self.radius = self.character_config.radius
        self.speed = self.character_config.speed

    def move(self, dx, dy):
        """Move the character by dx, dy, keeping within screen bounds"""
        new_x = self.x + dx
        new_y = self.y + dy
        
        # Keep character within screen boundaries
        new_x = max(self.radius, min(self.window_config.width - self.radius, new_x))
        new_y = max(self.radius, min(self.window_config.height - self.radius, new_y))
        
        self.x = new_x
        self.y = new_y

    def update(self):
        """Update character state - override in subclasses"""
        pass

    def render(self, screen):
        """Render the character as a circle"""
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)


class PlayerCharacter(Character):
    """Player-controlled character"""
    def __init__(
        self,
        x: float,
        y: float,
        config: LittleWorldConfig,
        color: Optional[tuple[int, int, int]] = None,
    ):
        """
        Initialize player character.
        
        Args:
            x: Initial x position
            y: Initial y position
            config: Configuration object (required, dependency injection)
            color: Character color. If None, uses config.colors.player
        """
        color = color or config.colors.player
        super().__init__(x, y, color, config=config)

    def handle_input(self, keys):
        """Handle keyboard input for movement"""
        dx = 0
        dy = 0
        
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += self.speed
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += self.speed
        
        if dx != 0 or dy != 0:
            self.move(dx, dy)


class AICharacter(Character):
    """AI-controlled character"""
    def __init__(
        self,
        x: float,
        y: float,
        config: LittleWorldConfig,
        color: Optional[tuple[int, int, int]] = None,
        character_config: Optional[CharacterConfig] = None,
    ):
        """
        Initialize AI character.
        
        Args:
            x: Initial x position
            y: Initial y position
            config: Configuration object (required, dependency injection)
            color: Character color. If None, uses config.colors.ai_character
            character_config: Character-specific config. If None, uses config.character
        """
        color = color or config.colors.ai_character
        super().__init__(x, y, color, config=config, character_config=character_config)
        self.direction_change_timer = 0
        self.current_dx = 0
        self.current_dy = 0

    def update(self):
        """Update AI character - moves randomly"""
        # Change direction every 60 frames (about 1 second at 60 FPS)
        self.direction_change_timer += 1
        if self.direction_change_timer >= 60:
            # Randomly choose a direction
            directions = [
                (0, -self.speed),   # Up
                (0, self.speed),    # Down
                (-self.speed, 0),   # Left
                (self.speed, 0),    # Right
                (0, 0)              # Stay
            ]
            self.current_dx, self.current_dy = random.choice(directions)
            self.direction_change_timer = 0
        
        # Move in current direction
        if self.current_dx != 0 or self.current_dy != 0:
            self.move(self.current_dx, self.current_dy)

    def make_decision(self, world_state, personality):
        """
        Make a decision based on world state and personality, then execute the appropriate action.
        
        This method will be called periodically (e.g., every 3 seconds) to determine what
        the AI character should do next. The decision can be to observe, communicate, or interact.
        
        Args:
            world_state: Current state of the world (visible characters, objects, etc.)
            personality: Character's personality traits and preferences
            
        Returns:
            Decision: Pydantic model containing the action type and parameters
            
        Example:
            decision = self.make_decision(world_state, personality)
            if decision.type == ActionType.OBSERVE:
                observation = self.observe(decision.radius)
            elif decision.type == ActionType.COMMUNICATE:
                self.communication(decision.target, decision.message)
            elif decision.type == ActionType.INTERACT:
                self.interact(decision.target)
            elif decision.type == ActionType.MOVE:
                self.move(decision.dx, decision.dy)
        """
        # TODO: Implement AI decision-making
        # 1. Use ai_agent to call LLM with world_state and personality
        # 2. Use LLM.with_structured_output(Decision) to get structured Decision object
        # 3. Return the Decision object
        pass

    def observe(self, radius):
        """
        Observer the environment
        """
        pass
    
    def communication(self):
        """
        Communicatet with other character.
        """
        pass
    
    def interact(self):
        """
        Interact with env or other character.
        """
        pass
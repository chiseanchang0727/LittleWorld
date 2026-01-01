import pygame
from config import LittleWorldConfig, load_config
from character import CharacterFactory


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
        
        # Create character factory with config
        self.character_factory = CharacterFactory(config)
        
        pygame.init()
        self.screen = pygame.display.set_mode((config.window.width, config.window.height))
        pygame.display.set_caption("LittleWorld")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Create player character (left side) using factory
        self.player = self.character_factory.create_player(
            config.window.width // 4,
            config.window.height // 2,
        )
        
        # Create AI character (right side) using factory
        self.ai_character = self.character_factory.create_ai(
            3 * config.window.width // 4,
            config.window.height // 2,
        )
        
        # List of all characters
        self.characters = [self.player, self.ai_character]

    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self):
        """Update world state"""
        # Handle player input
        keys = pygame.key.get_pressed()
        self.player.handle_input(keys)
        
        # Update AI character (moves randomly)
        self.ai_character.update()

    def render(self):
        """Render the world"""
        # Fill screen with ground color
        self.screen.fill(self.config.colors.ground)
        
        # Render all characters
        for character in self.characters:
            character.render(self.screen)
        
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


import pygame
from config import WINDOW_WIDTH, WINDOW_HEIGHT, GROUND_COLOR, FPS
from character import PlayerCharacter, AICharacter


class World:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("LittleWorld")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Create player character (left side)
        self.player = PlayerCharacter(WINDOW_WIDTH // 4, WINDOW_HEIGHT // 2)
        
        # Create AI character (right side)
        self.ai_character = AICharacter(3 * WINDOW_WIDTH // 4, WINDOW_HEIGHT // 2)
        
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
        self.screen.fill(GROUND_COLOR)
        
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
            self.clock.tick(FPS)
        
        pygame.quit()


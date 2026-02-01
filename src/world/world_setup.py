"""
World setup utilities for background, window, and general settings.
"""
import pygame
from config import LittleWorldConfig


def setup_pygame(config: LittleWorldConfig):
    """
    Initialize pygame and create the game window.
    
    Args:
        config: Configuration object
        
    Returns:
        Tuple of (screen, clock) pygame objects
    """
    pygame.init()
    screen = pygame.display.set_mode((config.window.width, config.window.height))
    pygame.display.set_caption("LittleWorld")
    clock = pygame.time.Clock()
    return screen, clock

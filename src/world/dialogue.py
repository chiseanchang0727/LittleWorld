"""
Dialogue bubble rendering utilities.
"""
import pygame
from typing import Optional


def render_dialogue_bubble(
    screen: pygame.Surface,
    text: str,
    x: float,
    y: float,
    font: Optional[pygame.font.Font] = None,
    max_width: int = 200,
    padding: int = 10,
    bg_color: tuple[int, int, int] = (255, 255, 255),
    text_color: tuple[int, int, int] = (0, 0, 0),
    border_color: tuple[int, int, int] = (0, 0, 0),
    border_width: int = 2,
) -> None:
    """
    Render a dialogue bubble with text above a character.
    
    Args:
        screen: Pygame surface to render on
        text: Text to display
        x: X position (character center)
        y: Y position (character center)
        font: Pygame font object. If None, creates default font
        max_width: Maximum width of the bubble in pixels
        padding: Padding inside the bubble
        bg_color: Background color (RGB)
        text_color: Text color (RGB)
        border_color: Border color (RGB)
        border_width: Border width in pixels
    """
    if font is None:
        font = pygame.font.Font(None, 24)
    
    # Wrap text to fit max_width
    words = text.split(' ')
    lines = []
    current_line = []
    current_width = 0
    
    for word in words:
        word_surface = font.render(word, True, text_color)
        word_width = word_surface.get_width()
        
        if current_width + word_width <= max_width - 2 * padding:
            current_line.append(word)
            current_width += word_width + font.size(' ')[0]
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
            current_width = word_width
    
    if current_line:
        lines.append(' '.join(current_line))
    
    # Calculate bubble dimensions
    line_height = font.get_height()
    bubble_height = len(lines) * line_height + 2 * padding
    bubble_width = max_width
    
    # Position bubble above character (centered)
    bubble_x = int(x - bubble_width // 2)
    bubble_y = int(y - 40 - bubble_height)  # 40 pixels above character
    
    # Draw bubble background
    bubble_rect = pygame.Rect(bubble_x, bubble_y, bubble_width, bubble_height)
    pygame.draw.rect(screen, bg_color, bubble_rect)
    pygame.draw.rect(screen, border_color, bubble_rect, border_width)
    
    # Draw text lines
    for i, line in enumerate(lines):
        text_surface = font.render(line, True, text_color)
        text_x = bubble_x + padding
        text_y = bubble_y + padding + i * line_height
        screen.blit(text_surface, (text_x, text_y))
    
    # Draw small triangle pointing to character
    triangle_points = [
        (int(x), int(y - 40)),  # Bottom point (above character)
        (int(x - 10), int(y - 40 - 10)),  # Top left
        (int(x + 10), int(y - 40 - 10)),  # Top right
    ]
    pygame.draw.polygon(screen, bg_color, triangle_points)
    pygame.draw.polygon(screen, border_color, triangle_points, border_width)

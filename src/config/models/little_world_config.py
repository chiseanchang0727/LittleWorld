"""
Configuration models using Pydantic for type safety and validation.
"""
from pydantic import BaseModel, Field
from typing import Tuple, Optional


class WindowConfig(BaseModel):
    """Window display settings."""
    width: int = Field(default=800, description="Window width in pixels")
    height: int = Field(default=600, description="Window height in pixels")


class ColorsConfig(BaseModel):
    """Color settings for game elements."""
    ground: Tuple[int, int, int] = Field(
        default=(144, 238, 144),
        description="Ground color (RGB)"
    )
    world_background: Tuple[int, int, int] = Field(
        default=(144, 238, 144),
        description="World background color (RGB)"
    )
    character: Tuple[int, int, int] = Field(
        default=(219, 112, 147),
        description="Default character color (RGB)"
    )
    player: Tuple[int, int, int] = Field(
        default=(219, 112, 147),
        description="Player character color (RGB)"
    )
    ai_character: Tuple[int, int, int] = Field(
        default=(255, 165, 0),
        description="AI character color (RGB)"
    )


class CharacterConfig(BaseModel):
    """Character settings."""
    radius: int = Field(default=20, description="Character radius in pixels")
    speed: int = Field(default=5, description="Character movement speed (pixels per frame)")


class GameConfig(BaseModel):
    """Game loop settings."""
    fps: int = Field(default=60, description="Frames per second")


class LittleWorldConfig(BaseModel):
    """Main configuration model for LittleWorld."""
    window: WindowConfig = Field(default_factory=WindowConfig, description="Window settings")
    colors: ColorsConfig = Field(default_factory=ColorsConfig, description="Color settings")
    character: CharacterConfig = Field(default_factory=CharacterConfig, description="Character settings")
    game: GameConfig = Field(default_factory=GameConfig, description="Game loop settings")
    characters: Optional[dict[str, dict]] = Field(default=None, description="Character instance configurations")


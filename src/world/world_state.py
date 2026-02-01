"""
World state models for AI character observations.
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from math import sqrt, atan2, degrees


class VisibleCharacter(BaseModel):
    """Information about a visible character."""
    name: str = Field(description="Character name/identifier")
    character_type: Literal["player", "ai"] = Field(description="Type of character")
    relative_x: float = Field(description="X position relative to observer (pixels)")
    relative_y: float = Field(description="Y position relative to observer (pixels)")
    distance: float = Field(description="Distance from observer (pixels)")
    direction: str = Field(description="Direction from observer (e.g., 'north', 'south-east')")


class WorldBounds(BaseModel):
    """Information about world boundaries relative to observer."""
    distance_to_north: float = Field(description="Distance to north edge (pixels)")
    distance_to_south: float = Field(description="Distance to south edge (pixels)")
    distance_to_east: float = Field(description="Distance to east edge (pixels)")
    distance_to_west: float = Field(description="Distance to west edge (pixels)")
    world_width: int = Field(description="Total world width (pixels)")
    world_height: int = Field(description="Total world height (pixels)")


class WorldState(BaseModel):
    """Structured world state observation for an AI character."""
    observer_position: tuple[float, float] = Field(description="Observer's (x, y) position")
    vision_radius: float = Field(description="Vision radius used for this observation")
    visible_characters: List[VisibleCharacter] = Field(default_factory=list, description="List of visible characters")
    world_bounds: WorldBounds = Field(description="World boundary information")
    
    def to_structured_dict(self) -> dict:
        """Convert to structured dictionary for LLM processing."""
        return self.model_dump()


def calculate_distance(x1: float, y1: float, x2: float, y2: float) -> float:
    """Calculate Euclidean distance between two points."""
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def calculate_direction(dx: float, dy: float) -> str:
    """
    Calculate cardinal/intercardinal direction from dx, dy.
    
    Args:
        dx: Delta x (positive = east, negative = west)
        dy: Delta y (positive = south, negative = north)
        
    Returns:
        Direction string (e.g., 'north', 'north-east', 'east')
    """
    if abs(dx) < 0.1 and abs(dy) < 0.1:
        return "here"
    
    # Calculate angle in degrees (0 = east, 90 = south, 180 = west, 270 = north)
    angle = degrees(atan2(dy, dx))
    
    # Normalize to 0-360
    if angle < 0:
        angle += 360
    
    # Map to directions
    if 337.5 <= angle or angle < 22.5:
        return "east"
    elif 22.5 <= angle < 67.5:
        return "south-east"
    elif 67.5 <= angle < 112.5:
        return "south"
    elif 112.5 <= angle < 157.5:
        return "south-west"
    elif 157.5 <= angle < 202.5:
        return "west"
    elif 202.5 <= angle < 247.5:
        return "north-west"
    elif 247.5 <= angle < 292.5:
        return "north"
    else:  # 292.5 <= angle < 337.5
        return "north-east"

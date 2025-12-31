from enum import Enum
from typing import Optional
from pydantic import BaseModel


class ActionType(str, Enum):
    """Types of actions a character can take"""
    OBSERVE = "observe"
    MOVE = "move"
    COMMUNICATE = "communicate"
    INTERACT = "interact"
    STAY = "stay"


class Decision(BaseModel):
    """Decision made by AI character about what action to take"""
    type: ActionType
    # Parameters specific to each action type
    radius: Optional[float] = None  # For observe action
    dx: Optional[int] = None  # For move action (delta x)
    dy: Optional[int] = None  # For move action (delta y)
    target: Optional[str] = None  # For communicate/interact (target character/object ID)
    message: Optional[str] = None  # For communicate action
    interaction_type: Optional[str] = None  # For interact action (what kind of interaction)


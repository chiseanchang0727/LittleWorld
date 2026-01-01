"""
Character module for LittleWorld.

Exports character classes and factory.
"""
from .base import Character, PlayerCharacter, AICharacter
from .character_factory import CharacterFactory

__all__ = [
    "Character",
    "PlayerCharacter",
    "AICharacter",
    "CharacterFactory",
]


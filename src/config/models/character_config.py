"""
Character-specific configuration models.
"""
from pydantic import BaseModel, Field
from typing import Optional


class LLMConfig(BaseModel):
    """LLM configuration for AI characters."""
    type: str = Field(description="LLM provider type (e.g., 'openai', 'gemini', 'vllm')")
    version: str = Field(description="Model version (e.g., 'gpt-4o', 'gpt-3.5-turbo')")
    api_key: str = Field(description="API key (environment variables expanded via os.path.expandvars)")


class CharacterInstanceConfig(BaseModel):
    """Configuration for a specific character instance."""
    name: str = Field(description="Character name/identifier")
    llm: Optional[LLMConfig] = Field(default=None, description="LLM configuration (for AI characters)")
    vision_radius: Optional[float] = Field(default=200.0, description="Vision radius in pixels (for AI characters)")
    # Add other character-specific settings here as needed
    # e.g., personality_file, decision_interval, etc.


"""
Utility functions for loading configuration from YAML.
"""
import os
import yaml
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
from .models.little_world_config import LittleWorldConfig


def load_config(config_filepath: Optional[Path] = None) -> LittleWorldConfig:
    """
    Load configuration from YAML file, with environment variable expansion.
    
    Args:
        config_filepath: Path to config file. If None, uses default settings.yaml.
        
    Returns:
        LittleWorldConfig instance
    """
    load_dotenv()
    
    if config_filepath is None:
        config_filepath = Path(__file__).parent / "settings.yaml"
    
    config_filepath = Path(config_filepath)
    
    if not config_filepath.exists():
        # Use defaults if YAML doesn't exist
        return LittleWorldConfig()
    
    file_extension = config_filepath.suffix
    
    # Check file extension first - raise error immediately if invalid
    match file_extension:
        case '.yml' | '.yaml':
            pass  # Valid extension
        case _:
            raise ValueError(
                f"Unable to parse config. Unsupported file extension: {file_extension}"
            )
    
    # Try to load and parse YAML
    try:
        with config_filepath.open("r", encoding="utf-8") as f:
            raw_content = f.read()
            expanded_content = os.path.expandvars(raw_content)  # Expand ${VAR}
            config_data = yaml.safe_load(expanded_content) or {}
        
        return LittleWorldConfig(**config_data)
    except Exception:
        # If YAML parsing fails, use defaults
        return LittleWorldConfig()


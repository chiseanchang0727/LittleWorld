"""
Personality loading utilities for AI characters.
"""
from pathlib import Path


def load_personality(file_path: str | Path) -> str:
    """
    Load personality text from a file.
    
    Args:
        file_path: Path to personality file (relative to project root or absolute)
        
    Returns:
        Personality text as string
    """
    path = Path(file_path)
    
    # If relative path, try relative to project root
    if not path.is_absolute():
        project_root = Path(__file__).parent.parent
        path = project_root / path
    
    with path.open("r", encoding="utf-8") as f:
        return f.read().strip()

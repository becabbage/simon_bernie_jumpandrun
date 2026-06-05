"""
Level Manager - Handles loading and saving game levels from .map files
"""

import os
import json
from pathlib import Path


def get_map_files(directory='.'):
    """
    Search for all .map files in the given directory.
    
    Args:
        directory: Path to search in (default: current directory)
    
    Returns:
        Sorted list of .map file paths
    """
    map_files = list(Path(directory).glob('*.map'))
    return sorted(map_files)


def load_level(filepath):
    """
    Load a level from a .map file.
    
    Args:
        filepath: Path to the .map file
    
    Returns:
        2D list representing the game world
    
    Raises:
        FileNotFoundError: If the file doesn't exist
        json.JSONDecodeError: If the file is not valid JSON
    """
    with open(filepath, 'r') as f:
        world_data = json.load(f)
    return world_data


def save_level(world_data, filepath):
    """
    Save a level to a .map file.
    
    Args:
        world_data: 2D list representing the game world
        filepath: Path where to save the .map file
    """
    with open(filepath, 'w') as f:
        json.dump(world_data, f, indent=2)


def get_level_name(filepath):
    """
    Extract a friendly name from the level file path.
    
    Args:
        filepath: Path to the .map file
    
    Returns:
        Filename without .map extension
    """
    return Path(filepath).stem

import os
import sys
from MindMateAI.logger import logger
from box import ConfigBox
from box.ennotaions import ensure_annotations
from typing import Any, List 
from box.exceptions import BoxValueError
from pathlib import Path
import yaml

@ensure_annotations
def read_yaml(path: Path) -> ConfigBox:
    """
    Reads a YAML file and returns its content as a ConfigBox.
    
    Args:
        path (str): The path to the YAML file.
    
    Returns:
        ConfigBox: The content of the YAML file as a ConfigBox.
    """
    try:
        with open(path, "r", encoding="utf-8") as file:
            content = yaml.safe_load(file)
            logger.info(f"Successfully read YAML file: {path}")
    except BoxValueError as e:
        logger.error(f"Error reading YAML file: {e}")
        raise FileNotFoundError(f"YAML file not found at path: {path}")
    except Exception as e:
        logger.error(f"Unexpected error reading YAML file: {e}")
        raise e
    return ConfigBox(content)
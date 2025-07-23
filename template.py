import os
import sys
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
ProjectName = "MindMateAI"

list_of_files = [
    f"src/{ProjectName}/__init__.py",
    f"src/{ProjectName}/Agents/__init__.py",
    f"src/{ProjectName}/Agents/agent.py",
    f"src/{ProjectName}/Tools/__init__.py",
    f"src/{ProjectName}/Tools/tool.py",
    f"src/{ProjectName}/utils/__init__.py",
    f"src/{ProjectName}/utils/common.py",
    f"src/{ProjectName}/Workflow/__init__.py",
    f"src/{ProjectName}/Workflow/workflow.py",
    "config/config.yaml",
    "app.py",
    "requirements.txt",
    "setup.py",
    "research/research.ipynb",
    "templates/index.html",
]

for file in list_of_files:
    try:
        file_path = Path(file)
        file_dir, file_name = os.path.split(file_path)
        if file_dir != "":
            os.makedirs(file_dir, exist_ok=True)
            logging.info(f"Created directory: {file_dir}")
        if (not os.path.exists(file_name)) or (os.path.getsize(file_name) == 0):
            with open(file_path, 'w') as f:
                pass
            logging.info(f"Created file: {file_name}")
        else:
            logging.info(f"File already exists and is not empty: {file_name}")
    except Exception as e:
        logging.error(f"Error creating file {file}: {e}")


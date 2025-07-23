import os
import sys
import logging


log_dir = "logs"
os.path.join(log_dir, "mindmate.log")
os.makedirs(log_dir, exist_ok=True)

formatter = "[%(asctime)s - %(name)s - %(levelname)s - %(message)s]"

logging.basicConfig(
    level=logging.INFO,
    format=formatter,
    handlers=[
        logging.FileHandler(os.path.join(log_dir, "mindmate.log")),
        logging.StreamHandler(sys.stdout),
    ],
)

logger = logging.getLogger("MindMateAI Logger")
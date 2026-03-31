import logging
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def setup_logger(log_file=None, level=logging.INFO, max_mb=3):
    if log_file is None:
        log_file = BASE_DIR / "hygiene.log"
    if os.path.exists(log_file) and os.path.getsize(log_file) > max_mb * 1024 * 1024:
        os.rename(log_file, f"{log_file}.old")

    logging.basicConfig(
        level=level,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger("HygieneCore")

logger = setup_logger()

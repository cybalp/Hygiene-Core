#!/usr/bin/env python3

__version__ = "1.0.0"

import sys
import os
import fcntl
import yaml
from pathlib import Path
from contextlib import contextmanager

from system.orchestrator import Orchestrator
from system.logger import logger
from telegram.sender import TelegramSender
from telegram.design import ReportDesigner

BASE_DIR = Path(__file__).resolve().parent

@contextmanager
def acquire_lock(lock_path=None):
    """
    Context Manager to prevent simultaneous executions.
    """
    if lock_path is None:
        lock_path = "/tmp/hygiene.lock"
        
    f = open(lock_path, "w")
    try:
        fcntl.lockf(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        yield
    except IOError:
        logger.error("Another instance of Hygiene-Core is already running.")
        sys.exit(1)
    finally:
        f.close()
        if os.path.exists(lock_path):
            os.remove(lock_path)

def load_config(config_name="config.yaml"):
    """Load configuration file safely."""
    config_path = BASE_DIR / config_name
    if not config_path.exists():
        logger.critical(f"Config file not found: {config_path}")
        sys.exit(1)
        
    with open(config_path, 'r') as conf_file:
        return yaml.safe_load(conf_file)

def main():
    with acquire_lock():
        try:
            # 1. Load config
            config = load_config()

            # 2. Run pipeline
            orchestrator = Orchestrator()
            logger.info(f"Hygiene-Core v{__version__} started.")
            results = orchestrator.run_pipeline()
            
            # 3. Handle Telegram Notification
            if config.get("telegram_report") and results:
                sender = TelegramSender()
                report = ReportDesigner.create_markdown(results, version=__version__)
                sender.send_report(report)
                logger.info("Telegram report sent.")

            logger.info(f"Hygiene-Core finished. Modules processed: {len(results)}")
            
        except Exception as e:
            logger.critical(f"System crash: {str(e)}")

if __name__ == "__main__":
    main()

import os
import time

class ThumbnailCleaner:
    def __init__(self, config):
        self.config = config
        self.dry_run = self.config.get('dry_run', True)
        self.expiry_days = self.config.get('thumbnail_expiry_days', 14)

    def run(self):
        target_dir = os.path.expanduser('~/.cache/thumbnails')
        cleaned_size = 0
        now = time.time()
        expiry_sec = self.expiry_days * 86400

        if not os.path.exists(target_dir):
            return {"module": "Thumbnail Cleaner", "status": "Success", "cleaned_mb": 0, "dry_run": self.dry_run}

        for root, _, files in os.walk(target_dir):
            for name in files:
                file_path = os.path.join(root, name)
                try:
                    stat = os.stat(file_path)
                    if (now - stat.st_mtime) > expiry_sec:
                        cleaned_size += stat.st_size
                        if not self.dry_run:
                            os.remove(file_path)
                except OSError:
                    continue

        return {
            "module": "Thumbnail Cleaner",
            "status": "Success",
            "cleaned_mb": cleaned_size / (1024*1024),
            "dry_run": self.dry_run
        }

import os
import time
import shutil

class TrashCleaner:
    def __init__(self, config):
        self.config = config
        self.dry_run = self.config.get('dry_run', True)
        self.expiry_days = self.config.get('trash_expiry_days', 30)

    def run(self):
        trash_dir = os.path.expanduser('~/.local/share/Trash')
        cleaned_size = 0
        now = time.time()
        expiry_sec = self.expiry_days * 86400

        if not os.path.exists(trash_dir):
            return {"module": "Trash Cleaner", "status": "Success", "cleaned_mb": 0, "dry_run": self.dry_run}

        for folder in ['files', 'info']:
            target = os.path.join(trash_dir, folder)
            if not os.path.exists(target):
                continue
                
            for item in os.listdir(target):
                item_path = os.path.join(target, item)
                try:
                    stat = os.stat(item_path)
                    if (now - stat.st_mtime) > expiry_sec:
                        if os.path.isfile(item_path):
                            size = os.path.getsize(item_path)
                            cleaned_size += size
                            if not self.dry_run:
                                os.remove(item_path)
                        elif os.path.isdir(item_path):
                            # get dir size
                            dir_size = sum(os.path.getsize(os.path.join(dp, f)) for dp, _, fn in os.walk(item_path) for f in fn if not os.path.islink(os.path.join(dp, f)))
                            cleaned_size += dir_size
                            if not self.dry_run:
                                shutil.rmtree(item_path)
                except Exception:
                    pass

        return {
            "module": "Trash Cleaner",
            "status": "Success",
            "cleaned_mb": cleaned_size / (1024*1024),
            "dry_run": self.dry_run
        }

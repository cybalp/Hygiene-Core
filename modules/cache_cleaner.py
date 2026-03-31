import os
import time
import subprocess
from pathlib import Path

class CacheCleaner:
    def __init__(self, config):
        self.config = config
        self.expiry_days = self.config.get('cache_expiry_days', 7)
        self.exclude_list = self.config.get('exclude_list', [])
        self.dry_run = self.config.get('dry_run', True)
        self.cleaned_size = 0
        self.open_files = set()

    def pre_run(self):
        """Protect files currently in use by using LSOF."""
        try:
            home_cache = os.path.expanduser('~/.cache')
            output = subprocess.check_output(['lsof', '+D', home_cache], 
                                           stderr=subprocess.DEVNULL).decode()
            for line in output.splitlines()[1:]:
                parts = line.split()
                if len(parts) > 8:
                    self.open_files.add(parts[-1])
        except Exception:
            pass

    def run(self):
        target_dirs = [os.path.expanduser('~/.cache')]
        if os.geteuid() == 0:
            target_dirs.append('/var/cache')
        
        now = time.time()
        expiry_sec = self.expiry_days * 86400

        for directory in target_dirs:
            if not os.path.exists(directory):
                continue
                
            for root, dirs, files in os.walk(directory):
                if any(ex in root for ex in self.exclude_list):
                    continue

                for name in files:
                    file_path = os.path.join(root, name)
                    
                    if file_path in self.open_files:
                        continue
                    
                    try:
                        filestat = os.stat(file_path)
                        if (now - filestat.st_mtime) > expiry_sec:
                            self.cleaned_size += filestat.st_size
                            if not self.dry_run:
                                os.remove(file_path)
                    except OSError:
                        continue

        return {
            "module": "Cache Cleaner",
            "status": "Success",
            "cleaned_mb": self.cleaned_size / (1024 * 1024),
            "dry_run": self.dry_run
        }

    def post_run(self):
        pass

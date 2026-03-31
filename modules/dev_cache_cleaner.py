import os
import shutil

class DevCacheCleaner:
    def __init__(self, config):
        self.config = config
        self.dry_run = self.config.get('dry_run', True)

    def get_dir_size(self, path):
        total_size = 0
        try:
            for dirpath, _, filenames in os.walk(path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    if not os.path.islink(fp):
                        total_size += os.path.getsize(fp)
        except Exception:
            pass
        return total_size

    def run(self):
        cleaned_size = 0
        
        targets = []
        if self.config.get('clean_npm_cache', True):
            targets.append(os.path.expanduser('~/.npm/_cacache'))
        if self.config.get('clean_pip_cache', True):
            targets.append(os.path.expanduser('~/.cache/pip'))
        if self.config.get('clean_cargo_cache', True):
            targets.append(os.path.expanduser('~/.cargo/registry/cache'))
            
        for target in targets:
            if os.path.exists(target):
                size = self.get_dir_size(target)
                cleaned_size += size
                if not self.dry_run:
                    shutil.rmtree(target, ignore_errors=True)

        return {
            "module": "Dev Cache Cleaner",
            "status": "Success",
            "cleaned_mb": cleaned_size / (1024*1024),
            "dry_run": self.dry_run
        }

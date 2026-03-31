import os
import subprocess

class PackageManagerCleaner:
    def __init__(self, config):
        self.config = config
        self.dry_run = self.config.get('dry_run', True)
        self.clean_aur = self.config.get('clean_aur_cache', True)

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
        error_msg = None
        
        # Pacman (needs root, we'll try)
        pacman_dir = '/var/cache/pacman/pkg'
        if os.path.exists(pacman_dir):
            size_before = self.get_dir_size(pacman_dir)
            if not self.dry_run:
                try:
                    subprocess.run(['sudo', '-n', 'pacman', '-Sc', '--noconfirm'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    size_after = self.get_dir_size(pacman_dir)
                    cleaned_size += max(0, size_before - size_after)
                except subprocess.CalledProcessError:
                    error_msg = "Root permissions required for pacman (-Sc) without password."
        
        # Yay
        yay_dir = os.path.expanduser('~/.cache/yay')
        if self.clean_aur and os.path.exists(yay_dir):
            size_before = self.get_dir_size(yay_dir)
            if not self.dry_run:
                try:
                    subprocess.run(['yay', '-Sc', '--noconfirm'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    size_after = self.get_dir_size(yay_dir)
                    cleaned_size += max(0, size_before - size_after)
                except Exception:
                    pass

        res = {
            "module": "Pacman & Yay Cleaner",
            "status": "Failed" if error_msg and cleaned_size == 0 else "Success",
            "cleaned_mb": cleaned_size / (1024*1024),
            "dry_run": self.dry_run
        }
        if error_msg:
            res["error"] = error_msg
        return res

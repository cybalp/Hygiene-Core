import os

class SymlinkSweeper:
    def __init__(self, config):
        self.config = config
        self.dry_run = self.config.get('dry_run', True)
        self.scan_dirs = self.config.get('symlink_scan_dirs', ['~/.config', '~/.local/bin', '~/.local/share'])

    def run(self):
        cleaned_count = 0
        error_msg = None

        for directory in self.scan_dirs:
            target_dir = os.path.expanduser(directory)
            if not os.path.exists(target_dir):
                continue
            
            try:
                for root, _, files in os.walk(target_dir):
                    for name in files:
                        file_path = os.path.join(root, name)
                        if os.path.islink(file_path):
                            target = os.readlink(file_path)
                            abs_target = target if os.path.isabs(target) else os.path.join(os.path.dirname(file_path), target)
                            if not os.path.exists(abs_target):
                                cleaned_count += 1
                                if not self.dry_run:
                                    try:
                                        os.remove(file_path)
                                    except Exception:
                                        pass
            except Exception as e:
                error_msg = str(e)

        res = {
            "module": f"Symlink Sweeper ({cleaned_count} found)" if cleaned_count > 0 else "Symlink Sweeper",
            "status": "Failed" if error_msg else "Success",
            "dry_run": self.dry_run
        }
        if error_msg: res["error"] = error_msg
        return res

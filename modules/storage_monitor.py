import shutil

class StorageMonitor:
    def __init__(self, config):
        self.config = config
        self.dry_run = self.config.get('dry_run', True)
        self.threshold = self.config.get('storage_alert_threshold_percent', 90)

    def run(self):
        error_msg = None
        
        try:
            total, used, free = shutil.disk_usage("/")
            percent = (used / total) * 100
            if percent >= self.threshold:
                error_msg = f"Root (/) memory usage is critical: {percent:.1f}%!"
        except Exception:
            pass

        return {
            "module": "Storage Monitor",
            "status": "Failed" if error_msg else "Success",
            "error": error_msg if error_msg else "Storage is healthy.",
            "dry_run": self.dry_run
        }

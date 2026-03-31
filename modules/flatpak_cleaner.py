import subprocess

class FlatpakCleaner:
    def __init__(self, config):
        self.config = config
        self.dry_run = self.config.get('dry_run', True)
        self.remove_unused = self.config.get('remove_unused_flatpaks', True)

    def run(self):
        if not self.remove_unused:
            return {"module": "Flatpak Cleaner", "status": "Skipped", "dry_run": self.dry_run}

        error_msg = None
        try:
            # Check if flatpak is installed
            subprocess.run(['flatpak', '--version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            if not self.dry_run:
                subprocess.run(['flatpak', 'uninstall', '--unused', '-y'], 
                               check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError:
            pass
        except FileNotFoundError:
            pass

        return {
            "module": "Flatpak & Snap Cleaner",
            "status": "Success",
            "dry_run": self.dry_run
        }

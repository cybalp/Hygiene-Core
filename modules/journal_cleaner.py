import subprocess

class JournalCleaner:
    def __init__(self, config):
        self.config = config
        self.dry_run = self.config.get('dry_run', True)
        self.max_size = self.config.get('journal_max_size', "200M")

    def run(self):
        error_msg = None
        if not self.dry_run:
            try:
                subprocess.run(['sudo', '-n', 'journalctl', f'--vacuum-size={self.max_size}'], 
                               check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            except subprocess.CalledProcessError:
                error_msg = "Failed to vacuum journal. Root (sudo -n) needed without password."

        res = {
            "module": "Systemd Journal Cleaner",
            "status": "Failed" if error_msg else "Success",
            "dry_run": self.dry_run
        }
        if error_msg:
            res["error"] = error_msg
        return res

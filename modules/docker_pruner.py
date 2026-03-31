import subprocess
import shutil

class DockerPruner:
    def __init__(self, config):
        self.config = config
        self.dry_run = self.config.get('dry_run', True)
        self.prune_volumes = self.config.get('docker_prune_volumes', True)

    def run(self):
        error_msg = None
        cleaned_size = 0

        if shutil.which("docker") is None:
            return {
                "module": "Docker Pruner",
                "status": "Skipped",
                "error": "Docker not installed.",
                "dry_run": self.dry_run
            }

        cmd = ['docker', 'system', 'prune', '-f']
        if self.prune_volumes:
            cmd.append('--volumes')

        if not self.dry_run:
            try:
                output = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode()
                import re
                match = re.search(r"Total reclaimed space: ([0-9.]+) ([KMG]?B)", output)
                if match:
                    val = float(match.group(1))
                    unit = match.group(2)
                    if unit == "MB":
                        cleaned_size = val
                    elif unit == "GB":
                        cleaned_size = val * 1024
                    elif unit == "KB":
                        cleaned_size = val / 1024
                    elif unit == "B":
                        cleaned_size = val / (1024*1024)
            except subprocess.CalledProcessError as e:
                error_msg = f"Docker prune failed. Permissions or daemon issue?"

        res = {
            "module": "Docker Pruner",
            "status": "Failed" if error_msg else "Success",
            "cleaned_mb": cleaned_size,
            "dry_run": self.dry_run
        }
        if error_msg:
            res["error"] = error_msg
        return res

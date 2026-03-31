import subprocess

class OrphanRemover:
    def __init__(self, config):
        self.config = config
        self.dry_run = self.config.get('dry_run', True)
        self.remove_orphans = self.config.get('remove_orphans', True)

    def run(self):
        if not self.remove_orphans:
            return {"module": "Orphan Remover", "status": "Skipped", "dry_run": self.dry_run}
            
        error_msg = None
        # Get orphans
        try:
            output = subprocess.check_output(['pacman', '-Qtdq'], stderr=subprocess.DEVNULL).decode().strip()
            orphans = output.split()
            
            if orphans:
                if not self.dry_run:
                    try:
                        subprocess.run(['sudo', '-n', 'pacman', '-Rns', '--noconfirm'] + orphans, 
                                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
                    except subprocess.CalledProcessError:
                        error_msg = "Root (sudo -n) required for pacman (-Rns) without password."
            
        except subprocess.CalledProcessError:
            # Returns code 1 if no orphans found, perfectly normal
            orphans = []

        res = {
            "module": f"Orphan Remover ({len(orphans)} pkgs)" if orphans else "Orphan Remover",
            "status": "Failed" if error_msg else "Success",
            "dry_run": self.dry_run
        }
        
        if error_msg:
            res["error"] = error_msg
        return res

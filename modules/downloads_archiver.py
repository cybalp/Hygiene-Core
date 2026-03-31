import os
import time
import zipfile

class DownloadsArchiver:
    def __init__(self, config):
        self.config = config
        self.dry_run = self.config.get('dry_run', True)
        self.archive_downloads = self.config.get('archive_downloads', True)
        self.expiry_days = self.config.get('archive_files_older_than_days', 180)
        self.dest = os.path.expanduser(self.config.get('archive_destination', '~/Downloads/Archive'))

    def run(self):
        if not self.archive_downloads:
            return {"module": "Downloads Archiver", "status": "Skipped", "dry_run": self.dry_run}

        downloads_dir = os.path.expanduser('~/Downloads')
        if not os.path.exists(downloads_dir):
            return {"module": "Downloads Archiver", "status": "Success", "dry_run": self.dry_run}

        now = time.time()
        expiry_sec = self.expiry_days * 86400
        archived_count = 0

        if not self.dry_run and not os.path.exists(self.dest):
            try:
                os.makedirs(self.dest)
            except Exception:
                pass
            
        archive_name = os.path.join(self.dest, f"archive_{int(now)}.zip")
        
        files_to_archive = []
        for f in os.listdir(downloads_dir):
            path = os.path.join(downloads_dir, f)
            if path == self.dest or os.path.isdir(path):
                continue
                
            try:
                stat = os.stat(path)
                if (now - stat.st_mtime) > expiry_sec:
                    files_to_archive.append(path)
            except Exception:
                continue

        if files_to_archive:
            if not self.dry_run:
                try:
                    with zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
                        for f in files_to_archive:
                            zipf.write(f, os.path.basename(f))
                            os.remove(f)
                except Exception:
                    pass
            archived_count = len(files_to_archive)

        return {
            "module": f"Downloads Archiver ({archived_count} items)",
            "status": "Success",
            "dry_run": self.dry_run
        }

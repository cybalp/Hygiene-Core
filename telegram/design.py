class ReportDesigner:
    @staticmethod
    def format_size(bytes_size):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_size < 1024:
                return f"{bytes_size:.2f} {unit}"
            bytes_size /= 1024
        return f"{bytes_size:.2f} TB"

    @staticmethod
    def create_markdown(results, version="1.0.0"):
        report = "🧹 *𝗛𝘆𝗴𝗶𝗲𝗻𝗲-𝗖𝗼𝗿𝗲 𝗔𝘂𝘁𝗼 𝗥𝗲𝗽𝗼𝗿𝘁*\n\n"
        report += "‾" * 60 + "\n\n"
        
        for res in results:
            status_icon = "✅" if res.get("status") == "Success" else "❌"
            dry_tag = " [DRY RUN]" if res.get("dry_run") else ""
            
            report += f"{status_icon} *{res['module']}*{dry_tag}\n"
            
            if "cleaned_mb" in res:
                size_str = ReportDesigner.format_size(res['cleaned_mb'] * 1024 * 1024)
                report += f" └ Cleaned: `{size_str}`\n"
            
            if "error" in res:
                report += f" └ Error: `{res['error']}`\n"
        
        report += f"\n*System Optimized. 𝗢𝗞!* `v{version}`"
        return report

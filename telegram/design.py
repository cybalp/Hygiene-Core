class ReportDesigner:
    @staticmethod
    def format_size(bytes_size):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_size < 1024:
                return f"{bytes_size:.2f} {unit}"
            bytes_size /= 1024
        return f"{bytes_size:.2f} TB"

    @staticmethod
    def create_markdown(results):
        is_dry_run = any(res.get("dry_run") for res in results)
        
        report = "🧹 *𝗛𝘆𝗴𝗶𝗲𝗻𝗲-𝗖𝗼𝗿𝗲 𝗔𝘂𝘁𝗼 𝗥𝗲𝗽𝗼𝗿𝘁*\n\n"
        if is_dry_run:
            report += "🛡 *MODE:* `DRY RUN (Safe Trial)`\n"
            
        report += "‾" * 60 + "\n\n"
        
        module_blocks = []
        for res in results:
            status_icon = "✅" if res.get("status") == "Success" else "❌"
            
            block = f"{status_icon} *{res['module']}*"
            
            if "cleaned_mb" in res:
                size_str = ReportDesigner.format_size(res['cleaned_mb'] * 1024 * 1024)
                block += f"\n └ Cleaned: `{size_str}`"
            
            if "error" in res:
                block += f"\n └ Error: `{res['error']}`"
            
            module_blocks.append(block)
            
        report += "\n\n".join(module_blocks) + "\n"
        
        if is_dry_run:
            report += "\n_Scan complete. No files were deleted._"
        else:
            report += "\n*System cleaned. 𝗢𝗞!*"
        return report

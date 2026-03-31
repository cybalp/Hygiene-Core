STRINGS = {
    "en": {
        "help": (
            "🤖 *Hygiene-Core Control Panel*\n\n"
            "🧹 `/clean` — Start cleaning now\n"
            "🛡 `/dryrun_on` — Enable Safe Mode (no files deleted)\n"
            "🧨 `/dryrun_off` — Disable Safe Mode ⚠️ files WILL be deleted\n"
            "⚙️ `/config` — View current settings\n"
            "✏️ `/set key value` — Change a config setting\n"
            "🌐 `/lang en` or `/lang tr` — Change interface language\n\n"
            "*Quick Examples:*\n"
            "`/set interactive_mode true`\n"
            "`/set alert_threshold_mb 500`\n"
            "`/set cache_expiry_days 14`"
        ),
        "clean_start":      "⏳ _Pipeline started. Scanning system..._",
        "dryrun_already_on":  "✔️ Already in Dry Run (Safe) mode.",
        "dryrun_enabled":   "🛡 *Dry Run:* ✅ ENABLED — No files will be deleted.",
        "dryrun_already_off": "🚨 Dry Run is already disabled. Files WILL be deleted on next run.",
        "dryrun_disabled":  "🛡 *Dry Run:* 🚨 DISABLED — Files will be deleted on next run!",
        "config_header":    "⚙️ *Current Configuration*\n\n```yaml\n",
        "set_usage":        "⚠️ Usage: `/set key value`\nExample: `/set interactive_mode true`",
        "set_unknown_key":  "❌ Unknown key: `{key}`\nRun `/config` to see valid keys.",
        "set_success":      "✅ *Config updated! 𝗢𝗞!*\n`{key}`: `{old}` → `{new}`",
        "lang_changed":     "🌐 Language changed to *English*. 𝗢𝗞!",
        "lang_invalid":     "❌ Unknown language. Use `/lang en` or `/lang tr`.",
        "confirm_clean_btn": "🧹 Confirm & Clean All",
        "confirm_clean_start": "⏳ _Running real pipeline. Files will be permanently deleted..._",
    },
    "tr": {
        "help": (
            "🤖 *Hygiene-Core Kontrol Paneli*\n\n"
            "🧹 `/clean` — Temizliği şimdi başlat\n"
            "🛡 `/dryrun_on` — Güvenli Modu Etkinleştir (silme yok)\n"
            "🧨 `/dryrun_off` — Güvenli Modu Devre Dışı Bırak ⚠️ Dosyalar SİLİNECEK\n"
            "⚙️ `/config` — Mevcut ayarları görüntüle\n"
            "✏️ `/set anahtar değer` — Bir ayarı değiştir\n"
            "🌐 `/lang en` veya `/lang tr` — Arayüz dilini değiştir\n\n"
            "*Hızlı Örnekler:*\n"
            "`/set interactive_mode true`\n"
            "`/set alert_threshold_mb 500`\n"
            "`/set cache_expiry_days 14`"
        ),
        "clean_start":      "⏳ _Pipeline başlatıldı. Sistem taranıyor..._",
        "dryrun_already_on":  "✔️ Zaten Güvenli (Dry Run) modasın.",
        "dryrun_enabled":   "🛡 *Dry Run:* ✅ AKTİF — Hiçbir dosya silinmeyecek.",
        "dryrun_already_off": "🚨 Dry Run zaten kapalı. Bir sonraki çalıştırmada dosyalar SİLİNECEK.",
        "dryrun_disabled":  "🛡 *Dry Run:* 🚨 KAPALI — Dosyalar bir sonraki çalıştırmada silinecek!",
        "config_header":    "⚙️ *Mevcut Yapılandırma*\n\n```yaml\n",
        "set_usage":        "⚠️ Kullanım: `/set anahtar değer`\nÖrnek: `/set interactive_mode true`",
        "set_unknown_key":  "❌ Bilinmeyen anahtar: `{key}`\nGeçerli anahtarları görmek için `/config` çalıştır.",
        "set_success":      "✅ *Ayar güncellendi! 𝗢𝗞!*\n`{key}`: `{old}` → `{new}`",
        "lang_changed":     "🌐 Dil *Türkçe* olarak değiştirildi. 𝗢𝗞!",
        "lang_invalid":     "❌ Bilinmeyen dil. `/lang en` veya `/lang tr` kullanın.",
        "confirm_clean_btn": "🧹 Onayla & Hepsini Temizle",
        "confirm_clean_start": "⏳ _Gerçek pipeline çalışıyor. Dosyalar kalıcı olarak silinecek..._",
    }
}

def t(config: dict, msg_id: str, **kwargs) -> str:
    """Translate a message ID based on the current language in config."""
    lang = config.get("lang", "en")
    if lang not in STRINGS:
        lang = "en"
    text = STRINGS[lang].get(msg_id, STRINGS["en"].get(msg_id, msg_id))
    return text.format(**kwargs) if kwargs else text

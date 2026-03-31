#!/usr/bin/env python3
import os
import yaml
import telebot
from pathlib import Path
from dotenv import load_dotenv

from system.orchestrator import Orchestrator
from telegram.design import ReportDesigner
from telegram.locales import t

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not BOT_TOKEN or not CHAT_ID:
    print("TELEGRAM_TOKEN or CHAT_ID missing from .env")
    exit(1)

bot = telebot.TeleBot(BOT_TOKEN)

# ──────────────────────────── Config Helpers ────────────────────────────

def load_config():
    config_path = BASE_DIR / "config.yaml"
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def save_config(config_data):
    config_path = BASE_DIR / "config.yaml"
    with open(config_path, 'w') as f:
        yaml.safe_dump(config_data, f, sort_keys=False)

def is_authorized(message):
    return str(message.chat.id) == str(CHAT_ID)

def parse_value(raw):
    """Auto-cast strings to proper Python types."""
    if raw.lower() == 'true':  return True
    if raw.lower() == 'false': return False
    try: return int(raw)
    except ValueError: pass
    try: return float(raw)
    except ValueError: pass
    return raw

# ──────────────────────────── Commands ────────────────────────────

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    if not is_authorized(message): return
    config = load_config()
    bot.send_message(message.chat.id, t(config, "help"), parse_mode="Markdown")

@bot.message_handler(commands=['clean'])
def run_clean(message):
    if not is_authorized(message): return
    config = load_config()
    bot.send_message(message.chat.id, t(config, "clean_start"), parse_mode="Markdown")

    orchestrator = Orchestrator()
    results = orchestrator.run_pipeline()
    report = ReportDesigner.create_markdown(results)
    bot.send_message(message.chat.id, report, parse_mode="Markdown")

@bot.message_handler(commands=['dryrun_on'])
def enable_dryrun(message):
    if not is_authorized(message): return
    config = load_config()
    if config.get("dry_run", True):
        bot.send_message(message.chat.id, t(config, "dryrun_already_on"))
        return
    config["dry_run"] = True
    save_config(config)
    bot.send_message(message.chat.id, t(config, "dryrun_enabled"), parse_mode="Markdown")

@bot.message_handler(commands=['dryrun_off'])
def disable_dryrun(message):
    if not is_authorized(message): return
    config = load_config()
    if not config.get("dry_run", True):
        bot.send_message(message.chat.id, t(config, "dryrun_already_off"))
        return
    config["dry_run"] = False
    save_config(config)
    bot.send_message(message.chat.id, t(config, "dryrun_disabled"), parse_mode="Markdown")

@bot.message_handler(commands=['config'])
def show_config(message):
    if not is_authorized(message): return
    config = load_config()
    text = t(config, "config_header")
    text += yaml.safe_dump(config, sort_keys=False)
    text += "\n```"
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(commands=['set'])
def set_config(message):
    if not is_authorized(message): return
    config = load_config()
    parts = message.text.strip().split(maxsplit=2)
    if len(parts) < 3:
        bot.send_message(message.chat.id, t(config, "set_usage"), parse_mode="Markdown")
        return

    key   = parts[1]
    value = parse_value(parts[2])

    if key not in config:
        bot.send_message(message.chat.id, t(config, "set_unknown_key", key=key), parse_mode="Markdown")
        return

    old = config[key]
    config[key] = value
    save_config(config)
    bot.send_message(message.chat.id, t(config, "set_success", key=key, old=old, new=value), parse_mode="Markdown")

@bot.message_handler(commands=['lang'])
def set_language(message):
    if not is_authorized(message): return
    config = load_config()
    parts = message.text.strip().split()
    if len(parts) < 2 or parts[1].lower() not in ("en", "tr"):
        bot.send_message(message.chat.id, t(config, "lang_invalid"), parse_mode="Markdown")
        return

    lang = parts[1].lower()
    config["lang"] = lang
    save_config(config)
    bot.send_message(message.chat.id, t(config, "lang_changed"), parse_mode="Markdown")

# ──────────────────────────── Callbacks ────────────────────────────

@bot.callback_query_handler(func=lambda call: call.data == "confirm_clean_all")
def callback_confirm_clean(call):
    if not is_authorized(call.message): return
    config = load_config()
    bot.edit_message_text(
        t(config, "confirm_clean_start"),
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        parse_mode="Markdown"
    )
    orchestrator = Orchestrator()
    orchestrator.config["dry_run"] = False
    results = orchestrator.run_pipeline()
    report = ReportDesigner.create_markdown(results)
    bot.edit_message_text(report, chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode="Markdown")

if __name__ == "__main__":
    print("Bot is listening...")
    bot.infinity_polling()

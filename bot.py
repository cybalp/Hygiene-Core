#!/usr/bin/env python3
import os
import yaml
import telebot
from pathlib import Path
from dotenv import load_dotenv

from system.orchestrator import Orchestrator
from telegram.design import ReportDesigner

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not BOT_TOKEN or not CHAT_ID:
    print("TELEGRAM_TOKEN or CHAT_ID missing from .env")
    exit(1)

bot = telebot.TeleBot(BOT_TOKEN)

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

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    if not is_authorized(message): return
    text = (
        "🤖 *Hygiene-Core Control Panel*\n\n"
        "🧹 `/clean` - Start cleaning process now\n"
        "🛡 `/dryrun_on` - Enable Test Mode (No delete)\n"
        "🧨 `/dryrun_off` - Disable Test Mode (DANGER!)\n"
        "⚙️ `/config` - View current settings\n"
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(commands=['clean'])
def run_clean(message):
    if not is_authorized(message): return
    bot.send_message(message.chat.id, "⏳ _Hygiene-Core started. Running pipeline..._", parse_mode="Markdown")
    
    orchestrator = Orchestrator()
    results = orchestrator.run_pipeline()
    report = ReportDesigner.create_markdown(results)
    
    bot.send_message(message.chat.id, report, parse_mode="Markdown")

@bot.message_handler(commands=['dryrun_on'])
def enable_dryrun(message):
    if not is_authorized(message): return
    config = load_config()
    if config.get("dry_run", True):
        bot.send_message(message.chat.id, "Zaten Dry Run modundasın ✔️")
        return
        
    config["dry_run"] = True
    save_config(config)
    bot.send_message(message.chat.id, "🛡 *Dry Run is now:* ✅ ENABLED (Safe Mode)", parse_mode="Markdown")

@bot.message_handler(commands=['dryrun_off'])
def disable_dryrun(message):
    if not is_authorized(message): return
    config = load_config()
    if not config.get("dry_run", True):
        bot.send_message(message.chat.id, "Zaten Dry Run modun kapalı (Tehlike modu) 🚨")
        return
        
    config["dry_run"] = False
    save_config(config)
    bot.send_message(message.chat.id, "🛡 *Dry Run is now:* 🚨 DISABLED (Danger Mode, files will be deleted!)", parse_mode="Markdown")

@bot.message_handler(commands=['config'])
def show_config(message):
    if not is_authorized(message): return
    config = load_config()
    text = "⚙️ *Current Configuration*\n\n```yaml\n"
    text += yaml.safe_dump(config, sort_keys=False)
    text += "\n```"
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "confirm_clean_all")
def callback_confirm_clean(call):
    if not is_authorized(call.message): return
    bot.edit_message_text("⏳ _Hygiene-Core started. Running real pipeline..._", chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode="Markdown")
    
    orchestrator = Orchestrator()
    orchestrator.config["dry_run"] = False
    results = orchestrator.run_pipeline()
    
    report = ReportDesigner.create_markdown(results)
    bot.edit_message_text(report, chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode="Markdown")

if __name__ == "__main__":
    print("Bot is listening...")
    bot.infinity_polling()

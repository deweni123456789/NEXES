#!/usr/bin/env python3
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup
import os
import re
from modules.downloader import download_facebook_video
from modules.buttons import make_uploaded_keyboard, make_start_keyboard

# Load config from env
API_ID = int(os.environ.get("API_ID", "0"))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
BOT_USERNAME = os.environ.get("BOT_USERNAME", "YourBotUsername")  # without @

if not BOT_TOKEN or API_ID == 0 or not API_HASH:
    raise SystemExit("❌ Please set API_ID, API_HASH and BOT_TOKEN environment variables (see README).")

app = Client(
    "fb_downloader_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    parse_mode="html"
)

# Start command
@app.on_message(filters.command("start") & filters.private)
async def start_cmd(c, m):
    text = "👋 Send me a Facebook video link (post / reel / story) and I'll try to download it."
    await m.reply_text(text, reply_markup=make_start_keyboard(BOT_USERNAME), quote=True)

# URL handler (fixed for Pyrogram v2)
@app.on_message(filters.private & ~filters.command(["start", "help"]))
async def url_handler(c, m):
    urls = re.findall(r'(https?://\S+)', m.text or "")
    if not urls:
        return await m.reply_text("⚠️ Please send a valid Facebook video link.")
    url = urls[0]

    msg = await m.reply_text("🔎 Fetching video info...", quote=True)
    try:
        info = await download_facebook_video(url, m.from_user.id)
    except Exception as e:
        await msg.edit(f"❌ Failed: <code>{e}</code>")
        return

    if info.get("error"):
        await msg.edit(f"❌ {info['error']}")
        return

    await msg.edit("⬇️ Downloading video...")
    path = info.get("filepath")
    title = info.get("title", "facebook_video")

    try:
        caption = f"{title}\n\nDownloaded from: {url}"
        uploading = await m.reply_text("📤 Uploading to Telegram...", quote=True)
        await m.reply_document(path, caption=caption, reply_markup=make_uploaded_keyboard(BOT_USERNAME))
        await uploading.delete()
        await msg.delete()
    except Exception as e:
        await msg.edit(f"❌ Upload failed: <code>{e}</code>")
    finally:
        try:
            os.remove(path)
        except:
            pass

# Help command
@app.on_message(filters.command("help") & filters.private)
async def help_cmd(c, m):
    await m.reply_text("📥 Send a Facebook video link and I’ll download it.\n\n⚠️ Note: Big videos may exceed Telegram’s upload limits.", quote=True)

if __name__ == '__main__':
    print("🚀 Bot starting...")
    app.run()

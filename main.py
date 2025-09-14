import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ParseMode

from modules.downloader import download_facebook_video
from modules.instagram import download_instagram_video
from modules.adult import download_adult_video
from modules.buttons import make_start_keyboard

# ==================================================
# Config
# ==================================================
API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
BOT_USERNAME = os.environ.get("BOT_USERNAME", "fb_insta_downloader_bot")

if not all([API_ID, API_HASH, BOT_TOKEN]):
    raise SystemExit("❌ Please set API_ID, API_HASH and BOT_TOKEN environment variables (see README).")

app = Client(
    "fb_insta_downloader",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ==================================================
# Start Command
# ==================================================
@app.on_message(filters.command("start") & filters.private)
async def start_cmd(client: Client, m: Message):
    text = (
        "👋 Hello!\n\n"
        "📥 Send me a **Facebook**, **Instagram**, or **Adult site** video link "
        "and I’ll download it for you."
    )
    await m.reply_text(
        text,
        reply_markup=make_start_keyboard(BOT_USERNAME),
        parse_mode=ParseMode.HTML
    )

# ==================================================
# Facebook Handler
# ==================================================
@app.on_message(filters.private & filters.regex(r"(https?://(www\.)?(facebook\.com|fb\.watch)[^\s]+)"))
async def fb_handler(client: Client, m: Message):
    url = m.matches[0].group(1)
    msg = await m.reply_text("🔎 Fetching Facebook video...", quote=True)

    result = await download_facebook_video(url, m.from_user.id)
    if "error" in result:
        return await msg.edit_text(f"❌ Error: {result['error']}")

    filepath = result["filepath"]
    title = result["title"]

    await msg.edit_text("⬆️ Uploading video to Telegram...")
    await m.reply_video(video=filepath, caption=f"📥 {title}")
    os.remove(filepath)

# ==================================================
# Instagram Handler
# ==================================================
@app.on_message(filters.private & filters.regex(r"(https?://(www\.)?(instagram\.com|instagr\.am)[^\s]+)"))
async def insta_handler(client: Client, m: Message):
    url = m.matches[0].group(1)
    msg = await m.reply_text("🔎 Fetching Instagram video...", quote=True)

    result = await download_instagram_video(url, m.from_user.id)
    if "error" in result:
        return await msg.edit_text(f"❌ Error: {result['error']}")

    filepath = result["filepath"]
    title = result["title"]

    await msg.edit_text("⬆️ Uploading video to Telegram...")
    await m.reply_video(video=filepath, caption=f"📥 {title}")
    os.remove(filepath)

# ==================================================
# Adult Sites Handler
# ==================================================
@app.on_message(filters.private & filters.regex(r"(https?://(www\.)?(pornhub\.com|xvideos\.com|xhamster\.com|xnxx\.com)[^\s]+)"))
async def adult_handler(client: Client, m: Message):
    url = m.matches[0].group(1)
    msg = await m.reply_text("🔎 Fetching video...", quote=True)

    result = await download_adult_video(url, m.from_user.id)
    if "error" in result:
        return await msg.edit_text(f"❌ Error: {result['error']}")

    filepath = result["filepath"]
    title = result["title"]

    await msg.edit_text("⬆️ Uploading video to Telegram...")
    await m.reply_video(video=filepath, caption=f"📥 {title}")
    os.remove(filepath)

# ==================================================
# Run Bot
# ==================================================
print("🚀 Bot starting...")
app.run()

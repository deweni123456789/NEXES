import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import API_ID, API_HASH, BOT_TOKEN, BOT_USERNAME
from utils.keyboard import make_start_keyboard

# Initialize bot
app = Client(
    "fb_insta_downloader",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Import modules after app creation
import modules.facebook
import modules.instagram

# Start command
@app.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):
    text = (
        "👋 Hello! I can help you download videos from:\n\n"
        "📘 Facebook\n"
        "📸 Instagram\n\n"
        "Just send me a video link to get started."
    )
    keyboard = make_start_keyboard(bot_username=BOT_USERNAME)
    await message.reply_text(text, reply_markup=keyboard)

if __name__ == "__main__":
    print("🚀 Bot starting...")
    app.run()

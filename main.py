import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import API_ID, API_HASH, BOT_TOKEN, BOT_USERNAME

# Import modules manually
from modules import facebook, instagram

# Initialize bot
app = Client(
    "fb_insta_downloader",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Start command
@app.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):
    text = (
        "👋 Hello! I can help you download videos from:\n\n"
        "📘 Facebook\n"
        "📸 Instagram\n\n"
        "Just send me a video link to get started."
    )
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/deweni2"),
            InlineKeyboardButton("💬 Support", url="https://t.me/slmusicmania"),
        ],
        [
            InlineKeyboardButton("📩 Contact Bot", url=f"https://t.me/{BOT_USERNAME}")
        ]
    ])
    await message.reply_text(text, reply_markup=keyboard)

if __name__ == "__main__":
    print("🚀 Bot starting...")
    app.run()

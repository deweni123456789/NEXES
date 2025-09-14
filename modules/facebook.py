from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.downloader import run_ytdlp
import os

@Client.on_message(filters.private & filters.regex(r"https?://(www\.)?(facebook\.com|fb\.watch)/[^\s]+"))
async def fb_handler(client, message):
    url = message.text.strip()
    msg = await message.reply_text("🔎 Fetching Facebook video...")

    try:
        result = await run_ytdlp(url, message.from_user.id)
    except Exception as e:
        return await msg.edit_text(f"❌ Unexpected error: {str(e)}")

    if "error" in result:
        return await msg.edit_text(f"❌ Error: {result['error']}")

    filepath = result["filepath"]
    title = result["title"]

    # Check if file exists
    if not os.path.exists(filepath):
        return await msg.edit_text("❌ Error: Video file not found after download.")

    await msg.edit_text("⬆️ Uploading video...")
    try:
        await message.reply_video(
            video=filepath,
            caption=f"🎬 {title}",
            reply_markup=InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/deweni2"),
                    InlineKeyboardButton("💬 Support", url="https://t.me/slmusicmania"),
                ]]
            )
        )
    except Exception as e:
        await msg.edit_text(f"❌ Upload failed: {str(e)}")
        return

    await msg.delete()

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.downloader import run_ytdlp

@Client.on_message(filters.private & filters.regex(r"(https?://(www\.)?(facebook\.com|fb\.watch)[^\s]+)"))
async def fb_handler(client, message):
    url = message.text.strip()
    msg = await message.reply_text("🔎 Fetching Facebook video...")

    result = await run_ytdlp(url, message.from_user.id)
    if "error" in result:
        return await msg.edit_text(f"❌ Error: {result['error']}")

    filepath = result["filepath"]
    title = result["title"]

    await msg.edit_text("⬆️ Uploading video...")
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
    await msg.delete()

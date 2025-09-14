from pyrogram import filters
from utils.downloader import run_ytdlp
from utils.keyboard import make_uploaded_keyboard
import os
from main import app

@app.on_message(filters.private & filters.regex(r"https?://(www\.)?(facebook\.com|fb\.watch)/[^\s]+"))
async def fb_handler(client, message):
    url = message.text.strip()
    msg = await message.reply_text("🔎 Fetching Facebook video...")

    result = await run_ytdlp(url, message.from_user.id)
    if "error" in result:
        return await msg.edit_text(f"❌ Error: {result['error']}")

    filepath = result["filepath"]
    title = result["title"]

    if not os.path.exists(filepath):
        return await msg.edit_text("❌ Error: Video file not found after download.")

    await msg.edit_text("⬆️ Uploading video...")

    buttons = make_uploaded_keyboard(bot_username=client.me.username)

    try:
        await message.reply_video(video=filepath, caption=f"🎬 {title}", reply_markup=buttons)
    except Exception as e:
        await msg.edit_text(f"❌ Upload failed: {str(e)}")
        return

    await msg.delete()

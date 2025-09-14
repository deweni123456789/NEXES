from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def make_uploaded_keyboard(bot_username: str):
    developer = InlineKeyboardButton(text="👨‍💻 Developer", url="https://t.me/deweni2")
    support = InlineKeyboardButton(text="💬 Support Group", url="https://t.me/slmusicmania")
    contact = InlineKeyboardButton(text="📩 Contact Bot", url=f"https://t.me/{bot_username}")
    return InlineKeyboardMarkup([[developer, support, contact]])  # all buttons in one row

def make_start_keyboard(bot_username: str):
    return make_uploaded_keyboard(bot_username)

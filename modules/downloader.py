import yt_dlp
import asyncio
import os
import re
from typing import Dict

OUTDIR = "/tmp"

async def download_facebook_video(url: str, user_id: int) -> Dict:
    """
    Download Facebook video using yt-dlp without requiring FFmpeg.
    Returns a dict with keys: filepath, title OR error.
    """
    # sanitize filename
    def slug(s):
        return re.sub(r'[^\\w\\-\\. ]', '_', s)[:120]

    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, _download_sync, url, slug)

def _download_sync(url, slugfn):
    # Use 'best' format to avoid needing ffmpeg
    ydl_opts = {
        "format": "best",  # single file, no merging
        "outtmpl": os.path.join(OUTDIR, "%(title)s.%(ext)s"),
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filepath = ydl.prepare_filename(info)
            title = info.get("title") or "facebook_video"
            return {"filepath": filepath, "title": title}
    except Exception as e:
        return {"error": str(e)}

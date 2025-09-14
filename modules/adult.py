import yt_dlp
import asyncio
import os
import re
from typing import Dict

OUTDIR = "/tmp"

async def download_adult_video(url: str, user_id: int) -> Dict:
    """
    Download adult site video using yt-dlp (no FFmpeg required).
    Returns dict: {filepath, title} or {error}.
    """
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, _download_sync, url)

def _download_sync(url):
    ydl_opts = {
        "format": "best",  # avoids ffmpeg merging
        "outtmpl": os.path.join(OUTDIR, "%(title)s.%(ext)s"),
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filepath = ydl.prepare_filename(info)
            title = info.get("title") or "adult_video"
            return {"filepath": filepath, "title": title}
    except Exception as e:
        return {"error": str(e)}

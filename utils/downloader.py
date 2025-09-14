import os
import asyncio
import yt_dlp

async def run_ytdlp(url: str, user_id: int):
    download_dir = f"downloads/{user_id}"
    os.makedirs(download_dir, exist_ok=True)

    ydl_opts = {
        "outtmpl": f"{download_dir}/%(title).80s.%(ext)s",
        "format": "best[ext=mp4]/best",
        "merge_output_format": "mp4",
        "noplaylist": True,
        "quiet": True,
        "nocheckcertificate": True,
    }

    loop = asyncio.get_event_loop()
    try:
        return await loop.run_in_executor(None, lambda: _download(url, ydl_opts))
    except Exception as e:
        return {"error": str(e)}

def _download(url, ydl_opts):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filepath = ydl.prepare_filename(info)
        return {"filepath": filepath, "title": info.get("title", "Video")}

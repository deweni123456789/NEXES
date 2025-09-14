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
        "nocheckcertificate": True,
        "quiet": False,  # Show logs for debugging
        "verbose": True,
    }

    loop = asyncio.get_event_loop()
    try:
        return await loop.run_in_executor(None, lambda: _download(url, ydl_opts))
    except Exception as e:
        return {"error": str(e)}

def _download(url, ydl_opts):
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filepath = ydl.prepare_filename(info)

            size_mb = os.path.getsize(filepath) / 1024 / 1024
            print(f"[DOWNLOADER] Video downloaded: {filepath} ({size_mb:.2f} MB)")

            # Telegram limit check
            if size_mb > 2000:
                return {"error": f"Video too large ({size_mb:.2f} MB) for Telegram upload."}

            return {"filepath": filepath, "title": info.get("title", "Video")}
    except Exception as e:
        print(f"[DOWNLOADER ERROR] {str(e)}")
        return {"error": str(e)}

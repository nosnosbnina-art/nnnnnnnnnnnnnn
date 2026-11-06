import json
import os
import sys
import time
import urllib.request
from pathlib import Path

MODEL = "fal-ai/kling-video/v2.5-turbo/pro/text-to-video"
BASE = "https://queue.fal.run/" + MODEL
PROMPT = os.environ.get("VIDEO_PROMPT", "").strip()
if not PROMPT and Path("/tmp/video-prompt.txt").exists():
    PROMPT = Path("/tmp/video-prompt.txt").read_text(encoding="utf-8").strip()
DURATION = os.environ.get("VIDEO_DURATION", "5")
ASPECT = os.environ.get("VIDEO_ASPECT", "9:16")
KEY = os.environ.get("FAL_KEY", "").strip()

if not KEY:
    sys.exit("Missing FAL_KEY. Add it in GitHub: Settings > Secrets and variables > Actions.")
if not PROMPT:
    sys.exit("The video prompt is empty.")

def request(url, method="GET", payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(
        url, data=data, method=method,
        headers={"Authorization": f"Key {KEY}", "Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=90) as response:
        body = response.read()
        return json.loads(body) if body else {}

print("Submitting video generation request to fal.ai / Kling 2.5 Turbo Pro...")
job = request(BASE, "POST", {
    "prompt": PROMPT,
    "duration": DURATION,
    "aspect_ratio": ASPECT,
    "negative_prompt": "blurry, low quality, distorted buildings, malformed people, text, subtitles, logos"
})
status_url = job.get("status_url")
response_url = job.get("response_url")
if not status_url or not response_url:
    raise RuntimeError("The provider did not return queue status/response URLs: " + json.dumps(job))

deadline = time.time() + 30 * 60
while time.time() < deadline:
    status = request(status_url)
    state = status.get("status")
    print("Generation status:", state)
    if state == "COMPLETED":
        result = request(response_url)
        video_url = (result.get("video") or {}).get("url")
        if not video_url:
            raise RuntimeError("Generation completed but no video URL was returned: " + json.dumps(result))
        Path("output").mkdir(exist_ok=True)
        req = urllib.request.Request(video_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=180) as response:
            Path("output/floodstorm-video.mp4").write_bytes(response.read())
        print("Video saved to output/floodstorm-video.mp4")
        break
    if state in ("FAILED", "CANCELLED"):
        raise RuntimeError("Video generation failed: " + json.dumps(status))
    time.sleep(15)
else:
    raise TimeoutError("Video generation did not finish within 30 minutes.")

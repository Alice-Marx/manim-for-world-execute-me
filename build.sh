#!/usr/bin/env bash
# Render the MV and optionally mux licensed audio.
# Usage:
#   ./build.sh [-ql|-qm|-qh|-qk]          # default -qh = 1080p60
#   AUDIO=./audio/song.mp3 ./build.sh     # mux your own licensed track
#
# Outputs land in ./out/ (created if missing). Audio is NEVER shipped with this repo.
set -euo pipefail
cd "$(dirname "$0")"
Q="${1:--qh}"

if [ ! -x .venv/bin/manim ]; then
  echo "Missing .venv — create it first:" >&2
  echo "  python3 -m venv .venv && .venv/bin/pip install -r requirements.txt" >&2
  exit 1
fi

.venv/bin/manim "$Q" --disable_caching --media_dir media scenes/world_execute_me.py WorldExecuteMe

case "$Q" in
  -ql) R=480p15 ;;
  -qm) R=720p30 ;;
  -qh) R=1080p60 ;;
  -qk) R=2160p60 ;;
  *)   echo "Unknown quality flag: $Q (use -ql|-qm|-qh|-qk)" >&2; exit 1 ;;
esac

VID="media/videos/world_execute_me/$R/WorldExecuteMe.mp4"
if [ ! -f "$VID" ]; then
  echo "Render output not found: $VID" >&2
  exit 1
fi

mkdir -p out
cp "$VID" out/world-execute-me-manim-silent.mp4

# Prefer AUDIO=…, else ./audio/world-execute-me.mp3 if the user placed one there
AUDIO="${AUDIO:-}"
if [ -z "$AUDIO" ] && [ -f audio/world-execute-me.mp3 ]; then
  AUDIO="audio/world-execute-me.mp3"
fi

if [ -n "${AUDIO}" ] && [ -f "$AUDIO" ]; then
  ffmpeg -y -v error -i "$VID" -i "$AUDIO" \
    -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 192k -shortest \
    -movflags +faststart out/world-execute-me-manim.mp4
  echo "Muxed → out/world-execute-me-manim.mp4 (with audio from $AUDIO)"
else
  cp "$VID" out/world-execute-me-manim.mp4
  echo "No audio found. Wrote silent copy → out/world-execute-me-manim.mp4"
  echo "Place a licensed mp3 at audio/world-execute-me.mp3 or set AUDIO=/path/to.mp3"
fi

ffprobe -v error -show_entries format=duration -of csv=p=0 out/world-execute-me-manim.mp4

#!/usr/bin/env bash
# Usage: ./render.sh N Short_Title   -> videos/NN_Short_Title.mp4
set -euo pipefail
N="$1"; NAME="$2"
cd "$(dirname "$0")"
mkdir -p videos build
NN=$(printf "%02d" "$N")
python3 "episodes/ep${N}_audio.py" "build/ep${N}.wav" &
python3 "episodes/ep${N}.py" "build/ep${N}_video.mp4"
wait
ffmpeg -y -loglevel error -i "build/ep${N}_video.mp4" -i "build/ep${N}.wav" \
  -c:v copy -c:a aac -b:a 160k -shortest "videos/${NN}_${NAME}.mp4"
ffprobe -v error -show_entries format=duration -of csv=p=0 "videos/${NN}_${NAME}.mp4"

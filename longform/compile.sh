#!/usr/bin/env bash
# Weekly long-form film: re-render episodes FIRST..LAST, trim title / TO-BE-CONTINUED cards,
# reframe the vertical footage to 1920x1080 over a blurred copy of itself, add chapter cards,
# and write longform/out/<NAME>.mp4 plus <NAME>_chapters.txt (YouTube chapter timestamps).
#
# Usage: longform/compile.sh FIRST LAST "Film_Name" "Intro title" "Intro subtitle"
#   e.g. longform/compile.sh 8 21 Week2_Full_Movie "The Egg + The Frozen North" "Episodes 8-21"
# Env: FORCE=1 re-renders episodes even if build/ files exist.
#
# Episode windows: variant-A episodes (title card first) start at 2.0s, variant-B (cold open)
# start at 0; every episode ends at its END_T (the cliffhanger frame, before the TBC card).
set -euo pipefail
cd "$(dirname "$0")/.."

FIRST="${1:?first episode}"; LAST="${2:?last episode}"
NAME="${3:-Week_Film}"
INTRO1="${4:-Fridge Kingdom}"
INTRO2="${5:-}"

mkdir -p build/lf longform/out
OUT="longform/out/${NAME}.mp4"
CHAPTERS="longform/out/${NAME}_chapters.txt"

# Titles come from the bible's episode log (2nd column).
title_of() { awk -F'|' -v n="$1" '$2+0==n && $2 ~ /[0-9]/ {gsub(/^ +| +$/,"",$3); print $3; exit}' story/bible.md; }
const_of() { grep -h -E "^$2 *=" "episodes/ep$1.py" | head -1 | sed -E "s/^[A-Z_]+ *= *([0-9.]+).*/\1/"; }

VF=(-r 30 -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p)
AF=(-c:a aac -b:a 160k -ar 48000 -ac 2)

card() {  # card OUT.mp4 SECONDS KIND lines...
  local out="$1" dur="$2"; shift 2
  python3 longform/chapter_card.py "build/lf/_card.png" "$@"
  ffmpeg -y -loglevel error -loop 1 -t "$dur" -i build/lf/_card.png \
    -f lavfi -t "$dur" -i "anoisesrc=d=${dur}:c=pink:a=0.25,lowpass=f=900,afade=t=in:d=0.2,afade=t=out:st=0.25:d=0.35,volume=0.6" \
    -vf "fade=t=in:d=0.3,fade=t=out:st=$(python3 -c "print($dur-0.3)"):d=0.3,format=yuv420p" \
    "${VF[@]}" "${AF[@]}" -shortest "$out"
}

SEGS=()
: > "$CHAPTERS"
T=0
add_seg() {  # add_seg FILE [chapter label]
  local d
  d=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$1")
  if [ -n "${2:-}" ]; then
    printf "%d:%02d %s\n" $((${T%.*}/60)) $((${T%.*}%60)) "$2" >> "$CHAPTERS"
  fi
  T=$(python3 -c "print($T+$d)")
  SEGS+=("$1")
}

# --- intro ---
card build/lf/intro.mp4 3.5 intro "$INTRO1" "$INTRO2"
add_seg build/lf/intro.mp4 "Intro"

for N in $(seq "$FIRST" "$LAST"); do
  TITLE="$(title_of "$N")"
  END_T="$(const_of "$N" END_T)"
  START="$(const_of "$N" T_START || true)"
  [ -z "$START" ] && START=0
  # Older episodes (9, 11) define the 2.0s title card inline rather than as T_START.
  if [ "$START" = "0" ] && grep -q -E "^\| *$N *\|.*variant A" story/bible.md; then START=2.0; fi

  if [ "${FORCE:-0}" = "1" ] || [ ! -f "build/ep${N}_video.mp4" ] || [ ! -f "build/ep${N}.wav" ]; then
    echo "Rendering Ep $N ($TITLE)..."
    python3 "episodes/ep${N}_audio.py" "build/ep${N}.wav" &
    python3 "episodes/ep${N}.py" "build/ep${N}_video.mp4"
    wait
  fi

  card "build/lf/ch${N}.mp4" 2.2 chapter "CHAPTER $((N-FIRST+1)) · EPISODE $N" "$TITLE"
  add_seg "build/lf/ch${N}.mp4" "Ep $N: $TITLE"

  DUR=$(python3 -c "print($END_T-$START)")
  ffmpeg -y -loglevel error -ss "$START" -t "$DUR" -i "build/ep${N}_video.mp4" \
    -ss "$START" -t "$DUR" -i "build/ep${N}.wav" \
    -filter_complex "[0:v]split[a][b];[a]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,boxblur=50:6,eq=brightness=-0.12:saturation=1.1[bg];[b]scale=-2:1080[fg];[bg][fg]overlay=(W-w)/2:0,format=yuv420p[v];[1:a]aresample=48000,aformat=channel_layouts=stereo,afade=t=in:d=0.04,afade=t=out:st=$(python3 -c "print($DUR-0.2)"):d=0.2[a]" \
    -map "[v]" -map "[a]" "${VF[@]}" "${AF[@]}" "build/lf/ep${N}.mp4"
  add_seg "build/lf/ep${N}.mp4"
done

# --- outro ---
card build/lf/outro.mp4 5 end "New episodes every day" "Subscribe so you don't miss Week 3"
add_seg build/lf/outro.mp4 "To be continued..."

: > build/lf/list.txt
for s in "${SEGS[@]}"; do echo "file '$(basename "$s")'" >> build/lf/list.txt; done
# Final pass: limiter (AAC can overshoot 0 dB) and a size-friendly encode (<100 MB so GitHub/Metricool can host it).
ffmpeg -y -loglevel error -f concat -safe 0 -i build/lf/list.txt \
  -af "alimiter=limit=0.8:level=disabled" -c:v libx264 -preset veryfast -crf 25 -pix_fmt yuv420p -r 30 \
  -c:a aac -b:a 160k -ar 48000 -ac 2 -movflags +faststart "$OUT"

echo "Wrote $OUT ($(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT")s)"
echo "Chapters in $CHAPTERS:"; cat "$CHAPTERS"

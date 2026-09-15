#!/usr/bin/env bash
# ELMA (bolum 08 onizleme) tam render montaji - YERELDE.
# 15 Eyl 2026. Actions 8 sessiz parca uretir; ses burada eklenir, cunku
# muzik depoya girmiyor (bkz. .gitignore) ve montaj kurali yerel ffmpeg.
set -eu
cd "$(dirname "$0")/.."
RUN="${1:?kullanim: elma-montaj.sh <actions-run-id>}"
OLCU=64
BPM=132.5
SURE=$(python -c "print(f'{$OLCU*(60/$BPM)*4:.6f}')")
IND="04-ciktilar/elma-parca"
if [ "${ATLA_INDIR:-0}" != "1" ]; then rm -rf "$IND"; fi
mkdir -p "$IND"
[ "${ATLA_INDIR:-0}" = "1" ] || gh run download "$RUN" -D "$IND" -p "parca-*"
find "$IND" -name 'parca-*.mp4' -printf '%f %p\n' | sort | awk '{print $2}' > "$IND/_sirali.txt"
cat "$IND/_sirali.txt"
: > "$IND/liste.txt"
while read -r f; do printf "file '%s'\n" "$(cygpath -m "$(cd "$(dirname "$f")" && pwd)/$(basename "$f")")" >> "$IND/liste.txt"; done < "$IND/_sirali.txt"
# Parcalar ayni kodlama parametreleriyle uretildi -> yeniden kodlama yok.
ffmpeg -v error -y -f concat -safe 0 -i "$IND/liste.txt" -c copy "$IND/govde.mp4"
ffmpeg -v error -y -i "$IND/govde.mp4" -i "01-muzik/subterranean-pulse-336olcu.wav" \
  -map 0:v:0 -map 1:a:0 -t "$SURE" -c:v copy -c:a aac -b:a 192k \
  "04-ciktilar/elma-tam.mp4"
echo "--- dogrulama ---"
ffprobe -v error -show_entries format=duration -of default=nw=1 "04-ciktilar/elma-tam.mp4"
echo "beklenen sure: $SURE sn"
ffmpeg -v error -xerror -i "04-ciktilar/elma-tam.mp4" -f null - && echo "TAM DECODE: TEMIZ"
ls -lh "04-ciktilar/elma-tam.mp4"

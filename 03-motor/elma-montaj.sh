#!/usr/bin/env bash
# ELMA bolumu montaji - YERELDE.
# Actions sessiz parca uretir (muzik depoya girmiyor; bkz. .gitignore ve
# docs/KURALLAR.md md.3-4); ses burada eklenir.
#
#   kullanim: elma-montaj.sh <actions-run-id> [olcu] [cikti]
#   ornek   : elma-montaj.sh 35054356948 336 04-ciktilar/DANCE-MODE-06-ELMA-1080p.mp4
#
# ATLA_INDIR=1 -> parcalar zaten inmisse tekrar indirmez.
set -eu
cd "$(dirname "$0")/.."
RUN="${1:?kullanim: elma-montaj.sh <actions-run-id> [olcu] [cikti]}"
OLCU="${2:-336}"
CIKTI="${3:-04-ciktilar/DANCE-MODE-06-ELMA-1080p.mp4}"
BPM=132.5
MUZIK="01-muzik/subterranean-pulse-336olcu.wav"
SURE=$(python -c "print(f'{$OLCU*(60/$BPM)*4:.6f}')")
IND="04-ciktilar/elma-parca"

if [ "${ATLA_INDIR:-0}" != "1" ]; then rm -rf "$IND"; fi
mkdir -p "$IND"
[ "${ATLA_INDIR:-0}" = "1" ] || gh run download "$RUN" -D "$IND" -p "parca-*"

# Siralama dosya ADINA gore: her parca kendi alt klasorune iniyor ve find'in
# bulma sirasi dogru gelmiyor.
find "$IND" -name 'parca-*.mp4' -printf '%f %p\n' | sort | awk '{print $2}' > "$IND/_sirali.txt"
echo "parca sayisi: $(wc -l < "$IND/_sirali.txt")"
cat "$IND/_sirali.txt"

: > "$IND/liste.txt"
# ffmpeg Windows yapisi POSIX yolunu acamiyor -> cygpath -m
while read -r f; do
  printf "file '%s'\n" "$(cygpath -m "$(cd "$(dirname "$f")" && pwd)/$(basename "$f")")" >> "$IND/liste.txt"
done < "$IND/_sirali.txt"

# Parcalar ayni kodlama parametreleriyle uretildi -> yeniden kodlama yok.
ffmpeg -v error -y -f concat -safe 0 -i "$IND/liste.txt" -c copy "$IND/govde.mp4"
ffmpeg -v error -y -i "$IND/govde.mp4" -i "$MUZIK" \
  -map 0:v:0 -map 1:a:0 -t "$SURE" -c:v copy -c:a aac -b:a 192k "$CIKTI"

echo "--- dogrulama ---"
ffprobe -v error -show_entries format=duration -of default=nw=1 "$CIKTI"
echo "beklenen sure: $SURE sn  (kural 570-630 sn, docs/KURALLAR.md md.1)"
ffprobe -v error -select_streams v -count_frames \
  -show_entries stream=width,height,nb_read_frames -of default=nw=1 "$CIKTI"
ffmpeg -v error -xerror -i "$CIKTI" -f null - && echo "TAM DECODE: TEMIZ"
ls -lh "$CIKTI"

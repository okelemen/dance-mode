#!/usr/bin/env bash
# HUMAN TETRIS 41 tam video montaji (yerel ffmpeg, md. 9 serbest): Actions parcalari -> dosya adindaki sifir dolgulu numaraya gore birlestir
# -> ses-41.wav ekle (-14 LUFS hedef, tepe <= -1 dBFS alimiter) -> 1080p master + 720p onizleme.
#   bash montaj-41.sh <run_id>
set -euo pipefail
RUN=$1
KOK=/c/Users/eleme/DANCE-MODE
CIK="/c/Users/eleme/OneDrive/Masaüstü/POZ-DUVARI/kesitler"
P=$KOK/03-motor/tetris-pvp/parca-41-${2:-r1}
mkdir -p "$P"
gh run download "$RUN" -R okelemen/dance-mode -D "$P"
mapfile -t L < <(find "$P" -name '*.mp4' | sed -E 's#.*/([^/]*)$#\1\t&#' | sort -t$'\t' -k1,1V | cut -f2)
echo "parca sayisi: ${#L[@]}"; printf '%s\n' "${L[@]##*/}"
: > "$P/liste.txt"; for f in "${L[@]}"; do echo "file '$(cygpath -m "$f")'" >> "$P/liste.txt"; done
ffmpeg -y -loglevel error -f concat -safe 0 -i "$P/liste.txt" -c copy "$P/sessiz.mp4"
S=$KOK/01-muzik/human-tetris-41/ses-41.wav
I=$(ffmpeg -hide_banner -nostats -i "$S" -af ebur128 -f null - 2>&1 | grep -E "^\s+I:" | tail -1 | awk '{print $2}')
K=$(python -c "print(round(-14.0-($I),2))")
echo "ses I=$I kazanc=$K dB"
ffmpeg -y -loglevel error -i "$P/sessiz.mp4" -i "$S" -filter_complex "[1:a]volume=${K}dB,aresample=192000,alimiter=limit=0.6:level=false,aresample=48000[a]" \
  -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 256k -shortest "$CIK/HUMAN-TETRIS-41-TAM-1080p.mp4"
ffmpeg -y -loglevel error -i "$CIK/HUMAN-TETRIS-41-TAM-1080p.mp4" -vf scale=1280:-2 -c:v libx264 -crf 23 -preset fast -c:a copy "$CIK/HUMAN-TETRIS-41-TAM-720p.mp4"
ffprobe -v error -show_entries format=duration:stream=width,height,r_frame_rate -of compact "$CIK/HUMAN-TETRIS-41-TAM-1080p.mp4"
ffmpeg -hide_banner -nostats -i "$CIK/HUMAN-TETRIS-41-TAM-1080p.mp4" -af ebur128=peak=true -f null - 2>&1 | grep -E "I:|Peak:" | tail -2
ffmpeg -y -loglevel error -i "$CIK/HUMAN-TETRIS-41-TAM-1080p.mp4" -vf "fps=1/6.6,scale=480:-1,tile=6x5" -frames:v 1 "$CIK/HUMAN-TETRIS-41-TAM-KONTAK.jpg"
ffmpeg -v error -i "$CIK/HUMAN-TETRIS-41-TAM-1080p.mp4" -f null - && echo "decode temiz"

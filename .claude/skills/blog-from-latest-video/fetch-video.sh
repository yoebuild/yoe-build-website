#!/usr/bin/env bash
# Fetch metadata + transcript for a [yoe] walkthrough video.
#
# Usage:
#   fetch-video.sh                # newest video in the default playlist
#   fetch-video.sh <video-id>     # a specific video
#   fetch-video.sh --list         # list the playlist, newest first
#
# Writes to a temp dir and prints:
#   VIDEO_ID, TITLE, URL (youtu.be short link), UPLOAD_DATE, DESCRIPTION,
#   and the transcript (or a clear "NO TRANSCRIPT" marker).
set -euo pipefail

PLAYLIST="https://www.youtube.com/playlist?list=PL3XJli5z9VFd5c0xlrFZkqm_N0dOeWhPP"

if [[ "${1:-}" == "--list" ]]; then
  yt-dlp --flat-playlist \
    --print "%(playlist_index)s|%(id)s|%(title)s" "$PLAYLIST"
  exit 0
fi

if [[ -n "${1:-}" ]]; then
  VID="$1"
else
  # Playlist index 1 is the newest upload.
  VID=$(yt-dlp --flat-playlist --playlist-items 1 --print "%(id)s" "$PLAYLIST")
fi

URL_WATCH="https://www.youtube.com/watch?v=${VID}"
WORK=$(mktemp -d)
trap 'rm -rf "$WORK"' EXIT

TITLE=$(yt-dlp --skip-download --print "%(title)s" "$URL_WATCH" 2>/dev/null)
UPLOAD=$(yt-dlp --skip-download --print "%(upload_date)s" "$URL_WATCH" 2>/dev/null)
DESC=$(yt-dlp --skip-download --print "%(description)s" "$URL_WATCH" 2>/dev/null)

echo "VIDEO_ID: ${VID}"
echo "TITLE: ${TITLE}"
echo "URL: https://youtu.be/${VID}"
echo "UPLOAD_DATE: ${UPLOAD}"
echo "DESCRIPTION:"
echo "${DESC}"
echo
echo "TRANSCRIPT:"
# Prefer human subs, fall back to auto-generated. Recent uploads may have neither.
yt-dlp --skip-download --write-subs --write-auto-subs \
  --sub-langs "en.*" --convert-subs srt \
  -o "${WORK}/sub.%(ext)s" "$URL_WATCH" >/dev/null 2>&1 || true

SRT=$(ls "${WORK}"/sub*.srt 2>/dev/null | head -1 || true)
if [[ -n "${SRT}" ]]; then
  # Strip SRT sequence numbers/timestamps/blank lines, then collapse the
  # rolling-caption duplicates auto-subs emit (each line repeats ~3x).
  grep -vE '^[0-9]+$|-->' "${SRT}" | sed '/^[[:space:]]*$/d' \
    | awk '$0 != prev { print } { prev = $0 }'
else
  echo "NOT_READY — YouTube has not generated captions for this video yet."
  echo "Captions usually appear within an hour or two of upload. Wait and retry;"
  echo "do not write the post from the description alone."
  exit 2
fi

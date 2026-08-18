#!/bin/bash
# Regenerates the Offgrid Media subsite image assets from the app repo.
# Run from offgridmedia/_build:  ./make_assets.sh
# Requires: imagemagick (magick), ffmpeg.
set -euo pipefail

APP="${APP:-../../../share_to_save}"
OUT="$(cd "$(dirname "$0")/.." && pwd)"
SHOTS="$APP/fastlane/screenshots"
ICON="$APP/OffgridMedia/Assets.xcassets/AppIcon.appiconset/icon-1024.png"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

NAMES=(01_library 02_import 03_folders 04_player 05_actions 06_settings)
# site locale : fastlane locale
LOCALES=(en:en-US de:de-DE es:es-ES fr:fr-FR hi:hi-IN id:id-ID pt:pt-BR ru:ru-RU zh:zh-Hans ar:ar-SA)

# ---- app icon ----
magick "$ICON" -resize 512x512 -strip -define png:compression-level=9 "$OUT/icon.png"

# ---- screenshots (fastlane framed output, one set per locale) ----
for pair in "${LOCALES[@]}"; do
    loc="${pair%%:*}"; fl="${pair##*:}"
    mkdir -p "$OUT/screenshots/$loc"
    for n in "${NAMES[@]}"; do
        magick "$SHOTS/$fl/iPhone 17 Pro Max-${n}_framed.png" \
            -resize 660x1434! -strip -quality 80 "$OUT/screenshots/$loc/iphone-$n.webp"
        magick "$SHOTS/$fl/iPad Pro 13-inch (M5)-${n}_framed.png" \
            -resize 720x960! -strip -quality 80 "$OUT/screenshots/$loc/ipad-$n.webp"
    done
done

# ---- hero preview (crossfade of the unframed English shots) ----
# ponytail: slideshow, not a screen recording — regenerating a recording needs a simulator run.
i=0
for n in "${NAMES[@]}"; do
    magick "$SHOTS/en-US/iPhone 17 Pro Max-$n.png" -resize 500x1084! -strip "$(printf "%s/in%02d.png" "$TMP" $i)"
    i=$((i + 1))
done
ffmpeg -y -v error \
    -loop 1 -t 3 -i "$TMP/in00.png" -loop 1 -t 3 -i "$TMP/in01.png" \
    -loop 1 -t 3 -i "$TMP/in02.png" -loop 1 -t 3 -i "$TMP/in03.png" \
    -loop 1 -t 3 -i "$TMP/in04.png" -loop 1 -t 3.5 -i "$TMP/in05.png" \
    -filter_complex "[0][1]xfade=fade:duration=0.6:offset=2.4[a];\
[a][2]xfade=fade:duration=0.6:offset=4.8[b];\
[b][3]xfade=fade:duration=0.6:offset=7.2[c];\
[c][4]xfade=fade:duration=0.6:offset=9.6[d];\
[d][5]xfade=fade:duration=0.6:offset=12,fps=24,format=yuv420p[v]" \
    -map "[v]" -c:v libx264 -crf 30 -preset slow -movflags +faststart "$OUT/preview.mp4"
magick "$TMP/in00.png" -strip -quality 80 "$OUT/preview-poster.webp"

# ---- social card ----
FONT="/System/Library/Fonts/Avenir Next.ttc"
NAVY_A="#132A5C"; NAVY_B="#081228"; SKY="#5CC8F7"; BODY="#C6D6F2"

magick -size 1200x630 gradient:"$NAVY_A"-"$NAVY_B" -rotate 0 "$TMP/bg.png"
magick "$TMP/bg.png" \
    \( -size 1200x630 radial-gradient:"#2F6FEC"-"#00000000" -resize 1200x630! \) \
    -compose Overlay -define compose:args=30 -composite -alpha off "$TMP/bg.png"

# rounded screenshot helper
round() { # src dst height
    magick "$1" -resize "x$3" \( +clone -alpha extract -draw "fill black polygon 0,0 0,26 26,0 fill white circle 26,26 26,0" \
        \( +clone -flip \) -compose Multiply -composite \( +clone -flop \) -compose Multiply -composite \) \
        -alpha off -compose CopyOpacity -composite "$2"
}
round "$SHOTS/en-US/iPhone 17 Pro Max-04_player.png" "$TMP/s2.png" 470
round "$SHOTS/en-US/iPhone 17 Pro Max-01_library.png" "$TMP/s1.png" 520

magick "$TMP/bg.png" \
    \( "$TMP/s2.png" \) -gravity NorthWest -geometry +1005+140 -composite \
    \( "$TMP/s1.png" \) -gravity NorthWest -geometry +800+92 -composite \
    \( "$ICON" -resize 132x132 \) -gravity NorthWest -geometry +72+72 -composite \
    -font "$FONT" \
    -fill white -pointsize 78 -annotate +72+292 "Offgrid Media" \
    -fill "$SKY" -pointsize 27 -kerning 4 -annotate +76+382 "PRIVATE LIBRARY" \
    -fill "$BODY" -pointsize 30 -kerning 0 \
    -annotate +72+462 "Everything you keep, offline." \
    -annotate +72+505 "Import, organise and play your own video" \
    -annotate +72+548 "and audio. On device. No account." \
    -quality 88 "$OUT/og-offgridmedia.jpg"

echo "assets written to $OUT"

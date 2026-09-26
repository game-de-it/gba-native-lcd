#!/bin/sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
VERSION=${1:-v0.1.0}
NAME="GBA-Native-LCD-Shader-${VERSION}"
STAGE=$(mktemp -d "${TMPDIR:-/tmp}/gba-native-lcd.XXXXXX")
PACKAGE="$STAGE/$NAME"
OUTPUT="$ROOT/dist/${VERSION}/$NAME.zip"

mkdir -p "$PACKAGE" "$(dirname -- "$OUTPUT")"

for file in \
    gba-reflective-ghost.glsl \
    gba-reflective-matrix.glsl \
    gba-reflective-optics.glsl \
    gba-reflective-response.glsl \
    gba-reflective-v2.glslp \
    rgb-curve-lut.glsl \
    rgb_curve_lut.png
do
    cp "$ROOT/variants/$file" "$PACKAGE/$file"
done

cp "$ROOT/shader-only/README.md" "$PACKAGE/README.md"
cp "$ROOT/shader-only/README_JA.md" "$PACKAGE/README_JA.md"
cp "$ROOT/LICENSE" "$PACKAGE/LICENSE"

(cd "$STAGE" && zip -q -X -r "$OUTPUT" "$NAME")
printf '%s\n' "$OUTPUT"

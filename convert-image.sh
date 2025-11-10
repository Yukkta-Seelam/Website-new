#!/bin/bash

# Simple script to convert HEIC to JPG for web compatibility
# Requires ImageMagick or sips (macOS built-in)

INPUT="IMG_1437.HEIC"
OUTPUT="IMG_1437.jpg"

if command -v sips &> /dev/null; then
    # macOS built-in converter
    sips -s format jpeg "$INPUT" --out "$OUTPUT"
    echo "✓ Converted $INPUT to $OUTPUT using sips"
elif command -v convert &> /dev/null; then
    # ImageMagick
    convert "$INPUT" "$OUTPUT"
    echo "✓ Converted $INPUT to $OUTPUT using ImageMagick"
else
    echo "⚠ No converter found. Please install ImageMagick or use macOS sips"
    echo "  On macOS: sips -s format jpeg IMG_1437.HEIC --out IMG_1437.jpg"
    echo "  Or use an online converter to convert HEIC to JPG/PNG"
fi


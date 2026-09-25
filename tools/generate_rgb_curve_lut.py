#!/usr/bin/env python3
"""Generate a provisional 256-entry RGB curve LUT from supplied anchors."""

from pathlib import Path

import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "diagnostics" / "rgb_curve_lut_interpolated.png"

INPUT = np.array([0, 32, 64, 96, 128, 160, 192, 224, 240, 255])
RED = np.array([20.0, 24.5, 26.1, 27.6, 28.9, 34.2, 39.0, 48.4, 61.7, 79.9])
GREEN = np.array([17.0, 19.5, 23.2, 23.8, 26.7, 28.3, 38.6, 50.6, 61.0, 78.7])
BLUE = np.array([19.0, 23.0, 28.7, 31.8, 39.7, 43.8, 52.1, 58.3, 58.9, 78.3])


def main() -> None:
    domain = np.arange(256)
    curves = np.stack(
        [np.interp(domain, INPUT, channel) for channel in (RED, GREEN, BLUE)],
        axis=-1,
    )
    pixels = np.rint(curves).clip(0, 255).astype(np.uint8)[None, :, :]
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(pixels, "RGB").save(OUTPUT)
    print(OUTPUT)


if __name__ == "__main__":
    main()

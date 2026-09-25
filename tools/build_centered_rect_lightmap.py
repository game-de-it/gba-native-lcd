#!/usr/bin/env python3
"""Extract and center the hand-authored rectangular light multiplier."""

from pathlib import Path

import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path("/Users/kroot/Downloads/bg-w3.png")
WIDTH, HEIGHT = 960, 640
RECT_X, RECT_Y, RECT_W, RECT_H = 96, 261, 776, 286


def smoothstep(edge0: float, edge1: float, value: np.ndarray) -> np.ndarray:
    t = np.clip((value - edge0) / (edge1 - edge0), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def flat_light_field() -> np.ndarray:
    rows = np.arange(HEIGHT, dtype=np.float32)
    columns = np.arange(WIDTH, dtype=np.float32)
    top = 0.25 + 0.75 * smoothstep(0.0, 30.0, rows)
    bottom = 0.25 + 0.75 * smoothstep(0.0, 30.0, HEIGHT - 1.0 - rows)
    left = 0.25 + 0.75 * smoothstep(0.0, 30.0, columns)
    right = 0.25 + 0.75 * smoothstep(0.0, 30.0, WIDTH - 1.0 - columns)
    lower = 1.0 + 0.80 * np.clip(
        (rows - 180.0) / (HEIGHT - 180.0 - 1.0), 0.0, 1.0
    )
    return (
        top[:, None]
        * bottom[:, None]
        * left[None, :]
        * right[None, :]
        * lower[:, None]
    )


def main() -> None:
    source = np.asarray(Image.open(SOURCE).convert("L"), dtype=np.float32)
    authored = source[40:680, 160:1120] / 255.0
    base = flat_light_field()
    source_rect = authored[
        RECT_Y : RECT_Y + RECT_H, RECT_X : RECT_X + RECT_W
    ]
    base_rect = base[
        RECT_Y : RECT_Y + RECT_H, RECT_X : RECT_X + RECT_W
    ] * 0.5
    rect_multiplier = np.clip(source_rect / np.maximum(base_rect, 1e-4), 0.0, 2.0)

    multiplier = np.ones((HEIGHT, WIDTH), dtype=np.float32)
    target_x = (WIDTH - RECT_W) // 2
    target_y = (HEIGHT - RECT_H) // 2
    multiplier[
        target_y : target_y + RECT_H, target_x : target_x + RECT_W
    ] = rect_multiplier

    # Encode multiplier 0..2 as texture values 0..1.
    encoded = np.round(multiplier * 0.5 * 255.0).astype(np.uint8)
    texture = Image.fromarray(encoded, "L")
    texture.save(ROOT / "variants" / "centered-rect-light-map.png")

    preview = np.clip(base * multiplier * 0.5, 0.0, 1.0)
    preview_rgb = np.repeat(preview[..., None], 3, axis=2)
    preview_image = Image.fromarray(
        np.round(preview_rgb * 255.0).astype(np.uint8), "RGB"
    )
    output = ROOT / "captures" / "lighting" / "centered-rect-light-preview.png"
    preview_image.save(output)
    print(output)


if __name__ == "__main__":
    main()

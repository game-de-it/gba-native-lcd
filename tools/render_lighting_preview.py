#!/usr/bin/env python3
"""Render the current and proposed GBA reflective-light fields."""

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "captures" / "lighting"
WIDTH = 960
HEIGHT = 640
SHADOW_END = 0.28


def smoothstep(edge0: float, edge1: float, value: np.ndarray) -> np.ndarray:
    t = np.clip((value - edge0) / (edge1 - edge0), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def field_image(field: np.ndarray) -> Image.Image:
    # Mid-grey makes both shadow loss and reflected-light gain visible without
    # introducing game colours or LCD matrix contrast.
    grey = np.clip(0.58 * field, 0.0, 1.0)
    if grey.ndim == 1:
        grey = np.repeat(grey[:, None], WIDTH, axis=1)
    rgb = grey[..., None]
    rgb = np.repeat(rgb, 3, axis=2)
    return Image.fromarray(np.round(rgb * 255.0).astype(np.uint8), "RGB")


def labelled(image: Image.Image, title: str, field: np.ndarray) -> Image.Image:
    header = 54
    result = Image.new("RGB", (WIDTH, HEIGHT + header), (20, 20, 20))
    result.paste(image, (0, header))
    draw = ImageDraw.Draw(result)
    draw.text((14, 10), title, fill=(245, 245, 245))
    vertical = field if field.ndim == 1 else field[:, WIDTH // 2]
    draw.text(
        (14, 30),
        f"top {vertical[0]:.2f} / shadow end {vertical[int(SHADOW_END * (HEIGHT - 1))]:.2f} / bottom {vertical[-1]:.2f}",
        fill=(190, 190, 190),
    )
    y = header + int(SHADOW_END * HEIGHT)
    draw.line((0, y, WIDTH - 1, y), fill=(230, 80, 80), width=2)
    if field.ndim == 2:
        draw.line((30, header, 30, header + HEIGHT - 1), fill=(230, 190, 60), width=1)
        draw.line((WIDTH - 31, header, WIDTH - 31, header + HEIGHT - 1), fill=(230, 190, 60), width=1)
    return result


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    y = (np.arange(HEIGHT, dtype=np.float32) + 0.5) / HEIGHT

    # Current shader: ambient gain remains below 1.0 after the bezel shadow
    # has ended, so most of the panel is still dimmer than normal.
    current_ambient = 0.80 + y * 0.26
    current_bezel = 0.72 + 0.28 * smoothstep(0.0, SHADOW_END, y)
    current = current_ambient * current_bezel

    # Proposed continuous three-region field for the 640-line display.
    rows = np.arange(HEIGHT, dtype=np.float32)
    top_t = np.clip(rows / 29.0, 0.0, 1.0)
    upper_t = np.clip((rows - 30.0) / 149.0, 0.0, 1.0)
    lower_t = np.clip((rows - 180.0) / 459.0, 0.0, 1.0)
    top = 0.10 + 0.20 * top_t
    upper = 0.30 + 0.70 * upper_t
    lower = 1.0 + 0.80 * lower_t
    vertical = np.where(rows < 30.0, top, np.where(rows < 180.0, upper, lower))
    columns = np.arange(WIDTH, dtype=np.float32)
    edge_distance = np.minimum(columns, WIDTH - 1.0 - columns)
    side = 0.40 + 0.60 * smoothstep(0.0, 30.0, edge_distance)
    proposed = vertical[:, None] * side[None, :]

    # Current sensor-driven lighting with the device lying face-up. All four
    # bezel shadows use the neutral 30px reach and a 0.25 root. There is no
    # tilt-driven far-light gain when the panel is level; the established
    # lower-panel reflected-light ramp remains active.
    top_distance = rows
    bottom_distance = HEIGHT - 1.0 - rows
    left_distance = columns
    right_distance = WIDTH - 1.0 - columns
    top_edge = 0.25 + 0.75 * smoothstep(0.0, 30.0, top_distance)
    bottom_edge = 0.25 + 0.75 * smoothstep(0.0, 30.0, bottom_distance)
    left_edge = 0.25 + 0.75 * smoothstep(0.0, 30.0, left_distance)
    right_edge = 0.25 + 0.75 * smoothstep(0.0, 30.0, right_distance)
    lower_reflection = 1.0 + 0.80 * np.clip(
        (rows - 180.0) / (HEIGHT - 180.0 - 1.0), 0.0, 1.0
    )
    sensor_flat = (
        top_edge[:, None]
        * bottom_edge[:, None]
        * left_edge[None, :]
        * right_edge[None, :]
        * lower_reflection[:, None]
    )

    # Use 0.5 exposure so neutral light (1.0) is middle grey and the current
    # 1.80 reflected-light maximum remains visible without clipping.
    sensor_grey = np.clip(sensor_flat * 0.5, 0.0, 1.0)
    sensor_rgb = np.repeat(sensor_grey[..., None], 3, axis=2)
    sensor_image = Image.fromarray(
        np.round(sensor_rgb * 255.0).astype(np.uint8), "RGB"
    )
    sensor_image.save(OUTPUT / "current-sensor-flat-light-field.png")

    x = (columns + 0.5) / WIDTH
    y_normalized = (rows + 0.5) / HEIGHT
    band_delta_y = (y_normalized - 0.5) / 0.14
    band_x_distance = np.abs(x - 0.5)
    band_horizontal = 1.0 - smoothstep(0.38, 0.46, band_x_distance)
    band_vertical = np.exp(-0.5 * band_delta_y ** 2)
    band = band_vertical[:, None] * band_horizontal[None, :]
    soft_band_field = sensor_flat * (1.0 + 0.80 * band)
    soft_band_grey = np.clip(soft_band_field * 0.5, 0.0, 1.0)
    soft_band_rgb = np.repeat(soft_band_grey[..., None], 3, axis=2)
    soft_band_image = Image.fromarray(
        np.round(soft_band_rgb * 255.0).astype(np.uint8), "RGB"
    )
    soft_band_image.save(OUTPUT / "soft-moving-band-light-preview.png")

    # Keep a compact 1.65 core, then use most of the surrounding 1.80 band as
    # a broad transition area. This avoids a visible inner-band boundary.
    inner_horizontal = 1.0 - smoothstep(0.16, 0.38, band_x_distance)
    inner_y_distance = np.abs(y_normalized - 0.5)
    inner_vertical = 1.0 - smoothstep(0.04, 0.14, inner_y_distance)
    inner_band = inner_vertical[:, None] * inner_horizontal[None, :]
    expanded_band_vertical = np.exp(
        -0.5 * ((y_normalized - 0.5) / (0.14 * 1.20)) ** 2
    )
    expanded_outer_band = expanded_band_vertical[:, None] * band_horizontal[None, :]
    outer_band_gain = 1.0 + 0.80 * expanded_outer_band
    nested_band_gain = outer_band_gain * (1.0 - inner_band) + 1.65 * inner_band
    nested_band_field = sensor_flat * nested_band_gain

    # Lower exposure keeps the 1.80 outer band below white clipping so the
    # independent 1.30 inner profile remains visible in the diagnostic preview.
    comparison_exposure = 0.32
    current_compare = np.clip(
        soft_band_field * comparison_exposure, 0.0, 1.0
    )
    nested_compare = np.clip(
        nested_band_field * comparison_exposure, 0.0, 1.0
    )

    def diagnostic_image(field: np.ndarray) -> Image.Image:
        rgb = np.repeat(field[..., None], 3, axis=2)
        return Image.fromarray(np.round(rgb * 255.0).astype(np.uint8), "RGB")

    nested_image = diagnostic_image(nested_compare)
    nested_image.save(OUTPUT / "nested-band-light-preview.png")

    header = 38
    comparison = Image.new("RGB", (WIDTH * 2, HEIGHT + header), (20, 20, 20))
    comparison.paste(diagnostic_image(current_compare), (0, header))
    comparison.paste(nested_image, (WIDTH, header))
    comparison_draw = ImageDraw.Draw(comparison)
    comparison_draw.text((14, 12), "Current band 1.80", fill=(245, 245, 245))
    comparison_draw.text(
        (WIDTH + 14, 12),
        "Outer band height +20% / inner band 1.65",
        fill=(245, 245, 245),
    )
    comparison.save(OUTPUT / "current-vs-nested-band-light.png")

    proposed_clean = field_image(proposed)
    proposed_clean.save(OUTPUT / "proposed-light-field-with-sides-clean.png")

    panels = [
        labelled(field_image(current), "Current light field", current),
        labelled(field_image(proposed), "Proposed top-light field", proposed),
    ]
    comparison = Image.new("RGB", (WIDTH * 2, HEIGHT + 54))
    comparison.paste(panels[0], (0, 0))
    comparison.paste(panels[1], (WIDTH, 0))
    comparison.save(OUTPUT / "current-vs-proposed-side-light-field.png")

    print(OUTPUT / "proposed-light-field-with-sides-clean.png")
    print(OUTPUT / "current-vs-proposed-side-light-field.png")
    print(OUTPUT / "current-sensor-flat-light-field.png")
    print(OUTPUT / "soft-moving-band-light-preview.png")
    print(OUTPUT / "nested-band-light-preview.png")
    print(OUTPUT / "current-vs-nested-band-light.png")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Render a CPU approximation of the GBA Native LCD GLSL preset."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "captures" / "no-shader.png"
DEFAULT_OUTPUT = ROOT / "captures" / "preview-current.png"
DEFAULT_PRESET = ROOT / "gba-native-lcd.glslp"
REFERENCE = ROOT / "captures" / "original-panel-crop.png"


def read_parameters(path: Path) -> dict[str, float]:
    values: dict[str, float] = {}
    for raw_line in path.read_text(encoding="ascii").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, raw_value = (part.strip() for part in line.split("=", 1))
        value = raw_value.strip('"')
        try:
            values[key] = float(value)
        except ValueError:
            continue
    return values


def smoothstep(edge0: float, edge1: float, value: np.ndarray) -> np.ndarray:
    t = np.clip((value - edge0) / (edge1 - edge0), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def taps(sigma: float, shift: float) -> np.ndarray:
    positions = np.array([-1.0, 0.0, 1.0], dtype=np.float32) - shift
    weights = np.exp(-0.5 * positions * positions / max(sigma * sigma, 1e-4))
    return weights / weights.sum()


def shifted_edge(image: np.ndarray, dx: int, dy: int) -> np.ndarray:
    height, width = image.shape[:2]
    x = np.clip(np.arange(width) + dx, 0, width - 1)
    y = np.clip(np.arange(height) + dy, 0, height - 1)
    return image[y[:, None], x[None, :]]


def panel_pass(source: np.ndarray, p: dict[str, float], scale: int) -> np.ndarray:
    bleed_x = p["LCD_BLEED_X"]
    bleed_y = p["LCD_BLEED_Y"]
    offset = p["ELEMENT_OFFSET"]

    wx = np.stack(
        [taps(bleed_x, -offset), taps(bleed_x, 0.0), taps(bleed_x, offset)],
        axis=1,
    )
    wy = taps(bleed_y, p["LCD_SMEAR_Y"])

    diffused = np.zeros_like(source)
    for yi, dy in enumerate((-1, 0, 1)):
        for xi, dx in enumerate((-1, 0, 1)):
            sample = shifted_edge(source, dx, dy)
            diffused += sample * wx[xi][None, None, :] * wy[yi]

    luma_weights = np.array([0.299, 0.587, 0.114], dtype=np.float32)
    centre_luma = source @ luma_weights
    diffused_luma = diffused @ luma_weights
    invasion = np.where(
        diffused_luma >= centre_luma,
        p["LCD_BRIGHT_INVADE"],
        p["LCD_DARK_INVADE"],
    )
    luma_mix = np.maximum(p["LCD_LUMA_BLEED"], invasion)
    retained_luma = centre_luma * (1.0 - luma_mix) + diffused_luma * luma_mix
    colour = diffused + (retained_luma - diffused_luma)[..., None]

    matrix = np.array(
        [[0.68, 0.17, 0.08], [0.12, 0.74, 0.18], [0.08, 0.22, 0.58]],
        dtype=np.float32,
    )
    mixed = colour @ matrix.T
    colour = colour * (1.0 - p["LCD_COLOR"]) + mixed * p["LCD_COLOR"]
    luminance = colour @ luma_weights
    colour = (
        luminance[..., None] * (1.0 - p["LCD_SATURATION"])
        + colour * p["LCD_SATURATION"]
    )
    colour = (colour - 0.5) * p["LCD_CONTRAST"] + 0.5

    cool = p["PANEL_COOL"]
    tint = np.array(
        [1.0 - cool * 0.90, 1.0 - cool * 0.46, 1.0 + cool * 1.30],
        dtype=np.float32,
    )
    colour = np.clip(colour * tint * p["LCD_BRIGHTNESS"], 0.0, 1.0)

    output = np.repeat(np.repeat(colour, scale, axis=0), scale, axis=1)
    height, width = output.shape[:2]

    phase_x = np.mod((np.arange(width, dtype=np.float32) + 0.5) / scale, 1.0)
    phase_y = np.mod((np.arange(height, dtype=np.float32) + 0.5) / scale, 1.0)
    edge_x = np.abs(phase_x - 0.5) * 2.0
    edge_y = np.abs(phase_y - 0.5) * 2.0
    grid = (
        1.0
        - p["GRID_VERTICAL"] * edge_x[None, :] ** 2
        - p["GRID_HORIZONTAL"] * edge_y[:, None] ** 2
    )

    right_boundary = (phase_x >= 0.75).astype(np.float32)
    lower_boundary = (phase_y >= 0.75).astype(np.float32)
    boundary = np.maximum(lower_boundary[:, None], right_boundary[None, :])
    cell_mask = (
        (1.0 + p["CELL_FACE"]) * (1.0 - boundary)
        + (1.0 - p["CELL_GAP"]) * boundary
    )

    band = np.floor(phase_x * 4.0).astype(np.int32)
    element_columns = np.ones((width, 3), dtype=np.float32)
    element_columns[band == 0] = (0.725, 0.725, 1.55)
    element_columns[band == 1] = (0.725, 1.55, 0.725)
    element_columns[band == 2] = (1.55, 0.725, 0.725)
    element_strength = (1.0 - boundary) * p["CELL_BGR"]
    rgb_elements = 1.0 + (
        element_columns[None, ...] - 1.0
    ) * element_strength[..., None]

    down_from_top = (np.arange(height, dtype=np.float32) + 0.5) / height
    broad = 0.55 + (1.30 - 0.55) * smoothstep(0.0, 1.0, down_from_top)
    penumbra = smoothstep(0.0, max(p["BEZEL_DEPTH"], 0.01), down_from_top)
    upper_shadow = 0.25 + (1.0 - 0.25) * penumbra
    vertical_light = (
        1.0 + (broad - 1.0) * p["REFLECTION_GRADIENT"]
    ) * (1.0 + (upper_shadow - 1.0) * p["BEZEL_SHADOW"])

    uv_x = (np.arange(width, dtype=np.float32) + 0.5) / width
    side_distance = np.abs(uv_x - 0.5) * 2.0
    side_light = 1.0 - 0.08 * side_distance**2
    light = vertical_light[:, None] * side_light[None, :]

    return np.clip(
        output
        * rgb_elements
        * cell_mask[..., None]
        * np.maximum(grid, 0.20)[..., None]
        * light[..., None],
        0,
        1,
    )


def optics_pass(image: np.ndarray, p: dict[str, float]) -> np.ndarray:
    left = shifted_edge(image, -1, 0)
    right = shifted_edge(image, 1, 0)
    up = shifted_edge(image, 0, -1)
    down = shifted_edge(image, 0, 1)
    spread = (4.0 * image + left + right + up + down) / 8.0

    luma_weights = np.array([0.299, 0.587, 0.114], dtype=np.float32)
    centre_luma = image @ luma_weights
    spread_luma = spread @ luma_weights
    centre_chroma = image - centre_luma[..., None]
    spread_chroma = spread - spread_luma[..., None]
    output_luma = (
        centre_luma * (1.0 - p["OPTICS_LUMA"])
        + spread_luma * p["OPTICS_LUMA"]
    )
    output_chroma = (
        centre_chroma * (1.0 - p["OPTICS_CHROMA"])
        + spread_chroma * p["OPTICS_CHROMA"]
    )
    return np.clip(output_luma[..., None] + output_chroma, 0.0, 1.0)


def reflective_v2_pass(source: np.ndarray, p: dict[str, float], scale: int) -> np.ndarray:
    neighbours = (
        shifted_edge(source, -1, 0)
        + shifted_edge(source, 1, 0)
        + shifted_edge(source, 0, -1)
        + shifted_edge(source, 0, 1)
    )
    blend = p["SRC_BLEND"]
    colour = source * (1.0 - blend) + neighbours * (blend * 0.25)
    source_colour = colour.copy()

    if "PANEL_MATRIX_STRENGTH" in p:
        matrix = np.array(
            [
                [0.72, 0.15, 0.06],
                [0.08, 0.68, 0.17],
                [0.07, 0.16, 0.65],
            ],
            dtype=np.float32,
        )
        mixed = colour @ matrix.T
        strength = p["PANEL_MATRIX_STRENGTH"]
        colour = colour * (1.0 - strength) + mixed * strength

    luma_weights = np.array([0.299, 0.587, 0.114], dtype=np.float32)
    luminance = colour @ luma_weights
    colour = (
        luminance[..., None] * (1.0 - p["PANEL_SAT_V2"])
        + colour * p["PANEL_SAT_V2"]
    )
    contrast = p.get("PANEL_CONTRAST_V2", 1.0)
    colour = (colour - 0.5) * contrast + 0.5
    floor = p["BLACK_FLOOR"]
    colour = np.power(
        np.maximum(colour, 0.0), p.get("PANEL_GAMMA_V2", 0.90)
    )
    colour = floor + colour * (p["WHITE_LEVEL"] - floor)
    highlight = smoothstep(0.58, 1.0, luminance) * (1.0 - luminance)
    colour += p["HIGHLIGHT_REFLECT"] * highlight[..., None]
    cool = p["PANEL_COOL_V2"]
    colour *= np.array(
        [1.0 - cool * 0.72, 1.0 - cool * 0.28, 1.0 + cool],
        dtype=np.float32,
    )
    colour *= p.get("PANEL_BRIGHTNESS_V2", 1.0)

    if p.get("HUE_CORRECTION", 0.0) > 0.5:
        red = source_colour[..., 0]
        green = source_colour[..., 1]
        blue = source_colour[..., 2]
        orange_mask = (
            smoothstep(0.65, 0.90, red)
            * smoothstep(0.35, 0.62, green)
            * (1.0 - smoothstep(0.18, 0.38, blue))
            * smoothstep(0.10, 0.35, red - green)
        )
        red_mask = (
            smoothstep(0.65, 0.90, red)
            * (1.0 - smoothstep(0.18, 0.42, green))
            * smoothstep(0.30, 0.65, red - green)
            * smoothstep(0.25, 0.60, red - blue)
        )
        green_mask = (
            smoothstep(0.30, 0.62, green)
            * smoothstep(0.06, 0.28, green - red)
            * smoothstep(0.04, 0.26, green - blue)
        )

        correction = np.ones_like(colour)
        factors = (
            (orange_mask, np.array([p["ORANGE_R"], p["ORANGE_G"], p["ORANGE_B"]], dtype=np.float32)),
            (red_mask, np.array([p["RED_R"], p["RED_G"], p["RED_B"]], dtype=np.float32)),
            (green_mask, np.array([p["GREEN_R"], p["GREEN_G"], p["GREEN_B"]], dtype=np.float32)),
        )
        for mask, factor in factors:
            correction = correction * (1.0 - mask[..., None]) + factor * mask[..., None]
        colour *= correction

    output = np.repeat(np.repeat(colour, scale, axis=0), scale, axis=1)
    height, width = output.shape[:2]
    phase_x = np.mod((np.arange(width, dtype=np.float32) + 0.5) / scale, 1.0)
    phase_y = np.mod((np.arange(height, dtype=np.float32) + 0.5) / scale, 1.0)
    band = np.floor(phase_x * 4.0).astype(np.int32)

    filters = np.ones((width, 3), dtype=np.float32)
    filters[band == 0] = (0.90, 0.94, 1.16)
    filters[band == 1] = (0.92, 1.12, 0.92)
    filters[band == 2] = (1.16, 0.93, 0.90)
    filters = 1.0 + (filters - 1.0) * p["SUBPIXEL_STRENGTH"]

    boundary = np.maximum(
        (phase_y[:, None] >= 0.75).astype(np.float32),
        (phase_x[None, :] >= 0.75).astype(np.float32),
    )
    matrix = p["MATRIX_FACE"] * (1.0 - boundary) + (
        1.0 - p["MATRIX_GAP"]
    ) * boundary
    down = (np.arange(height, dtype=np.float32) + 0.5) / height
    rows = np.arange(height, dtype=np.float32)
    top_end = p["TOP_BAND_PX"]
    shadow_end = p["SHADOW_END_PX"]
    shadow_t = np.clip(
        (rows - top_end) / max(shadow_end - top_end - 1.0, 1.0), 0.0, 1.0
    )
    top_t = np.clip(rows / max(top_end - 1.0, 1.0), 0.0, 1.0)
    top_gradient = (
        p["TOP_EDGE_LIGHT"] * (1.0 - top_t)
        + p["SHADOW_START_LIGHT"] * top_t
    )
    lower_t = np.clip(
        (rows - shadow_end) / max(height - shadow_end - 1.0, 1.0), 0.0, 1.0
    )
    shadow_gradient = (
        p["SHADOW_START_LIGHT"] * (1.0 - shadow_t) + shadow_t
    )
    lower_reflection = 1.0 + (p["BOTTOM_LIGHT"] - 1.0) * lower_t
    ambient = np.where(
        rows < top_end,
        top_gradient,
        np.where(rows < shadow_end, shadow_gradient, lower_reflection),
    )
    columns = np.arange(width, dtype=np.float32)
    edge_distance = np.minimum(columns, width - 1.0 - columns)
    side_t = smoothstep(0.0, p.get("SIDE_WIDTH_PX", 1.0), edge_distance)
    side_light = p.get("SIDE_EDGE_LIGHT", 1.0) + (
        1.0 - p.get("SIDE_EDGE_LIGHT", 1.0)
    ) * side_t
    light = ambient[:, None] * side_light[None, :]
    return np.clip(
        output
        * filters[None, ...]
        * matrix[..., None]
        * light[..., None],
        0.0,
        1.0,
    )


def label(image: Image.Image, text: str) -> Image.Image:
    header = 34
    result = Image.new("RGB", (image.width, image.height + header), (20, 20, 20))
    result.paste(image, (0, header))
    draw = ImageDraw.Draw(result)
    draw.text((12, 9), text, fill=(240, 240, 240))
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--preset", type=Path, default=DEFAULT_PRESET)
    parser.add_argument("--lut", type=Path)
    parser.add_argument("--scale", type=int, default=4)
    args = parser.parse_args()

    parameters = read_parameters(args.preset)
    original = Image.open(args.input).convert("RGB")
    source_size = (original.width // args.scale, original.height // args.scale)
    source = original.resize(source_size, Image.Resampling.NEAREST)
    source_array = np.asarray(source, dtype=np.float32) / 255.0

    if args.lut:
        lut = np.asarray(Image.open(args.lut).convert("RGB"), dtype=np.float32)
        lut = lut.reshape(-1, 3)[:256] / 255.0
        indices = np.rint(source_array * 255.0).astype(np.uint8)
        source_array = np.stack(
            [lut[indices[..., channel], channel] for channel in range(3)], axis=-1
        )

    if "SRC_BLEND" in parameters:
        panel = reflective_v2_pass(source_array, parameters, args.scale)
    else:
        panel = panel_pass(source_array, parameters, args.scale)
    rendered = optics_pass(panel, parameters)
    preview = Image.fromarray(np.round(rendered * 255.0).astype(np.uint8), "RGB")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    preview.save(args.output)

    panels = [label(original, "No shader"), label(preview, "CPU shader preview")]
    if REFERENCE.exists():
        reference = Image.open(REFERENCE).convert("RGB").resize(original.size)
        panels.append(label(reference, "Original GBA SP LCD photo"))
    comparison = Image.new("RGB", (sum(p.width for p in panels), panels[0].height))
    x = 0
    for panel in panels:
        comparison.paste(panel, (x, 0))
        x += panel.width
    comparison.save(args.output.with_name(args.output.stem + "-comparison.png"))

    print(args.output)
    print(args.output.with_name(args.output.stem + "-comparison.png"))


if __name__ == "__main__":
    main()

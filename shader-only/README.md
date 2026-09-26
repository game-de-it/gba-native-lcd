# GBA Native LCD shader-only package

[English](README.md) | [日本語](README_JA.md)

This package contains only the GLSL shader. It does not include RetroArch,
mGBA, configuration files or the custom accelerometer-enabled APK.

## Install

1. Keep every file in this directory together with its original filename.
2. Copy the directory to a location visible to RetroArch's shader browser.
3. Select the RetroArch `gl` video driver and restart RetroArch.
4. Load `gba-reflective-v2.glslp` from **Shaders > Load Preset**.
5. Use mGBA with a 240 x 160 GBA image. Exact 4x output at 960 x 640 is the
   calibrated configuration.

The preset needs all seven shader/LUT files. Moving only the `.glslp` file or
renaming `rgb_curve_lut.png` will make it fail to load.

## Why other devices may not look or behave correctly

This is a physical-device profile for KONKR Pocket ADVANCE (Android model:
GT78-VN), not a universal LCD filter.

- **Resolution and scale:** Its cell matrix assumes one 240 x 160 GBA pixel is
  represented by an exact 4 x 4 block on a 960 x 640 output. Other scales can
  produce uneven grid widths, moire, shimmer or an unexpectedly clean image.
- **Panel-specific color:** The 256-step RGB LUT was visually calibrated on the
  KPA panel. Another panel's gamut, gamma, brightness and vendor color
  processing can make the image too dark or change reds and greens.
- **Pixel-based lighting:** Edge shadows use 30- and 180-output-pixel distances
  tuned for 960 x 640. Their apparent size changes at another resolution.
- **Motion support:** Stock RetroArch does not provide the custom
  `Accelerometer` shader uniform used by the KPA APK. The shader therefore uses
  its fixed-light fallback; tilt-driven shadows and reflections will not move.
- **Video driver:** This package is GLSL and requires RetroArch's `gl` driver.
  Vulkan uses Slang presets and cannot load this `.glslp` directly.
- **Performance:** The preset uses five passes and temporal feedback. Slower
  GPUs may show reduced performance even when the files load successfully.

Rendering without an error only confirms shader compatibility. It does not
mean that another device reproduces the intended KPA-calibrated appearance.

## License

GBA Native LCD shader files are released under the MIT License. See `LICENSE`.

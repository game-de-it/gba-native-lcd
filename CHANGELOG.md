# Changelog

## v0.1.1 - 2026-09-28

- Changed the selectable shader installation root to
  `/storage/emulated/0/RetroArch/shaders/` so GLSL presets appear correctly in
  RetroArch's **Load Preset** browser.
- Added `native-lcd-v0.1.1` as the default preset at
  `/storage/emulated/0/RetroArch/shaders/native-lcd-v0.1.1/`.
- Kept the original v0.1.0 shader as the selectable legacy preset
  `/storage/emulated/0/RetroArch/shaders/native-lcd-v0.1.0/`.
- Rebuilt the reflective pixel structure as a fixed dark 4 x 8 cell matrix
  with vertically elliptical emitting faces. This preserves the accepted dark
  separators while softening only the light-emitting area.
- Retuned accelerometer lighting: left/right shadow reach is capped at 80
  pixels, top/bottom reach remains 180 pixels, and the opposite edge clears as
  the device tilts toward the light.
- Reduced and blended the moving environmental reflection to an outer gain of
  `1.30` and an inner absolute level of `1.25`, avoiding the bright framed
  appearance of the earlier reflection.
- Bundled only the final and legacy presets in the release APK; obsolete
  experimental presets are not exposed to users.
- Updated the shader-only archive to include the sixth pass and all eight
  required preset, shader and LUT files.

## v0.1.0 - 2026-09-25

- Added a five-pass reflective GBA LCD shader calibrated on KONKR Pocket
  ADVANCE / GT78-VN.
- Added a 256-step per-channel color LUT, 4x4 BGR cell matrix, restrained
  temporal response, recessed-bezel shadows and a soft reflection band.
- Added accelerometer-driven lighting through a companion RetroArch build.
- Bundled mGBA, RGUI assets, persistent user-data paths and tested low-latency
  video/input defaults.
- Enabled the effect-capable OpenSL path required by AYANEO Equalizer.
- Added English and Japanese documentation with digital and physical-device
  comparisons.

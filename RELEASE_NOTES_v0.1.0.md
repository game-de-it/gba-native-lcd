# GBA Native LCD v0.1.0

This first release packages a KONKR Pocket ADVANCE / GT78-VN profile together
with a custom Arm64 RetroArch build. It recreates the pixel matrix, muted color
response, recessed-panel shadows and temporal softness of the original
reflective Game Boy Advance LCD. Accelerometer input moves the shadows and
soft environmental reflection as the handheld is tilted.

## Included

- RetroArch 1.22.2-based Arm64 APK
- bundled mGBA core and automatic core preset
- five-pass GBA reflective LCD shader and 256-step RGB LUT
- accelerometer-driven lighting with a fixed-light fallback
- AYANEO Equalizer compatible OpenSL audio path
- English and Japanese documentation

## Compatibility

The verified target is KONKR Pocket ADVANCE / GT78-VN at 960 x 640. Other
Arm64 Android handhelds are experimental: the APK may launch, but their display
resolution, panel response, sensor axes and firmware audio effects can differ.

## Important notes

- Back up `retroarch.cfg` before uninstalling or clearing application data.
- Saves, states, screenshots and playlists use the shared
  `/storage/emulated/0/RetroArch-gyrotest/` tree.
- The release APK must be signed with the project's persistent release key.
  Development-signed test builds cannot update a differently signed install.

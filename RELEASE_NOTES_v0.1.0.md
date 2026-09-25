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

## KPA-only release

This release is built, calibrated and supported only for KONKR Pocket ADVANCE /
GT78-VN at 960 x 640. Its 4x pixel matrix, RGB LUT, physical shadow distances,
sensor orientation and AYANEO Equalizer path are KPA-specific. The APK may
technically launch on another Arm64 Android device, but that use is unsupported
and is not evidence that the intended image or motion model is reproduced.

## Important notes

- Back up `retroarch.cfg` before uninstalling or clearing application data.
- Saves, states, screenshots and playlists use the shared
  `/storage/emulated/0/RetroArch-gyrotest/` tree.
- Future updates must use the same persistent release key. Keep the keystore
  and its credentials backed up securely; losing them prevents in-place APK
  updates.

## Licensing

Project-authored files are MIT licensed. RetroArch remains GPL-3.0+ and the
bundled mGBA core remains MPL-2.0; their notices are included in the APK.

## Source code

- [GBA Native LCD source](https://github.com/game-de-it/gba-native-lcd)
- [Modified RetroArch source commit](https://github.com/game-de-it/RetroArch/commit/7059a84431cd5c91f417a96250aa8ef088743792)

## Release verification

- APK: `RetroArch-GBA-LCD-v0.1.0-KPA-arm64.apk`
- SHA-256: `caeb535c8947a745a0903b381ec1b2aa0dc58557231f8bb32fc037f9aa6b1fe0`
- Version: `1.22.2_GBA_LCD_0.1.0`
- ABI: `arm64-v8a`
- Signing certificate SHA-256:
  `5D:CC:20:45:24:79:9D:8F:95:2E:9F:80:0F:FA:BE:86:9C:A9:75:54:99:12:32:79:A3:A1:CD:19:8D:6E:42:9D`

The signed APK was installed and launched on GT78-VN. GBA content, shader
rendering, accelerometer-driven lighting, physical controls and release-key
in-place reinstall were verified. The reinstall preserved the configuration
checksum and the shared save/state file count.

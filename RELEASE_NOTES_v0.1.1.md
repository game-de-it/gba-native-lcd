# GBA Native LCD v0.1.1

This release completes the revised reflective-cell shader for **KONKR Pocket
ADVANCE (Android model: GT78-VN)** and makes it the default preset in the
bundled RetroArch build.

## Visual comparison

In both comparisons below, **the left side is the v0.1.1 shader and the right
side is a photograph of an original reflective GBA LCD**.

![Left: v0.1.1 shader. Right: original reflective GBA LCD](https://raw.githubusercontent.com/game-de-it/gba-native-lcd/v0.1.1/docs/images/v0.1.1-shader-vs-reflective-lcd-overview.png)

![Left: detailed v0.1.1 shader crop. Right: detailed original reflective GBA LCD crop](https://raw.githubusercontent.com/game-de-it/gba-native-lcd/v0.1.1/docs/images/v0.1.1-shader-vs-reflective-lcd-detail.png)

The shader's emitting cells are slightly brighter and its color is subtly
different from the photographed LCD because the shader includes a moving
environmental reflection band. The band restores luminance after the muted
color LUT and represents ambient light reflected by the LCD surface, not an
internal backlight. The photograph also contains its own illumination and
camera response.

## Changes

- Shader storage now uses `/storage/emulated/0/RetroArch/shaders/`, allowing
  the presets to appear correctly under **Shaders > Load Preset**.
- `native-lcd-v0.1.1` is the new completed shader and the default mGBA preset:
  `/storage/emulated/0/RetroArch/shaders/native-lcd-v0.1.1/`.
- `native-lcd-v0.1.0` remains bundled as the selectable legacy shader:
  `/storage/emulated/0/RetroArch/shaders/native-lcd-v0.1.0/`.
- The reflective matrix now uses vertically elliptical emitting faces inside a
  fixed dark 4 x 8 cell structure, producing the accepted reflective-LCD dot
  texture without blurring the black separators.
- Tilt lighting was retuned. Left/right shadows extend up to 80 pixels;
  top/bottom shadows retain the 180-pixel maximum.
- The moving reflection band and its gradients were retuned to avoid a bright
  frame: the outer gain is `1.30`, and the inner absolute level is `1.25`.
- Obsolete experimental shader presets were removed from the user-facing APK.
- The shader-only ZIP now contains all eight files required by the six-pass
  preset.

## Installation and update

Install `RetroArch-GBA-LCD-v0.1.1-KPA-arm64.apk`. It is signed with the same
persistent release key as v0.1.0 and can update that installation in place.
Saves, states and shared user data remain under
`/storage/emulated/0/RetroArch-gyrotest/`. Back up `retroarch.cfg` before
uninstalling, clearing app data or changing Android package storage.

The APK is calibrated and supported only for KONKR Pocket ADVANCE. Other
Arm64 Android devices may launch it, but panel color, cell scale, sensor axes,
controls and AYANEO Equalizer integration are not guaranteed.

## Downloads

- `RetroArch-GBA-LCD-v0.1.1-KPA-arm64.apk`
- `GBA-Native-LCD-Shader-v0.1.1.zip`
- `SHA256SUMS`

## Verification

- Package: `com.retroarch.aarch64`
- Version: `1.22.2_GBA_LCD_v0.1.1`
- APK SHA-256: `97ce9a3e23c99542a02d158ddc80f223aadb85a0bf26c102881e149b70d26071`
- Shader ZIP SHA-256: `d121ccbb4db8e92747ab1bb9a0222091d97890a30e23353e67d7918d07f7b987`
- Modified RetroArch source: [`06cc964`](https://github.com/game-de-it/RetroArch/commit/06cc9643c70a8ad3197259c24110eda32773eef6)

## Licenses

Project-authored files are MIT licensed. RetroArch remains GPL-3.0-or-later,
and the bundled mGBA core remains MPL-2.0. Their notices are included in the
APK.

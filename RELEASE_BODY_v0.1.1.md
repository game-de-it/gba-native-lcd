# GBA Native LCD v0.1.1

[English](#english) | [日本語](#日本語)

## English

v0.1.1 completes the revised reflective-cell shader for **KONKR Pocket
ADVANCE (Android model: GT78-VN)** and makes `native-lcd-v0.1.1` the default.

### Visual comparison

In both images, **the left side is the v0.1.1 shader and the right side is a
photograph of an original reflective GBA LCD**.

![Left: v0.1.1 shader. Right: original reflective GBA LCD](https://raw.githubusercontent.com/game-de-it/gba-native-lcd/v0.1.1/docs/images/v0.1.1-shader-vs-reflective-lcd-overview.png)

![Left: detailed v0.1.1 shader crop. Right: detailed original reflective GBA LCD crop](https://raw.githubusercontent.com/game-de-it/gba-native-lcd/v0.1.1/docs/images/v0.1.1-shader-vs-reflective-lcd-detail.png)

The shader's emitting cells are slightly brighter and its color is subtly
different because the moving environmental reflection band restores luminance
after the muted color LUT. It models ambient light reflected by the LCD
surface, not an internal backlight. The photograph also includes its own
illumination and camera response.

### Changes

- Shader storage moved to `/storage/emulated/0/RetroArch/shaders/` so presets
  appear correctly in **Shaders > Load Preset**.
- `native-lcd-v0.1.1` is the completed and default preset at
  `/storage/emulated/0/RetroArch/shaders/native-lcd-v0.1.1/`.
- The legacy `native-lcd-v0.1.0` remains selectable at
  `/storage/emulated/0/RetroArch/shaders/native-lcd-v0.1.0/`.
- Added the accepted fixed dark 4 x 8 cell structure with vertically
  elliptical emitting faces.
- Retuned moving shadows: 80px horizontal maximum and 180px vertical maximum.
- Retuned the reflection band and gradient to outer `1.30` / inner `1.25`.
- Removed obsolete experimental presets from the user-facing APK.
- Updated the shader-only ZIP with all eight files required by the six-pass
  preset.

### Install

Install `RetroArch-GBA-LCD-v0.1.1-KPA-arm64.apk`. It uses the same persistent
release key as v0.1.0 and supports an in-place update. User data remains under
`/storage/emulated/0/RetroArch-gyrotest/`.

This APK is calibrated and supported only for KONKR Pocket ADVANCE. See the
[English README](https://github.com/game-de-it/gba-native-lcd/blob/v0.1.1/README.md)
for compatibility, save-data and license details.

### Verification

- Package: `com.retroarch.aarch64`
- Version: `1.22.2_GBA_LCD_v0.1.1`
- APK SHA-256: `97ce9a3e23c99542a02d158ddc80f223aadb85a0bf26c102881e149b70d26071`
- Shader ZIP SHA-256: `d121ccbb4db8e92747ab1bb9a0222091d97890a30e23353e67d7918d07f7b987`
- Modified RetroArch source: [`06cc964`](https://github.com/game-de-it/RetroArch/commit/06cc9643c70a8ad3197259c24110eda32773eef6)

---

## 日本語

v0.1.1では、**KONKR Pocket ADVANCE（Android model: GT78-VN）**向けの
反射型セル表現を完成させ、`native-lcd-v0.1.1`を既定シェーダーにしました。

### 表示比較

2枚とも、**左がv0.1.1シェーダー、右が純正GBA反射型LCDの写真**です。

![左：v0.1.1シェーダー、右：純正GBA反射型LCD](https://raw.githubusercontent.com/game-de-it/gba-native-lcd/v0.1.1/docs/images/v0.1.1-shader-vs-reflective-lcd-overview.png)

![左：v0.1.1シェーダーの拡大、右：純正GBA反射型LCD写真の拡大](https://raw.githubusercontent.com/game-de-it/gba-native-lcd/v0.1.1/docs/images/v0.1.1-shader-vs-reflective-lcd-detail.png)

シェーダー側の発色領域がわずかに明るく、色味が少し異なるのは、移動式の環境光
反射帯でLUT適用後の輝度を補っているためです。これはLCD表面へ映り込む外光の
表現であり、内部バックライトではありません。参照写真には撮影時の光源と
カメラの応答も含まれます。

### 更新内容

- 格納先を`/storage/emulated/0/RetroArch/shaders/`へ変更し、
  **シェーダー > プリセットをロード**へ正しく表示されるようにしました。
- 完成版・既定の`native-lcd-v0.1.1`を
  `/storage/emulated/0/RetroArch/shaders/native-lcd-v0.1.1/`へ配置します。
- 旧`native-lcd-v0.1.0`も比較用として
  `/storage/emulated/0/RetroArch/shaders/native-lcd-v0.1.0/`へ同梱します。
- 固定された暗い4 x 8セル構造と、縦長楕円の発色領域を採用しました。
- 傾き連動の影を左右最大80px、上下最大180pxへ調整しました。
- 反射帯とグラデーションを外側`1.30`、内側`1.25`へ調整しました。
- 実験用プリセットをAPKの選択肢から除外しました。
- シェーダー単体ZIPへ6-passに必要な8ファイルを収録しました。

### インストール

`RetroArch-GBA-LCD-v0.1.1-KPA-arm64.apk`をインストールしてください。v0.1.0と
同じ正式署名鍵を使用しており、上書き更新できます。ユーザーデータは
`/storage/emulated/0/RetroArch-gyrotest/`以下に維持されます。

本APKはKONKR Pocket ADVANCE専用に調整・サポートしています。互換性、セーブ
データ、ライセンスの詳細は
[日本語README](https://github.com/game-de-it/gba-native-lcd/blob/v0.1.1/README_JA.md)を
参照してください。

### 検証情報

- パッケージ：`com.retroarch.aarch64`
- バージョン：`1.22.2_GBA_LCD_v0.1.1`
- APK SHA-256：`97ce9a3e23c99542a02d158ddc80f223aadb85a0bf26c102881e149b70d26071`
- シェーダーZIP SHA-256：`d121ccbb4db8e92747ab1bb9a0222091d97890a30e23353e67d7918d07f7b987`
- RetroArch改造ソース：[`06cc964`](https://github.com/game-de-it/RetroArch/commit/06cc9643c70a8ad3197259c24110eda32773eef6)

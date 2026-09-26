# GBA Native LCD v0.1.0

[English](#english) | [日本語](#日本語)

## English

The first release provides a custom Arm64 RetroArch build and reflective GBA
LCD profile made specifically for **KONKR Pocket ADVANCE (Android model:
GT78-VN)**.

It includes a 4x pixel matrix, 256-step RGB LUT, restrained LCD response,
recessed-bezel shadows, a soft environmental reflection, accelerometer-driven
lighting, bundled mGBA and AYANEO Equalizer compatibility.

### KPA-only

This build is calibrated and supported only for the KPA's 960 x 640 display,
panel response, sensor axes and AYANEO audio environment. It may technically
launch on another Arm64 Android device, but such use is unsupported.

### Installation and data

Install `RetroArch-GBA-LCD-v0.1.0-KPA-arm64.apk`. The blue launcher icon
identifies this build. Back up `retroarch.cfg` before uninstalling or clearing
app data. Saves, states and screenshots remain under
`/storage/emulated/0/RetroArch-gyrotest/`.

### Shader-only download

`GBA-Native-LCD-Shader-v0.1.0.zip` contains the seven required GLSL/LUT files,
MIT license and bilingual installation notes. It can be loaded by standard
RetroArch with the `gl` video driver, but tilt-driven lighting requires the
custom APK.

The shader is calibrated for the KPA's 960 x 640 panel and exact 4x GBA scale.
On another device, different output scale, panel color, pixel-based shadow
distances, missing sensor uniforms or GPU performance may cause uneven grids,
incorrect colors, static lighting or slowdown. Successful loading alone does
not mean the KPA-calibrated appearance is reproduced.

### Source and licenses

- [GBA Native LCD source](https://github.com/game-de-it/gba-native-lcd)
- [Modified RetroArch source commit](https://github.com/game-de-it/RetroArch/commit/7059a84431cd5c91f417a96250aa8ef088743792)
- Project files: MIT
- RetroArch: GPL-3.0+
- mGBA core: MPL-2.0

### Verification

- APK version: `1.22.2_GBA_LCD_0.1.0`
- ABI: `arm64-v8a`
- SHA-256: `caeb535c8947a745a0903b381ec1b2aa0dc58557231f8bb32fc037f9aa6b1fe0`
- Shader ZIP SHA-256:
  `6e32bd614374e44b85ab25f48850f1c9eaaeee11156352e4169db1cf7b2fb521`

The signed APK was verified on GT78-VN for GBA launch, shader rendering,
accelerometer lighting, physical controls and release-key reinstall.

---

## 日本語

初回リリースでは、**KONKR Pocket ADVANCE（Android model: GT78-VN）専用**の
反射型GBA液晶
プロファイルと、カスタムArm64版RetroArchを提供します。

4倍ドットマトリクス、256段階RGB LUT、控えめな液晶応答、ベゼルの影、柔らかな
環境光反射、加速度センサー連動光源、mGBAコア、AYANEO Equalizer対応を含みます。

### KPA専用

本ビルドはKPAの960 x 640液晶、パネル色特性、センサー軸、AYANEO音声環境に
合わせて調整・検証しています。他のArm64 Android端末で起動する可能性はありますが、
サポート対象外です。

### インストールとデータ

`RetroArch-GBA-LCD-v0.1.0-KPA-arm64.apk`をインストールしてください。青い
ランチャーアイコンが本ビルドの目印です。アンインストールやアプリデータ消去の前に
`retroarch.cfg`をバックアップしてください。セーブ、ステート、スクリーンショットは
`/storage/emulated/0/RetroArch-gyrotest/`以下へ保存されます。

### シェーダーのみのダウンロード

`GBA-Native-LCD-Shader-v0.1.0.zip`には、必須の7つのGLSL／LUTファイル、
MITライセンス、英語・日本語の導入説明が含まれます。標準RetroArchでも`gl`
ビデオドライバーで読み込めますが、傾き連動光源には専用APKが必要です。

本シェーダーはKPAの960 x 640液晶とGBAの正確な4倍表示に合わせて調整しています。
別端末では、表示倍率、パネル色、ピクセル単位の影距離、センサーuniformの有無、
GPU性能の違いにより、格子の不均一、色の変化、固定光源、速度低下が発生する可能性が
あります。読み込みに成功しても、KPA向けの見え方が再現できたとは限りません。

### ソースとライセンス

- [GBA Native LCDソース](https://github.com/game-de-it/gba-native-lcd)
- [RetroArch改造ソースのコミット](https://github.com/game-de-it/RetroArch/commit/7059a84431cd5c91f417a96250aa8ef088743792)
- プロジェクト独自部分: MIT
- RetroArch: GPL-3.0+
- mGBAコア: MPL-2.0

### 検証情報

- APKバージョン: `1.22.2_GBA_LCD_0.1.0`
- ABI: `arm64-v8a`
- SHA-256: `caeb535c8947a745a0903b381ec1b2aa0dc58557231f8bb32fc037f9aa6b1fe0`
- シェーダーZIP SHA-256:
  `6e32bd614374e44b85ab25f48850f1c9eaaeee11156352e4169db1cf7b2fb521`

正式署名APKをGT78-VNへ導入し、GBA起動、シェーダー表示、加速度センサー連動光源、
物理ボタン、正式鍵による上書き再インストールを確認済みです。

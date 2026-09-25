# GBA Native LCD v0.1.0

[English](#english) | [日本語](#日本語)

## English

The first release provides a custom Arm64 RetroArch build and reflective GBA
LCD profile made specifically for **KONKR Pocket ADVANCE / GT78-VN**.

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

The signed APK was verified on GT78-VN for GBA launch, shader rendering,
accelerometer lighting, physical controls and release-key reinstall.

---

## 日本語

初回リリースでは、**KONKR Pocket ADVANCE / GT78-VN専用**の反射型GBA液晶
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

正式署名APKをGT78-VNへ導入し、GBA起動、シェーダー表示、加速度センサー連動光源、
物理ボタン、正式鍵による上書き再インストールを確認済みです。

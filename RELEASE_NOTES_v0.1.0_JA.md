# GBA Native LCD v0.1.0

初回リリースでは、KONKR Pocket ADVANCE（Android model: GT78-VN）専用
プロファイルと、
加速度センサー対応のカスタムArm64版RetroArchを提供します。初代Game Boy
Advance純正反射型液晶のドット構造、落ち着いた色応答、奥まったパネルにできる影、
時間方向の柔らかさを再現します。本体を傾けると、影と環境光の反射帯が移動します。

## 同梱内容

- RetroArch 1.22.2ベースのArm64 APK
- mGBAコアと自動適用されるコアプリセット
- 5-pass GBA反射型LCDシェーダーと256段階RGB LUT
- 固定光源フォールバックを備えた加速度センサー連動光源
- AYANEO Equalizer対応OpenSL音声経路
- 英語・日本語ドキュメント

## KPA専用リリース

本リリースは960 x 640のKONKR Pocket ADVANCE（Android model: GT78-VN）専用
として設計、調整、
検証しています。4倍ドットマトリクス、RGB LUT、影の物理距離、センサー方向、
AYANEO Equalizer経路はKPA固有です。他のArm64 Android端末で起動する可能性は
ありますがサポート対象外であり、意図した表示や動きが再現できるとは限りません。

## 注意事項

- アンインストールやアプリデータ消去の前に`retroarch.cfg`をバックアップしてください。
- セーブ、ステート、スクリーンショット、プレイリストは
  `/storage/emulated/0/RetroArch-gyrotest/`以下へ保存されます。
- 今後の更新には同じ正式署名鍵が必要です。

## ライセンスとソース

本プロジェクト独自部分はMIT Licenseです。RetroArchはGPL-3.0+、同梱mGBAコアは
MPL-2.0のままで、ライセンス通知はAPK内に同梱されています。

- [GBA Native LCD source](https://github.com/game-de-it/gba-native-lcd)
- [Modified RetroArch source commit](https://github.com/game-de-it/RetroArch/commit/7059a84431cd5c91f417a96250aa8ef088743792)

## 検証情報

- APK: `RetroArch-GBA-LCD-v0.1.0-KPA-arm64.apk`
- SHA-256: `caeb535c8947a745a0903b381ec1b2aa0dc58557231f8bb32fc037f9aa6b1fe0`
- バージョン: `1.22.2_GBA_LCD_0.1.0`
- ABI: `arm64-v8a`

正式署名APKをGT78-VNへ導入し、GBA起動、シェーダー表示、加速度センサー連動光源、
物理ボタン、正式鍵による上書き再インストールを確認しました。上書き後も設定ファイルの
チェックサムと、共有セーブ／ステートのファイル数は維持されています。

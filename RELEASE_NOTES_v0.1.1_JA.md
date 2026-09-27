# GBA Native LCD v0.1.1

本リリースでは、**KONKR Pocket ADVANCE（Android model: GT78-VN）**向けの
反射型セル表現を完成させ、同梱RetroArchの既定シェーダーに設定しました。

## 表示比較

次の2枚はいずれも、**左がv0.1.1シェーダー、右が純正GBA反射型LCDを撮影した
写真**です。

![左：v0.1.1シェーダー、右：純正GBA反射型LCD](https://raw.githubusercontent.com/game-de-it/gba-native-lcd/v0.1.1/docs/images/v0.1.1-shader-vs-reflective-lcd-overview.png)

![左：v0.1.1シェーダーの拡大、右：純正GBA反射型LCD写真の拡大](https://raw.githubusercontent.com/game-de-it/gba-native-lcd/v0.1.1/docs/images/v0.1.1-shader-vs-reflective-lcd-detail.png)

シェーダー側の発色領域がわずかに明るく、写真と色味が少し異なるのは、移動式の
環境光反射帯を加えているためです。この反射帯は、落ち着いた色へ変換するLUTの後で
輝度を補い、LCD表面へ映り込む外光を表現します。内部バックライトを追加する処理
ではありません。また、参照写真には撮影時の光源とカメラの応答も含まれます。

## 更新内容

- シェーダーの格納先を`/storage/emulated/0/RetroArch/shaders/`へ変更し、
  RetroArchの**シェーダー > プリセットをロード**に正しく表示されるようにしました。
- 完成版`native-lcd-v0.1.1`を新しい既定mGBAプリセットにしました。
  格納先は`/storage/emulated/0/RetroArch/shaders/native-lcd-v0.1.1/`です。
- 旧シェーダー`native-lcd-v0.1.0`も比較用として同梱しています。
  格納先は`/storage/emulated/0/RetroArch/shaders/native-lcd-v0.1.0/`です。
- 固定された暗い4 x 8セル構造の中に、縦長楕円の発色領域を形成する方式へ変更し、
  黒い境界をぼかさずに反射型LCDらしいドットの質感を再現しました。
- 傾き連動の影を再調整しました。左右の影は最大80px、上下は最大180pxです。
- 明るい枠のように見える状態を避けるため、移動式反射帯とグラデーションを調整し、
  外側を`1.30`、内側の絶対光量を`1.25`にしました。
- 実験用シェーダーをAPKの選択肢から除外し、完成版と旧版だけを残しました。
- シェーダー単体ZIPへ、6-passプリセットに必要な8ファイルをすべて収録しました。

## インストールと更新

`RetroArch-GBA-LCD-v0.1.1-KPA-arm64.apk`をインストールしてください。v0.1.0と
同じ正式署名鍵を使用するため、上書き更新できます。セーブ、ステートなどの共有
データは`/storage/emulated/0/RetroArch-gyrotest/`以下に維持されます。
アンインストール、アプリデータ消去、Androidのパッケージ領域変更を行う前に、
`retroarch.cfg`をバックアップしてください。

本APKはKONKR Pocket ADVANCE専用に調整・サポートしています。他のArm64 Android
端末で起動する可能性はありますが、パネル色、セル倍率、センサー軸、操作、
AYANEO Equalizer連携は保証されません。

## ダウンロード

- `RetroArch-GBA-LCD-v0.1.1-KPA-arm64.apk`
- `GBA-Native-LCD-Shader-v0.1.1.zip`
- `SHA256SUMS`

## 検証情報

- パッケージ：`com.retroarch.aarch64`
- バージョン：`1.22.2_GBA_LCD_v0.1.1`
- APK SHA-256：`97ce9a3e23c99542a02d158ddc80f223aadb85a0bf26c102881e149b70d26071`
- シェーダーZIP SHA-256：`d121ccbb4db8e92747ab1bb9a0222091d97890a30e23353e67d7918d07f7b987`
- RetroArch改造ソース：[`06cc964`](https://github.com/game-de-it/RetroArch/commit/06cc9643c70a8ad3197259c24110eda32773eef6)

## ライセンス

本プロジェクト独自部分はMIT Licenseです。RetroArchはGPL-3.0-or-later、同梱mGBA
コアはMPL-2.0のままで、各ライセンス通知はAPK内に収録しています。

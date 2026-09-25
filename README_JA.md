# GBA Native LCD

[English](README.md) | **日本語**

GT78-VN Androidハンドヘルド向けのRetroArch GLSLシェーダープロジェクトです。
CRTや現代的なIPS液晶、過度に強調されたピクセルグリッドではなく、
初代Game Boy Advanceの純正液晶を控えめに再現することを目指しています。

本シェーダーは測色器から生成したディスプレイプロファイルではなく、知覚的な
再現です。純正反射型GBA液晶の写真とKONKR Pocket ADVANCE上の表示を繰り返し
比較しながら初期値を調整しました。表示モデルは、ドット構造、色応答、ベゼルの
影、任意の環境光反射という、個別に理解できる4つの要素に分かれています。

## ダウンロード

正式署名済みKPA用APKと`SHA256SUMS`は、
[最新のGitHubリリース](https://github.com/game-de-it/gba-native-lcd/releases/latest)から
ダウンロードできます。本パッケージのサポート対象はKONKR Pocket ADVANCE /
GT78-VNのみです。

## 表示比較

RetroArchのスクリーンショットは、実際の液晶パネルへ表示される前のレンダリング
結果です。

| シェーダーOFF | シェーダーON |
| --- | --- |
| ![シェーダー未適用のRetroArch出力](docs/images/shader-off.png) | ![反射型GBA液晶シェーダー適用後](docs/images/shader-on.png) |

次の写真は、KONKR Pocket ADVANCE実機上で同じ比較を撮影したものです。
上段がシェーダーOFF、下段がシェーダーONです。デジタルキャプチャとは異なり、
対象パネルの輝度、視野角、表面反射、カメラの応答も含まれています。

![実機比較：上段がシェーダーOFF、下段がシェーダーON](docs/images/physical-comparison-shader-off-on.jpeg)

## 表示モデル

### 1. ドット構造

GBAの240 x 160映像を、対象機の960 x 640パネルへ正確に4倍で対応させます。
そのため、GBAの1ピクセルは出力側の安定した4 x 4ピクセル領域になります。
3列にB、G、Rの控えめな透過特性を与え、4列目と4行目をセル間の暗い
マトリクス境界として扱います。

| パラメータ | 初期値 | 目的 |
| --- | ---: | --- |
| `MATRIX_FACE` | `1.00` | 発色領域の光透過率 |
| `MATRIX_GAP` | `0.66` | マトリクス境界の透過率を34%まで低下 |
| `SUBPIXEL_STRENGTH` | `0.22` | BGR分離を見せながら過度な強調を抑制 |
| `SRC_BLEND` | `0.04` | 元ピクセルの色を上下左右へ4%混合 |
| `OPTICS_CHROMA` | `0.04` | カバー層における小さな色クロストーク |
| `OPTICS_LUMA` | `0.02` | カバー層における、さらに小さな輝度クロストーク |

虹色の分離よりも、暗いマトリクスを重視しています。小さな隣接画素混合により、
リニアフィルタリングや画面全体へのブラーを使わず、現代のIPS液晶では硬すぎる
輪郭を和らげます。

### 2. 色応答

色補正はLCDマトリクス処理の前に、R/G/B各チャンネル独立の256段階LUTを
100%の強度で適用します。この補正は単一の明るさ、彩度、ガンマ値では表現
できません。代表的なLUT値は次のとおりです。

| 入力 | R | G | B |
| ---: | ---: | ---: | ---: |
| 0 | 20 | 17 | 19 |
| 128 | 29 | 27 | 40 |
| 192 | 39 | 39 | 52 |
| 240 | 62 | 61 | 59 |
| 255 | 80 | 79 | 78 |

`RGB_CURVE_STRENGTH`は`1.00`です。このLUTは現代の液晶が出力する明るく
鮮やかな色を強く圧縮し、参照写真に見られる、くすんだ中間色、抑えられた
赤と緑、わずかに寒色寄りの暗部へ変換します。その後の光源処理で、発光する
バックライトではなく、外光の反射として輝度を補います。

これらの値は対象機と参照写真に合わせたものです。Android端末のパネル、
画面輝度、メーカー独自のカラーマネジメントが異なる場合は、別のLUTが必要に
なる可能性があります。

### 3. ベゼルの影と反射光

初代GBAの液晶は反射型で内部バックライトを持たず、前面レンズへ完全密着
していないため、その奥に配置されています。そのため、発光型のライトカーブを
追加するのではなく、奥まった液晶面へ外光が当たる状態をモデル化しています。

センサー光源が有効な場合、端末を水平に置いた状態では上下左右に30ピクセルの
影ができます。端末を傾けると、持ち上がった辺の影は最大180ピクセルまで伸び、
反対側の影は消えていきます。影の根元は輝度係数`0.25`から始まり、最大まで
伸びると`0.10`になります。画面下部の反射光は`1.00`から`1.80`へ増加します。

加速度センサーにはデッドゾーンを設けず、`0.20`のローパス係数を使用します。
これにより追従性を維持しながら、ボタン操作の衝撃や手の細かな震えによる点滅を
抑えます。距離と光量は960 x 640の対象機に合わせた視覚調整値であり、純正
本体をミリメートル単位で測定した値ではありません。

センサー情報を利用できない環境では、固定された上方光源へフォールバック
します。0～29行は`0.25`から`0.50`、30～179行は`0.50`から通常光、
180～639行は`1.00`から`1.80`へ変化します。

### 4. 任意の環境光反射

柔らかな横方向の反射帯は、すべての純正GBA液晶に常時存在する特徴として
再現したものではありません。窓や天井照明などの局所光源が反射型液晶面へ
映り込む状態を抽象化した演出です。四角い境界は持たず、端末の傾きに応じて
移動します。

| パラメータ | 初期値 | 目的 |
| --- | ---: | --- |
| `BAND_LIGHT` | `1.80` | 広い反射帯の最大光量 |
| `BAND_WIDTH` | `0.46` | 広い反射帯の横方向半径 |
| `BAND_HEIGHT` | `0.168` | ガウス分布による縦方向の広がり |
| `BAND_TRAVEL` | `0.30` | 傾きに応じた正規化最大移動量 |
| `INNER_BAND_LIGHT` | `1.65` | 内側の柔らかな領域の絶対光量 |
| `INNER_BAND_WIDTH` | `0.16` | 内側中心部の横方向半径 |
| `INNER_BAND_HEIGHT` | `0.04` | 内側中心部の縦方向半径 |
| `INNER_BAND_FADE_WIDTH` | `0.38` | 横方向のフェード範囲 |
| `INNER_BAND_FADE_HEIGHT` | `0.14` | 縦方向のフェード範囲 |

内側の領域は、外側の`1.80`へ乗算するのではなく、絶対光量`1.65`へ収束
します。これにより中央が白くクリップした帯になることを防ぎ、均一すぎない
反射面にしています。液晶パネル自体の再現だけを求める場合は、
`BAND_LIGHT`と`INNER_BAND_LIGHT`を両方`1.00`に設定すると、マトリクス、
LUT、ベゼル影へ影響を与えず反射帯だけを無効化できます。

### 時間方向の応答

LCDの時間方向の応答は、4つの空間的要素とは別に適用されます。明転時の
追従速度は`0.81`で、暗転時には最大6フレームまで減衰する残像を保持します。
Game Gear比較用シェーダーのSTN液晶応答よりも、短く弱い効果です。

## 内容

- `variants/gba-reflective-v2.glslp`：現在の5-passリリースプリセット
- `variants/rgb-curve-lut.glsl`：256段階RGB色補正
- `variants/gba-reflective-ghost.glsl`：時間方向のLCD応答
- `variants/gba-reflective-response.glsl`：元セルの光学応答
- `variants/gba-reflective-matrix.glsl`：BGRマトリクス、影、反射
- `variants/gba-reflective-optics.glsl`：最終カバー層のクロストーク
- `reference/device-profile.md`：対象機で確認した構成
- `reference/tuning-notes.md`：視覚的な設計意図とパラメータ説明
- `reference/photos/`：ユーザー提供の純正GBA SP液晶写真
- `captures/`：調整中に使用した適用前後の実機キャプチャ
- `docs/images/`：README用スクリーンショットと実機比較写真

## Androidでのテストパス

手動でテストする場合は、`variants/`内のファイルをまとめて次の場所へ配置します。

`/storage/emulated/0/RetroArch/shaders/gba-reflective-v2/`

RetroArchの**Load Preset**から`gba-reflective-v2.glslp`を読み込みます。
プリセット、LUT、シェーダーファイルは同じディレクトリへ置いてください。
Android用コアプリセットは、mGBA起動時に自動的に読み込みます。画面比較と
性能確認が完了するまでは、グローバルプリセットとして保存しないでください。

現在のバージョンはリニアフィルタリングや発光型バックライトを使用しません。
パネルの柔らかさは、中心輝度を維持した色拡散によって作られます。照明は上部の
ベゼル影を含む、方向性のある反射光フィールドです。

## リリースAPKへの統合

リリースAPKには、5-passプリセット、LUT、mGBAコア、メニューアセット、
調整済み設定が含まれます。管理対象のシェーダーファイルをアプリのプライベート
ディレクトリへ配置し、mGBA用コアプリセットを自動適用します。セーブデータ、
ステート、スクリーンショット、プレイリストは書き込み可能な共有ストレージへ
保存されます。

ホーム画面では、標準RetroArchと見分けられるように青色
（`RGB 48, 65, 160`）のアイコンで表示されます。ランチャーによってアプリ名が
省略表示される場合もありますが、この青いアイコンが**RetroArch GBA LCD**です。

![標準RetroArchの隣に青いRetroArch GBA LCDアイコンが表示されたKPAホーム画面](docs/images/kpa-home-retroarch-icon.png)

センサー連動光源には、GLSLパイプラインへ加速度センサーuniformを追加した
同梱RetroArchビルドが必要です。標準RetroArchでも固定光源のフォールバックは
描画できますが、端末の傾きに合わせてベゼル影や反射帯を動かすことはできません。

### KPA専用リリース

このAPKは**KONKR Pocket ADVANCE / GT78-VN専用**としてリリースします。
汎用Android表示プロファイルではありません。KPAの960 x 640パネル、GBAの
240 x 160映像の正確な4倍表示、実測したパネル色特性、横持ち時のセンサー軸、
AYANEOシステム音声を前提に設計しています。

解像度が異なる場合も描画自体は可能ですが、4 x 4セルとピクセル単位の影距離は
意図した物理スケールから外れます。パネルが異なれば色LUTも作り直す必要があり、
センサー軸の入れ替えや反転が必要になる場合もあります。AYANEO Equalizer対応は、
互換性のあるAndroid Dynamics Processingエフェクトを提供するファームウェアに
限られます。

APKに機種名による強制的な起動制限はないため、別のArm64 Android端末で起動する
可能性はあります。ただし、その利用はサポート対象外です。表示精度、センサー方向、
操作、性能、システムEQ連携は保証されません。別機種では専用プロファイルを調整し、
実機上で改めて検証する必要があります。

### AYANEO Equalizer対応

このAPKは、対象機のAYASpace／AYANEOシステムソフトウェアが提供する
**AYANEO Equalizer**に対応しています。これは実機UIに表示される名称です。
[AYANEOの公開AYASpaceページ](https://www.ayaneo.com/ayaspace)ではシステムレベルのサウンドエフェクトについて
説明されていますが、このAndroid EQについて、これ以上に固有の製品名は現在
公開されていません。

標準RetroArchの低遅延OpenSL経路では、システムの音声エフェクトを迂回して
いました。このビルドでは、エフェクトを利用できるOpenSLパフォーマンスモードを
要求し、AYASpaceのAndroid `Dynamics Processing`エフェクトが48 kHzの
RetroArch音声セッションへ接続できるようにしています。EQ自体はこのAPKに
内蔵されていないため、AYASpace側で有効化・調整する必要があります。

エフェクト対応経路では、元の高速経路より大きな音声バッファが報告されます。
AudioFlinger上の計測値は約42 msから約82 msへ増えましたが、EQのON・OFF
いずれでも通常プレイ中に体感できる音声遅延は確認されませんでした。

### セーブデータと注意事項

APKのパッケージIDは`com.retroarch.aarch64`です。960 x 640の
GT78-VN／KONKR Pocket ADVANCE構成を対象としています。標準版の
`com.retroarch`とは別アプリとしてインストールされ、標準版の設定は共有しません。

ユーザーデータは、アプリが管理するプライベートファイルとは別に保存されます。

| データ | 保存先 |
| --- | --- |
| バッテリーセーブ | `/storage/emulated/0/RetroArch-gyrotest/saves/` |
| セーブステート | `/storage/emulated/0/RetroArch-gyrotest/states/` |
| スクリーンショット | `/storage/emulated/0/RetroArch-gyrotest/screenshots/` |
| プレイリスト | `/storage/emulated/0/RetroArch-gyrotest/playlists/` |
| BIOS／システムファイル | `/storage/emulated/0/RetroArch-gyrotest/system/` |
| メイン設定 | `/storage/emulated/0/Android/data/com.retroarch.aarch64/files/retroarch.cfg` |

同じ署名のAPKで上書き更新した場合、セーブ、ステート、通常設定は維持されます。
Bundle version 3では、入力ポーリングをLateへ変更し、VRR専用の
Sync to Exact Content Framerateを無効化する移行を一度だけ実行します。
それ以降にユーザーが変更した値は維持されます。

APKをアンインストールしても共有領域の`RetroArch-gyrotest`は残る想定ですが、
Androidはパッケージ固有の`Android/data`ディレクトリを削除する可能性があり、
`retroarch.cfg`も失われる場合があります。アンインストールやアプリデータ消去の
前に設定をバックアップしてください。未バックアップのセーブやBIOSがある場合は、
`RetroArch-gyrotest`を削除しないでください。

AndroidでAPKを上書き更新するには、以前と同じ署名鍵が必要です。
v0.1.0リリースAPKは、[`SIGNING_CERTIFICATE.md`](SIGNING_CERTIFICATE.md)に
記載した永続的な正式証明書で署名されています。今後の全バージョンでも同じ秘密鍵を
使用する必要があります。以前の開発用鍵で署名したテスト版から切り替える場合は、
既存パッケージのアンインストールが必要になり、前述のパッケージ固有設定が削除される
可能性があります。

リリース準備の進捗と公開に関する残作業は
[`RELEASE_CHECKLIST.md`](RELEASE_CHECKLIST.md)にまとめています。

## ライセンス

本プロジェクト独自のシェーダー、ツール、ドキュメントは
[MIT License](LICENSE)で公開します。同梱APKにはGPL-3.0+のRetroArchと、
MPL-2.0のmGBA libretroコアも含まれます。各ライセンス本文とサードパーティ通知は
APK内に同梱されています。MITライセンスがこれらのライセンスを置き換えるものでは
ありません。

v0.1.0で使用したRetroArch改造ソースは、
[game-de-itのRetroArchフォーク](https://github.com/game-de-it/RetroArch/commit/7059a84431cd5c91f417a96250aa8ef088743792)で公開しています。

## Androidコアプリセットのフォールバック

このRetroArchビルドでは、ダウンロードしたシェーダーがアプリのプライベート
ストレージへ保存されるため、外部の`.glslp`ファイルが一覧へ表示されない場合が
あります。その場合は`core-presets/mGBA/gba.glslp`を次の場所へ配置します。

`/storage/emulated/0/RetroArch/config/mGBA/gba.glslp`

このファイルは外部プロジェクトのプリセットを絶対パスで参照し、mGBAの
コンテンツ起動時に適用します。以前のコアプリセットは
`backups/gba-online-updater.glslp`へ保存されています。

## macOSでのプレビュー

`tools/render_preview.py`は、シェーダー未適用のキャプチャに現在のプリセットを
CPUで近似適用します。リリース用パラメータとRGB LUTを読み込み、レンダリング
したPNGと、シェーダー未適用画像・CPUプレビュー・純正液晶写真を並べた比較画像を
生成します。

```sh
python3 tools/render_preview.py \
  --preset variants/gba-reflective-v2.glslp \
  --lut variants/rgb_curve_lut.png
```

標準の出力先は`captures/preview-current.png`と
`captures/preview-current-comparison.png`です。NumPyとPillowが必要です。

<div align="center">

<img src="docs/assets/logo.png" width="128" alt="SayaTech-Midi-Studio Logo">

# SayaTech-Midi-Studio

**Windows 向けの MIDI 自動演奏スタジオ。ピアノ / ドラム演奏、自動調整、スプラッシュ画面、テーマ、ガラス風 UI を搭載。**

[简体中文](README.md) · [English](README.en.md) · [日本語](README.ja.md)
[![Repository](https://img.shields.io/badge/GitHub-ShiroiSaya%2FSayaTech-Midi-Studio-181717?logo=github)](https://github.com/ShiroiSaya/SayaTech-Midi-Studio)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**リポジトリ:** <https://github.com/ShiroiSaya/SayaTech-Midi-Studio>

```bash
git clone https://github.com/ShiroiSaya/SayaTech-Midi-Studio.git
cd SayaTech-Midi-Studio
```


<img src="docs/assets/banner.png" alt="SayaTech-Midi-Studio Banner">

</div>

## プレビュー

アプリケーションはモダンなフロストガラス風インターフェースデザインを採用し、ライトモードとダークモードの両方に対応しています。

- **メイン画面**：ピアノ、ドラムワークスペース、設定パネルへの素早い切り替えが可能なクリアなナビゲーションバー
- **ピアノワークスペース**：リアルタイムの MIDI ノート表示、ベロシティパラメータ、時間ウィンドウ設定、自動チューニング機能対応
- **ドラムワークスペース**：独立したドラムキットパラメータ設定、複数のドラム音色と演奏モードに対応
- **設定パネル**：ホットキーバインディング、テーマ選択、起動オプションなどを含む統一設定センター
- **スプラッシュ画面**：オプションのアニメーション起動画面でアプリケーション起動体験を向上
- **ダークモード**：背景画像を自動的に無効化して可読性を向上、快適な夜間使用体験を提供

## 主な機能

- ピアノ MIDI 自動演奏
- ドラム MIDI 自動演奏
- 自動チューニングとパラメータ提案
- 短音域向け固定ウィンドウロジック
- 北京時間同期付きの合奏タイマー
- ホットキーのカスタマイズ
- 複数テーマ、ダークモード、ガラス風 UI
- オプションのスプラッシュ画面
- ホバー説明と分かりやすいパラメータ名
- クラッシュログと実行ログ

## 動作環境

- Windows 10 / 11
- Python 3.10+
- PySide6 ベースの GUI 環境
- ゲームやウィンドウへキーボード入力を送る用途に適しています

## ダウンロードと Release

- GitHub Releases に掲載する推奨インストーラー名: `SayaTech_MIDI_Studio_Setup.exe`
- 単体実行版のファイル名: `SayaTech_MIDI_Studio.exe`
- 推奨 Release ページ: <https://github.com/ShiroiSaya/SayaTech-Midi-Studio/releases>

## クイックスタート

```bash
git clone https://github.com/ShiroiSaya/SayaTech-Midi-Studio.git
cd SayaTech-Midi-Studio
pip install -r requirements.txt
python app.py
```

## ビルド

### 単一 EXE
同梱のビルドスクリプト、または PyInstaller でパッケージ化できます。出力ファイル名は `dist/SayaTech_MIDI_Studio.exe` です。

### インストーラー版
起動速度を優先する場合は、`onedir + Inno Setup` の構成がおすすめです。インストーラーの出力ファイル名は `installer_output/SayaTech_MIDI_Studio_Setup.exe` に固定されています。

## ハイライト

このプロジェクトは単なるスクリプト集ではなく、MIDI 自動演奏のための一連のワークフローを提供します。

- 統一されたデスクトップ UI
- ピアノ / ドラムの独立ワークスペース
- 実行時パラメータと連動する自動チューナー
- 一元化された設定画面
- スプラッシュ画面とテーマ切替
- 配布向けのパッケージング手段

## リポジトリ構成

```text
.
├─ app.py
├─ sayatech_modern/
├─ docs/
│  └─ assets/
├─ scripts/
├─ SayaTech_MIDI_Studio_onefile.spec
├─ SayaTech_MIDI_Studio_onedir.spec
├─ installer.iss
├─ config.txt
├─ config.example.txt
├─ requirements.txt
└─ LICENSE
```

## 補足

- ライトモードでは背景画像とガラス効果が使えます
- ダークモードでは可読性のため背景画像を自動で無効化します
- 初回起動時はリポジトリ内の `config.txt` を優先して読み込み、存在しない場合は既定テンプレートから再生成します
- README のスクリーンショットは最近の UI バージョンから取得しています
- Release には `SayaTech_MIDI_Studio_Setup.exe` をアップロードする構成を想定しており、ビルド済みバイナリはソースリポジトリに含めません

## License

このプロジェクトは **MIT License** で公開されています。詳細は [LICENSE](LICENSE) をご確認ください。

## Dependencies

実行時とパッケージング時の依存関係は [requirements.txt](requirements.txt) にまとめてあります。

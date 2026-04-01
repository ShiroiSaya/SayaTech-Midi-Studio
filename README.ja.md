<div align="center">

<img src="docs/assets/logo.png" width="128" alt="SayaTech-Midi-Studio Logo">

# SayaTech-Midi-Studio

**「星痕共鸣」のゲーム内楽器演奏向け Windows 用 MIDI 自動演奏ツール。**  
ピアノ / ドラムの 2 モード、自動調整、合奏タイマー、テーマ切替、モダンなデスクトップ UI を備えています。

[简体中文](README.md) · [English](README.en.md) · [日本語](README.ja.md)

[![Repository](https://img.shields.io/badge/GitHub-ShiroiSaya%2FSayaTech-Midi-Studio-181717?logo=github)](https://github.com/ShiroiSaya/SayaTech-Midi-Studio)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

<img src="docs/assets/banner.png" alt="SayaTech-Midi-Studio Banner">

</div>

## 概要

SayaTech-Midi-Studio は、MIDI ファイルをキーボード入力へ変換し、「星痕共鸣」のゲーム内楽器演奏に利用するためのデスクトップツールです。GUI を中心に構成されており、ピアノとドラムの独立したワークフローに加えて、音域適応、右シフトウィンドウ、ペダル処理、自動調整、合奏時刻指定、再生プレビューなどを備えています。

単なるスクリプト集ではなく、実際に使いやすく、配布しやすい構成を意識したデスクトップアプリとして整理されています。

- グラフィカルなメイン画面と設定パネル
- ピアノ / ドラムの独立ワークスペース
- トラック選択、ピアノロール、ドラムレーンのプレビュー
- 自動調整機能と編集可能な設定テンプレート
- テーマ、ダークモード、ガラス風背景、スプラッシュ画面
- 配布向けのビルド / インストーラースクリプト

## プレビュー

### メイン画面
![Home](docs/assets/screenshot-home-empty.png)

### ピアノモード
![Piano](docs/assets/screenshot-piano.png)

### ドラムモード
![Drum](docs/assets/screenshot-drum.png)

### 設定画面
![Settings](docs/assets/screenshot-settings.png)

### スプラッシュ画面
![Splash](docs/assets/screenshot-splash.png)

### ダークモード
![Dark Mode](docs/assets/screenshot-dark.png)

## 主な機能

### 再生機能
- ピアノ MIDI 自動演奏
- ドラム MIDI 自動演奏
- 再生 / 一時停止 / 停止ホットキー
- MIDI トラックの絞り込みと推奨選択
- ピアノロール、ドラムプレビュー、波形による位置確認

### 音域・キー適応
- 自動音域適応
- 右シフトウィンドウと短音域固定ウィンドウ
- ペダル処理と再トリガー制御
- ピアノ / ドラム別の独立パラメータ
- 既定テンプレート付きの `config.txt`

### 補助機能
- 合奏タイマー
- 北京時間との時刻同期
- 自動調整とパラメータ提案
- 実行ログとクラッシュログ

### UI と操作性
- 複数テーマ
- ダークモード
- ガラス風背景効果
- 任意のスプラッシュ画面
- 分かりやすいパラメータ名とホバー説明

## 動作環境

- Windows 10 / 11
- Python 3.10+
- PySide6 ベースの GUI 環境
- 「星痕共鸣」で MIDI をキーボード入力へ変換して演奏する用途を想定

## インストールと実行

### ソースから起動

```bash
git clone https://github.com/ShiroiSaya/SayaTech-Midi-Studio.git
cd SayaTech-Midi-Studio
pip install -r requirements.txt
python app.py
```

### Release 名称

ソースリポジトリにはビルド済みバイナリを含めていません。Release 用の推奨ファイル名は以下です。

- `SayaTech_MIDI_Studio_Setup.exe`：Windows インストーラー
- `SayaTech_MIDI_Studio.exe`：単体実行版

Release ページ：<https://github.com/ShiroiSaya/SayaTech-Midi-Studio/releases>

## ビルド

### 単一 EXE
付属スクリプト、または PyInstaller でビルドできます。

- 出力：`dist/SayaTech_MIDI_Studio.exe`

### インストーラー
推奨構成は `onedir + Inno Setup` です。

- ディレクトリ版：`dist/SayaTech_MIDI_Studio/`
- インストーラー版：`installer_output/SayaTech_MIDI_Studio_Setup.exe`

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

- ライトモードでは背景画像とガラス風効果が利用できます
- ダークモードでは視認性のため背景画像を自動で無効化します
- `config.txt` が存在しない場合は既定テンプレートから再生成されます
- README のスクリーンショットは現行プロジェクト UI のものです

## License

本プロジェクトは [MIT License](LICENSE) のもとで公開されています。

<p align="center">
  <img src="docs/assets/logo.png" alt="SayaTech-Midi-Studio Logo" width="120" />
</p>

<h1 align="center">SayaTech-Midi-Studio</h1>

<p align="center">
  面向《星痕共鸣》的 Windows MIDI 自动演奏工具
</p>

<p align="center">
  <a href="README.md">简体中文</a> ·
  <a href="README.en.md">English</a> ·
  <a href="README.ja.md">日本語</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Platform-Windows%2010%20%2F%2011-4c8bf5" alt="Platform" />
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB" alt="Python" />
  <img src="https://img.shields.io/badge/License-MIT-111111" alt="License" />
</p>

<p align="center">
  <img src="docs/assets/banner.svg" alt="SayaTech-Midi-Studio Banner" />
</p>

## 项目简介

SayaTech-Midi-Studio 用于将 MIDI 文件转换为键盘输入，服务于《星痕共鸣》的游戏内乐器演奏场景。项目以桌面 GUI 为核心，提供两类工作台：

- **钢琴 / 吉他 / 贝斯**
- **架子鼓**

它不是单纯的脚本打包，而是一套更适合日常使用、调参、测试与分发的桌面工具。围绕游戏内演奏的实际需求，项目集成了轨道筛选、可视化预览、区间移动、踏板识别、自动调参、合奏定时与现代化界面。

## 预览

### 主界面
![Home](docs/assets/home.png)

### 钢琴 / 吉他 / 贝斯
![Piano](docs/assets/piano.png)

### 架子鼓
![Drum](docs/assets/drum.png)

### 设置
![Settings](docs/assets/settings.png)

### 夜间模式
![Dark Mode](docs/assets/dark.png)

## 功能特性

### 演奏与播放
- 钢琴 / 吉他 / 贝斯 MIDI 自动演奏
- 架子鼓 MIDI 自动演奏
- 播放 / 暂停 / 停止热键
- MIDI 轨道筛选与推荐
- 钢琴卷帘预览、鼓轨实时预览、时间轴拖动跳转

### 音域与映射
- 自动适配可弹音域
- 区间移动逻辑
- 踏板识别与重触发控制
- 钢琴 / 吉他 / 贝斯与架子鼓独立参数
- 可编辑 `config.txt` 与默认配置模板

### 自动调参与工具能力
- 自动调参与参数建议
- 合奏定时
- 北京时间校时
- 运行日志与崩溃日志

### 界面体验
- 多主题外观
- 夜间模式
- 毛玻璃背景效果
- 可选启动动画
- 更直观的参数命名与悬停说明

## 适用环境

- Windows 10 / 11
- Python 3.10+
- PySide6 图形界面环境
- 适用于《星痕共鸣》内需要将 MIDI 映射为键盘输入的乐器演奏场景

## 安装与运行

### 从源码启动

```bash
git clone https://github.com/ShiroiSaya/SayaTech-Midi-Studio.git
cd SayaTech-Midi-Studio
pip install -r requirements.txt
python app.py
```

### Release 文件命名

仓库源码默认不包含已构建二进制文件。发布版本建议使用以下名称：

- `SayaTech_MIDI_Studio_Setup.exe`：Windows 安装包
- `SayaTech_MIDI_Studio.exe`：单文件便携版

Release 页面：<https://github.com/ShiroiSaya/SayaTech-Midi-Studio/releases>

## 构建

### 单文件 EXE
使用项目内脚本或直接通过 PyInstaller 构建：

- 输出：`dist/SayaTech_MIDI_Studio.exe`

### 安装版
推荐使用 `onedir + Inno Setup` 生成安装程序：

- 目录版输出：`dist/SayaTech_MIDI_Studio/`
- 安装包输出：`installer_output/SayaTech_MIDI_Studio_Setup.exe`

## 仓库结构

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

## 使用说明

- 浅色模式支持背景图与毛玻璃效果
- 夜间模式会自动关闭背景图，以保证界面对比度与可读性
- 架子鼓参数页与钢琴 / 吉他 / 贝斯参数页相互独立
- 自动调参生成的建议，适合先回填再试听，不建议盲目一次性覆盖全部习惯参数

## 许可协议

本项目采用 [MIT License](LICENSE)。

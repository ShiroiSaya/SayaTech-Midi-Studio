<div align="center">

<img src="docs/assets/logo.png" width="128" alt="SayaTech-Midi-Studio Logo">

# SayaTech-Midi-Studio

**A Windows MIDI auto-play tool for the in-game instruments of “星痕共鸣”.**  
It includes piano and drum modes, auto tuning tools, ensemble timing, theme customization, and a modern desktop UI.

[简体中文](README.md) · [English](README.en.md) · [日本語](README.ja.md)

[![Repository](https://img.shields.io/badge/GitHub-ShiroiSaya%2FSayaTech-Midi-Studio-181717?logo=github)](https://github.com/ShiroiSaya/SayaTech-Midi-Studio)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

<img src="docs/assets/banner.png" alt="SayaTech-Midi-Studio Banner">

</div>

## Overview

SayaTech-Midi-Studio converts MIDI files into keyboard input for the instrument gameplay of “星痕共鸣”. The project is built around a desktop GUI and provides separate piano and drum workflows, together with range adaptation, shifted-window logic, pedal handling, auto tuning, ensemble scheduling, and playback visualization.

Instead of being just a loose collection of scripts, it is structured as a desktop tool that is easier to run, configure, and distribute:

- graphical main window and parameter panels
- dedicated piano and drum workspaces
- track selection, piano-roll preview, and drum-lane preview
- auto-tuning tools and editable config templates
- themes, dark mode, glass-style background, and splash screen
- packaging scripts for portable builds and installers

## Preview

### Main screen
![Home](docs/assets/screenshot-home-empty.png)

### Piano mode
![Piano](docs/assets/screenshot-piano.png)

### Drum mode
![Drum](docs/assets/screenshot-drum.png)

### Settings
![Settings](docs/assets/screenshot-settings.png)

### Splash screen
![Splash](docs/assets/screenshot-splash.png)

### Dark mode
![Dark Mode](docs/assets/screenshot-dark.png)

## Features

### Playback
- piano MIDI auto-play
- drum MIDI auto-play
- play / pause / stop hotkeys
- MIDI track filtering and recommendations
- piano-roll preview, drum preview, and waveform-based navigation

### Range and key mapping
- automatic range adaptation
- shifted window and fixed short-range window logic
- pedal handling and retrigger controls
- separate parameter sets for piano and drums
- editable `config.txt` with default template

### Utility features
- ensemble timing
- Beijing time synchronization
- auto tuning and parameter suggestions
- runtime logs and crash logs

### UI and workflow
- multiple visual themes
- dark mode
- glass-style background effect
- optional splash screen
- clearer parameter names and hover descriptions

## Environment

- Windows 10 / 11
- Python 3.10+
- PySide6 GUI environment
- Intended for “星痕共鸣” instrument playback scenarios that require MIDI-to-keyboard input mapping

## Installation and Run

### Run from source

```bash
git clone https://github.com/ShiroiSaya/SayaTech-Midi-Studio.git
cd SayaTech-Midi-Studio
pip install -r requirements.txt
python app.py
```

### Release naming

Prebuilt binaries are not tracked in the source repository. Recommended asset names for releases:

- `SayaTech_MIDI_Studio_Setup.exe` — Windows installer
- `SayaTech_MIDI_Studio.exe` — one-file portable build

Releases page: <https://github.com/ShiroiSaya/SayaTech-Midi-Studio/releases>

## Build

### One-file EXE
Build with the included scripts or with PyInstaller directly:

- output: `dist/SayaTech_MIDI_Studio.exe`

### Installer
`onedir + Inno Setup` is the recommended packaging flow:

- directory build: `dist/SayaTech_MIDI_Studio/`
- installer build: `installer_output/SayaTech_MIDI_Studio_Setup.exe`

## Repository Structure

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

## Notes

- Light mode supports the background image and glass-style effect
- Dark mode disables the background image automatically for readability
- The application reads `config.txt` first and regenerates it from the default template when missing
- Screenshots in this README are taken from the current project UI

## License

Released under the [MIT License](LICENSE).

<p align="center">
  <img src="docs/assets/logo.png" alt="SayaTech-Midi-Studio Logo" width="120" />
</p>

<h1 align="center">SayaTech-Midi-Studio</h1>

<p align="center">
  A Windows MIDI auto-play tool for the in-game instruments of “星痕共鸣”
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

## Overview

SayaTech-Midi-Studio converts MIDI files into keyboard input for the instrument gameplay of “星痕共鸣”. It is built around a desktop GUI and currently provides two workspace groups:

- **Piano / Guitar / Bass**
- **Drums**

Rather than being a loose collection of scripts, the project is organized as a desktop tool for everyday use, tuning, testing, and distribution. It focuses on practical in-game workflows such as track filtering, visual previews, interval movement, pedal handling, auto tuning, ensemble scheduling, and a modern UI.

## Preview

### Main screen
![Home](docs/assets/home.png)

### Piano / Guitar / Bass
![Piano](docs/assets/piano.png)

### Drums
![Drum](docs/assets/drum.png)

### Settings
![Settings](docs/assets/settings.png)

### Dark mode
![Dark Mode](docs/assets/dark.png)

## Features

### Playback
- MIDI auto-play for piano / guitar / bass
- MIDI auto-play for drums
- play / pause / stop hotkeys
- MIDI track filtering and recommendations
- piano-roll preview, drum-lane preview, and timeline seeking

### Range and mapping
- automatic playable-range adaptation
- interval movement logic
- pedal handling and retrigger controls
- separate parameter sets for piano / guitar / bass and drums
- editable `config.txt` with a default template

### Auto tuning and utilities
- auto tuning and parameter suggestions
- ensemble scheduling
- Beijing time synchronization
- runtime logs and crash logs

### UI and workflow
- multiple visual themes
- dark mode
- glass-style background effect
- optional splash screen
- clearer parameter naming and hover descriptions

## Environment

- Windows 10 / 11
- Python 3.10+
- PySide6 GUI environment
- intended for “星痕共鸣” instrument gameplay that maps MIDI to keyboard input

## Installation and Run

### Run from source

```bash
git clone https://github.com/ShiroiSaya/SayaTech-Midi-Studio.git
cd SayaTech-Midi-Studio
pip install -r requirements.txt
python app.py
```

### Release file naming

The source repository does not include prebuilt binaries by default. Recommended release names:

- `SayaTech_MIDI_Studio_Setup.exe`: Windows installer
- `SayaTech_MIDI_Studio.exe`: single-file portable build

Release page: <https://github.com/ShiroiSaya/SayaTech-Midi-Studio/releases>

## Build

### Single-file EXE
Use the included scripts or build directly with PyInstaller:

- output: `dist/SayaTech_MIDI_Studio.exe`

### Installer
The recommended release pipeline is `onedir + Inno Setup`:

- directory build: `dist/SayaTech_MIDI_Studio/`
- installer build: `installer_output/SayaTech_MIDI_Studio_Setup.exe`

## Repository layout

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

- Light mode supports the background image and glass-style effects.
- Dark mode disables the background image automatically for better readability.
- Drum parameters are separated from the piano / guitar / bass parameter page.
- Auto tuning suggestions are best applied first and then verified in playback, instead of replacing every custom setting blindly.

## License

This project is licensed under the [MIT License](LICENSE).

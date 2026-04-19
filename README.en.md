<div align="center">

<img src="docs/assets/logo.png" width="128" alt="SayaTech-Midi-Studio Logo">

# SayaTech-Midi-Studio

**A Windows MIDI auto-play studio with piano / drum playback, auto tuning, splash screen, themes, and glass-style UI.**

[简体中文](README.md) · [English](README.en.md) · [日本語](README.ja.md)
[![Repository](https://img.shields.io/badge/GitHub-ShiroiSaya%2FSayaTech-Midi-Studio-181717?logo=github)](https://github.com/ShiroiSaya/SayaTech-Midi-Studio)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Repository:** <https://github.com/ShiroiSaya/SayaTech-Midi-Studio>

```bash
git clone https://github.com/ShiroiSaya/SayaTech-Midi-Studio.git
cd SayaTech-Midi-Studio
```


<img src="docs/assets/banner.png" alt="SayaTech-Midi-Studio Banner">

</div>

## Preview

### Main screen (no MIDI loaded)
![Home](docs/assets/screenshot-home-empty.png)

### Piano workspace
![Piano](docs/assets/screenshot-piano.png)

### Drum workspace
![Drum](docs/assets/screenshot-drum.png)

### Settings dialog
![Settings](docs/assets/screenshot-settings.png)

### Splash screen
![Splash](docs/assets/screenshot-splash.png)

### Dark mode
![Dark Mode](docs/assets/screenshot-dark.png)

## Features

- Piano MIDI auto-play
- Drum MIDI auto-play
- Automatic parameter tuning and suggestions
- Short-range fixed-window logic
- Ensemble timer with Beijing time sync
- Configurable hotkeys
- Multiple themes, dark mode, and glass UI
- Optional splash screen
- Hover tooltips and clearer parameter naming
- Crash logs and runtime logs

## Environment

- Windows 10 / 11
- Python 3.10+
- PySide6-based GUI environment
- Suitable for scenarios that send keyboard input to games or windows

## Downloads and Releases

- Recommended installer filename for GitHub Releases: `SayaTech_MIDI_Studio_Setup.exe`
- Portable one-file build: `SayaTech_MIDI_Studio.exe`
- Suggested Releases page: <https://github.com/ShiroiSaya/SayaTech-Midi-Studio/releases>

## Quick Start

```bash
git clone https://github.com/ShiroiSaya/SayaTech-Midi-Studio.git
cd SayaTech-Midi-Studio
pip install -r requirements.txt
python app.py
```

## Build

### One-file EXE
You can use the included build scripts or package the app with PyInstaller directly. The output filename is `dist/SayaTech_MIDI_Studio.exe`.

### Installer
Using `onedir + Inno Setup` is recommended for a faster launch experience than a single-file build. The installer output filename is fixed as `installer_output/SayaTech_MIDI_Studio_Setup.exe`.

## Highlights

This project is more than a simple script pack. It provides a complete MIDI auto-play workflow:

- Unified desktop UI
- Separate piano and drum workspaces
- Auto tuner linked with runtime parameters
- Centralized settings panel
- Splash screen and visual themes
- Packaging options suitable for distribution

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

- Background image and glass effects are available in light mode
- Dark mode automatically disables the background image for better readability
- The app prefers the tracked `config.txt` in the repository; if it is missing, it will regenerate one from the default template
- All screenshots in this README are from a recent version of the UI
- For Releases, it is recommended to upload `SayaTech_MIDI_Studio_Setup.exe`; prebuilt binaries are not committed to the source repository

## License

This project is released under the **MIT License**. See [LICENSE](LICENSE) for details.

## Dependencies

Runtime and packaging dependencies are listed in [requirements.txt](requirements.txt).

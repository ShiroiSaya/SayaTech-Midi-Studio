@echo off
setlocal
cd /d "%~dp0\.."
if not exist config.txt copy /Y config.example.txt config.txt >nul
python -m pip install -r requirements.txt
python -m PyInstaller SayaTech_MIDI_Studio_onefile.spec

echo.
echo Build complete. Output: dist\SayaTech_MIDI_Studio.exe
pause

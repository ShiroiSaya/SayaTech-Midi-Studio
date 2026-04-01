@echo off
setlocal
cd /d "%~dp0\.."
if not exist config.txt copy /Y config.example.txt config.txt >nul
python -m pip install -r requirements.txt
python -m PyInstaller SayaTech_MIDI_Studio_onedir.spec
if exist "%LocalAppData%\Programs\Inno Setup 6\ISCC.exe" (
  "%LocalAppData%\Programs\Inno Setup 6\ISCC.exe" installer.iss
) else (
  echo Inno Setup 6 not found. Please install it first.
)

echo.
echo Build complete. Folder: dist\SayaTech_MIDI_Studio
echo Installer output: installer_output\SayaTech_MIDI_Studio_Setup.exe
pause

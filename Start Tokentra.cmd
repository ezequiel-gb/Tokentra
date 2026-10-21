@echo off
if exist "%LOCALAPPDATA%\Programs\Tokentra\Tokentra.exe" (
  start "Tokentra" "%LOCALAPPDATA%\Programs\Tokentra\Tokentra.exe"
) else if exist "%~dp0dist-rc3\Tokentra\Tokentra.exe" (
  start "Tokentra" "%~dp0dist-rc3\Tokentra\Tokentra.exe"
) else (
  echo Install the current setup package or build the development executable first.
  pause
)

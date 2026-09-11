@echo off
REM Angie'yi durdurur (n8n + cloudflared).
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\angie-baslat.ps1" -Durdur
pause

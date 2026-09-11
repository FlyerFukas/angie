@echo off
REM Angie'yi baslatir (cloudflared tunnel + n8n). Cift tiklayarak calistirabilirsin.
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\angie-baslat.ps1"
echo.
echo Kapatmak icin bu pencereyi kapatabilirsin, Angie arka planda calismaya devam eder.
echo Durdurmak icin: Angie-Durdur.cmd
pause

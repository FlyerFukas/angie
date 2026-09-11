# Angie'yi baslatir: cloudflared tunnel + n8n.
#
#   .\angie-baslat.ps1          -> baslatir
#   .\angie-baslat.ps1 -Durdur  -> durdurur
#
# Tunnel URL'i her baslatmada degisir; script URL'i yakalayip n8n'e
# WEBHOOK_URL olarak verir. n8n de Telegram'a webhook'u kendisi bildirir.
# OAuth callback'i localhost'a sabitli oldugu icin Google ayarlari bozulmaz.

param([switch]$Durdur)

$Proje     = Split-Path $PSScriptRoot -Parent
$TunnelLog = Join-Path $Proje "tunnel.log"
$N8nLog    = Join-Path $Proje "n8n.log"

# ---------------------------------------------------------------- durdur
Write-Output "Eski surecler durduruluyor..."
Get-Process cloudflared -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
$baglanti = Get-NetTCPConnection -LocalPort 5678 -State Listen -ErrorAction SilentlyContinue
if ($baglanti) { $baglanti | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue } }
Start-Sleep -Seconds 3

if ($Durdur) { Write-Output "Angie durduruldu."; exit 0 }

# ---------------------------------------------------------------- tunnel
Remove-Item $TunnelLog -ErrorAction SilentlyContinue
Start-Process -FilePath (Join-Path $Proje "bin\cloudflared.exe") `
  -ArgumentList "tunnel", "--url", "http://localhost:5678", "--no-autoupdate" `
  -RedirectStandardError $TunnelLog `
  -RedirectStandardOutput (Join-Path $Proje "tunnel.out.log") `
  -WindowStyle Hidden

Write-Output "Tunnel aciliyor..."
$url = $null
for ($i = 0; $i -lt 60; $i++) {
  Start-Sleep -Seconds 1
  if (Test-Path $TunnelLog) {
    $m = Select-String -Path $TunnelLog -Pattern "https://[a-z0-9-]+\.trycloudflare\.com" -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($m) { $url = $m.Matches[0].Value; break }
  }
}
if (-not $url) {
  Write-Output "Tunnel URL alinamadi. Bak: $TunnelLog"
  exit 1
}
Write-Output "Tunnel hazir: $url"

# ---------------------------------------------------------------- n8n
$env:WEBHOOK_URL                       = $url
$env:N8N_EDITOR_BASE_URL               = "http://localhost:5678"
$env:N8N_PORT                          = "5678"
$env:N8N_USER_FOLDER                   = $env:USERPROFILE
$env:N8N_SECURE_COOKIE                 = "false"
$env:GENERIC_TIMEZONE                  = "Europe/Istanbul"
$env:TZ                                = "Europe/Istanbul"
$env:N8N_DIAGNOSTICS_ENABLED           = "false"
$env:N8N_VERSION_NOTIFICATIONS_ENABLED = "false"
$env:EXECUTIONS_DATA_PRUNE             = "true"
$env:EXECUTIONS_DATA_MAX_AGE           = "168"
$env:N8N_PERSONALIZATION_ENABLED       = "false"

. (Join-Path $PSScriptRoot "n8n-yolu.ps1")
$n8nBin = Get-N8nBin
Write-Output "n8n: $n8nBin"
Start-Process -FilePath "node" -ArgumentList $n8nBin, "start" `
  -RedirectStandardOutput $N8nLog `
  -RedirectStandardError (Join-Path $Proje "n8n.err.log") `
  -WindowStyle Hidden

Write-Output "n8n baslatiliyor..."
for ($i = 0; $i -lt 60; $i++) {
  try {
    $r = Invoke-WebRequest -Uri "http://localhost:5678/healthz" -UseBasicParsing -TimeoutSec 3
    if ($r.StatusCode -eq 200) {
      Write-Output ""
      Write-Output "======================================================"
      Write-Output " Angie calisiyor"
      Write-Output " Arayuz : http://localhost:5678"
      Write-Output " Tunnel : $url"
      Write-Output "======================================================"
      exit 0
    }
  } catch { Start-Sleep -Seconds 2 }
}
Write-Output "n8n baslatilamadi. Bak: $N8nLog"
exit 1

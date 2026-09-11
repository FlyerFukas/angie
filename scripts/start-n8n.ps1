# Angie - n8n baslatma scripti
# OAuth callback'i sabit tutmak icin N8N_EDITOR_BASE_URL localhost'a sabitlendi.
# Telegram webhook kullanilacaksa WEBHOOK_URL disaridan verilir (tunnel URL'i).
#
# ONEMLI: Bu script tek basina (restart-n8n.ps1 uzerinden, ornegin yayinla.ps1
# icinde) cagrildiginda WEBHOOK_URL ortam degiskeni miras alinmaz. cloudflared
# tunneli hala calisiyor olabilir (restart-n8n.ps1 onu durdurmuyor) ama URL'i
# n8n'e yeniden verilmezse Telegram webhook'u localhost'a kayitli kalir ve
# disaridan ulasilamaz hale gelir. Bu yuzden burada tunnel.log'dan aktif
# tunnel URL'ini kendimiz okuyup WEBHOOK_URL olarak set ediyoruz.
if (-not $env:WEBHOOK_URL) {
  $tunnelLog = Join-Path (Split-Path $PSScriptRoot -Parent) "tunnel.log"
  if (Test-Path $tunnelLog) {
    $m = Select-String -Path $tunnelLog -Pattern "https://[a-z0-9-]+\.trycloudflare\.com" -ErrorAction SilentlyContinue |
         Select-Object -Last 1
    if ($m) {
      $env:WEBHOOK_URL = $m.Matches[0].Value
      Write-Output "WEBHOOK_URL tunnel.log'dan alindi: $($env:WEBHOOK_URL)"
    } else {
      Write-Output "UYARI: tunnel.log'da tunnel URL'i bulunamadi. Telegram webhook'u localhost'a kayitli olabilir."
    }
  } else {
    Write-Output "UYARI: tunnel.log yok, cloudflared calismiyor olabilir. Telegram webhook'u localhost'a kayitli olabilir."
  }
}

$env:N8N_EDITOR_BASE_URL   = "http://localhost:5678"
$env:N8N_PORT              = "5678"
# Veritabani konumunu acikca sabitle: credential'lar ve workflow'lar
# ~/.n8n icinde. HOME farkliliklarinda kaymasin diye acikca veriliyor.
$env:N8N_USER_FOLDER       = $env:USERPROFILE
$env:N8N_SECURE_COOKIE     = "false"
$env:GENERIC_TIMEZONE      = "Europe/Istanbul"
$env:TZ                    = "Europe/Istanbul"
$env:N8N_DIAGNOSTICS_ENABLED = "false"
$env:N8N_VERSION_NOTIFICATIONS_ENABLED = "false"
$env:EXECUTIONS_DATA_PRUNE = "true"
$env:EXECUTIONS_DATA_MAX_AGE = "168"
$env:N8N_PERSONALIZATION_ENABLED = "false"

. (Join-Path $PSScriptRoot "n8n-yolu.ps1")
$n8nBin = Get-N8nBin
Write-Output "n8n baslatiliyor -> http://localhost:5678"
Write-Output "  (n8n: $n8nBin)"
& node $n8nBin start

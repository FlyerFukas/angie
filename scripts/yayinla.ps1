# Angie workflow'unu n8n'e yukler, yayinlar ve n8n'i yeniden baslatir.
#
# n8n 2.x'te workflow'u aktif etmek icin publish + yeniden baslatma gerekiyor;
# ayrica import, yayindaki workflow'u pasiflestirdigi icin sira onemli.

$ErrorActionPreference = "Continue"
. (Join-Path $PSScriptRoot "n8n-yolu.ps1")

$Proje = Split-Path $PSScriptRoot -Parent
$n8n   = Get-N8nBin
$wf    = Join-Path $Proje "workflows\01-angie.json"
$env:N8N_USER_FOLDER = $env:USERPROFILE

if (-not (Test-Path $wf)) {
  Write-Output "01-angie.json yok. Once uret: py scripts\uret-angie.py"
  exit 1
}

Write-Output "1/4 workflow iceri aktariliyor..."
& node $n8n import:workflow --input=$wf 2>&1 | Select-String -Pattern "Success|error" | Select-Object -First 2

Write-Output "2/4 yayinlaniyor..."
# n8n calisirken CLI komutlari port cakisiyor (task broker 5679); gecici port ver.
$env:N8N_RUNNERS_BROKER_PORT = "5680"
$env:N8N_PORT = "5681"
& node $n8n publish:workflow --id=angieAsistan0001 2>&1 | Select-String -Pattern "Publish|error" | Select-Object -First 2
Remove-Item Env:\N8N_RUNNERS_BROKER_PORT -ErrorAction SilentlyContinue
Remove-Item Env:\N8N_PORT -ErrorAction SilentlyContinue

Write-Output "3/4 n8n yeniden baslatiliyor..."
& (Join-Path $PSScriptRoot "restart-n8n.ps1")

Write-Output "4/4 durum kontrolu..."
Start-Sleep -Seconds 5
& py (Join-Path $PSScriptRoot "durum.py")
Write-Output "Bitti. n8n: http://localhost:5678"

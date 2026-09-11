# n8n'i durdurup yeniden baslatir (arka planda), hazir olana kadar bekler.
# Tunnel'a dokunmaz; calisan cloudflared varsa start-n8n.ps1 onun URL'ini
# tunnel.log'dan okuyup WEBHOOK_URL olarak kullanir.

$Proje = Split-Path $PSScriptRoot -Parent

$baglanti = Get-NetTCPConnection -LocalPort 5678 -State Listen -ErrorAction SilentlyContinue
if ($baglanti) {
  $baglanti | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }
}
Start-Sleep -Seconds 3

Start-Process -FilePath "powershell.exe" `
  -ArgumentList "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", (Join-Path $PSScriptRoot "start-n8n.ps1") `
  -RedirectStandardOutput (Join-Path $Proje "n8n.log") `
  -RedirectStandardError  (Join-Path $Proje "n8n.err.log") `
  -WindowStyle Hidden

for ($i = 0; $i -lt 60; $i++) {
  try {
    $r = Invoke-WebRequest -Uri "http://localhost:5678/healthz" -UseBasicParsing -TimeoutSec 3
    if ($r.StatusCode -eq 200) { Write-Output "n8n hazir ($($i * 2) sn)"; exit 0 }
  } catch { Start-Sleep -Seconds 2 }
}
Write-Output "n8n baslatilamadi"
exit 1

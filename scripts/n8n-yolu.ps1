# n8n calistirilabilir dosyasini bulur.
#
# Once proje icindeki yerel kurulum (node_modules), bulunamazsa global npm
# kurulumu denenir. Yerel kurulum tercih edilir: bazi Windows kurulumlarinda
# %APPDATA%\npm yolu uygulama sandbox'ina yonlenebiliyor ve global olarak
# kurulan n8n normal bir terminalden "Cannot find module" hatasi veriyor.

function Get-N8nBin {
    $adaylar = @(
        (Join-Path (Split-Path $PSScriptRoot -Parent) "node_modules\n8n\bin\n8n"),
        (Join-Path $env:APPDATA "npm\node_modules\n8n\bin\n8n")
    )
    foreach ($yol in $adaylar) {
        if (Test-Path $yol) { return $yol }
    }
    throw "n8n bulunamadi. Proje klasorunde calistir: npm install n8n@2.30.7"
}

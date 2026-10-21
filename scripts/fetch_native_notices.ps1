# Build-time only: reproduce the retained native/Rust notice inputs over normal TLS.
# Never execute downloaded archives; collect_native_notices.py only reads notices.
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$sourceRoot = Join-Path $projectRoot '.tools/compliance'
$manifestPath = Join-Path $projectRoot 'docs/compliance/native-rust-notices.json'
$manifest = Get-Content -LiteralPath $manifestPath -Raw -Encoding utf8 | ConvertFrom-Json
New-Item -ItemType Directory -Path $sourceRoot -Force | Out-Null
$downloads = @()
foreach ($crate in $manifest.rust_components) {
    $downloads += [pscustomobject]@{name="$($crate.name)-$($crate.version).crate";url=$crate.url;sha256=$crate.sha256}
}
$downloads += [pscustomobject]@{name='rustc-1.97.1-windows.tar.xz';url=$manifest.rust_standard_library_url;sha256=$manifest.rust_standard_library_archive_sha256}
$downloads += $manifest.native_source_downloads
foreach ($entry in $downloads) {
    if ([IO.Path]::GetFileName($entry.name) -cne $entry.name) { throw 'Unsafe manifest filename' }
    $destination = Join-Path $sourceRoot $entry.name
    if (-not (Test-Path -LiteralPath $destination)) {
        Invoke-WebRequest -UseBasicParsing -Uri $entry.url -OutFile $destination
    }
    $actual = (Get-FileHash -LiteralPath $destination -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($actual -ne $entry.sha256) { throw "Notice input hash mismatch: $($entry.name)" }
}
# Collector input list; URLs/hashes remain committed in the public provenance file.
$manifest.native_source_downloads | ConvertTo-Json -Depth 20 |
    Set-Content -LiteralPath (Join-Path $sourceRoot 'supplement-downloads.json') -Encoding utf8
Write-Output "Verified $($downloads.Count) local native/Rust notice inputs."

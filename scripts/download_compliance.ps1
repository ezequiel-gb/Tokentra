# Build-time acquisition with Windows' normal certificate validation. No TLS bypass.
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
$folder = Join-Path $root '.tools\compliance'
New-Item -ItemType Directory -Force -Path $folder | Out-Null
$sources = @(
    'https://download.qt.io/official_releases/qt/6.12/6.12.0/submodules/qtbase-everywhere-src-6.12.0.tar.xz',
    'https://download.qt.io/official_releases/QtForPython/pyside6/PySide6-6.12.0-src/pyside-setup-everywhere-src-6.12.0.tar.xz'
)
foreach ($url in $sources) {
    $target = Join-Path $folder ([Uri]$url).Segments[-1]
    if (-not (Test-Path -LiteralPath $target)) {
        Invoke-WebRequest -Uri $url -OutFile ($target + '.part') -TimeoutSec 180
        Move-Item -LiteralPath ($target + '.part') -Destination $target
    }
    Get-FileHash -LiteralPath $target -Algorithm SHA256 | Select-Object Hash
}
# Pin package URLs and hashes from the authenticated HTTPS PyPI service.
$evidence = @()
foreach ($name in @('PySide6-Essentials','shiboken6','tiktoken')) {
    $version = if ($name -eq 'tiktoken') { '0.14.0' } else { '6.12.0' }
    $metadata = Invoke-RestMethod -Uri "https://pypi.org/pypi/$name/$version/json" -TimeoutSec 60
    $selected = @($metadata.urls | Where-Object { ($_.filename -like '*abi3-win_amd64.whl') -or ($name -eq 'tiktoken' -and $_.packagetype -eq 'sdist') })
    foreach ($entry in $selected) {
        $target = Join-Path $folder $entry.filename
        if (-not (Test-Path -LiteralPath $target)) { Invoke-WebRequest -Uri $entry.url -OutFile $target -TimeoutSec 180 }
        $digest = (Get-FileHash -LiteralPath $target -Algorithm SHA256).Hash.ToLower()
        if ($digest -ne $entry.digests.sha256) { throw 'Upstream package digest mismatch' }
        $evidence += [ordered]@{name=$name;version=$version;filename=$entry.filename;url=$entry.url;sha256=$digest;verification='Matches digest returned by PyPI HTTPS JSON API'}
    }
}
$evidence | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $folder 'pypi-artifacts.json') -Encoding utf8

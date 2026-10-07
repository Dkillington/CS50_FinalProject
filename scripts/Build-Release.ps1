param([string]$Python = 'python')
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
Push-Location -LiteralPath $projectRoot
try {
    # PyInstaller's hook discovery treats brackets in its own install path as
    # glob syntax. Use an isolated build environment when the checkout has them.
    $packagerPath = & $Python -c 'import PyInstaller; print(PyInstaller.__file__)'
    if ($LASTEXITCODE -ne 0) { throw 'Install requirements-build.txt before packaging.' }
    if ($packagerPath -match '[\[\]]') {
        $isolatedEnv = Join-Path ([IO.Path]::GetTempPath()) 'youtube-channel-stats-build'
        & $Python -m venv $isolatedEnv
        if ($LASTEXITCODE -ne 0) { throw 'Could not create isolated build environment.' }
        $Python = Join-Path $isolatedEnv 'Scripts\python.exe'
        & $Python -m pip install -r requirements-build.txt
        if ($LASTEXITCODE -ne 0) { throw 'Build dependency installation failed.' }
    }
    & $Python -m PyInstaller --noconfirm --clean --onefile --windowed --exclude-module setuptools --exclude-module _distutils_hack --name YouTubeChannelStats --add-data 'templates;templates' --add-data 'static;static' launcher.py
    if ($LASTEXITCODE -ne 0) { throw 'Dashboard packaging failed.' }
    Write-Host 'Ready: dist\YouTubeChannelStats.exe'
} finally { Pop-Location }

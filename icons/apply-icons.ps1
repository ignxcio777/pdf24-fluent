# Applies the Fluent icons to every PDF24 / PDFgear shortcut it finds
# (Start menu and desktops, for the current user and for all users).
#   .\apply-icons.ps1                 shortcuts only
#   .\apply-icons.ps1 -PdfFileIcon    also the icon of .pdf files when PDFgear is the default app
#   .\apply-icons.ps1 -Revert         restore everything from the backups
# Icons are copied to %LOCALAPPDATA%\pdf24-fluent, so you can delete this folder afterwards.
param([switch]$PdfFileIcon, [switch]$Revert, [string]$Store, [switch]$Elevated)

$ErrorActionPreference = 'Stop'
if (-not $Store) { $Store = Join-Path $env:LOCALAPPDATA 'pdf24-fluent' }
$backupDir = Join-Path $Store 'backup'

# executable name (lower case) -> icon
$map = @{
    'pdf24.exe'           = 'pdf24\ico\PDF24-PDF24.ico'
    'pdf24-toolbox.exe'   = 'pdf24\ico\PDF24-PDF24.ico'
    'pdf24-launcher.exe'  = 'pdf24\ico\PDF24-PDF24.ico'
    'pdf24-creator.exe'   = 'pdf24\ico\PDF24-Creator.ico'
    'pdf24-compress.exe'  = 'pdf24\ico\PDF24-Compress.ico'
    'pdf24-ocr.exe'       = 'pdf24\ico\PDF24-OCR.ico'
    'pdf24-reader.exe'    = 'pdf24\ico\PDF24-Reader.ico'
    'pdf24-fax.exe'       = 'pdf24\ico\PDF24-Fax.ico'
    'pdf24-assistant.exe' = 'pdf24\ico\PDF24-Assistant.ico'
    'pdf24-doctool.exe'   = 'pdf24\ico\PDF24-DocTool.ico'
    'pdf24-settings.exe'  = 'pdf24\ico\PDF24-Settings.ico'
    'pdflauncher.exe'     = 'pdfgear\ico\PDFgear.ico'
    'pdfeditor.exe'       = 'pdfgear\ico\PDFgear.ico'
}
$sh = New-Object -ComObject WScript.Shell

function Get-Shortcuts([string[]]$roots) {
    Get-ChildItem $roots -Recurse -Filter *.lnk -ErrorAction SilentlyContinue | ForEach-Object {
        $t = $sh.CreateShortcut($_.FullName).TargetPath
        if ($t -and $map.ContainsKey((Split-Path $t -Leaf).ToLower())) { [pscustomobject]@{ Path = $_.FullName; Exe = (Split-Path $t -Leaf).ToLower() } }
    }
}
function Update-Shortcut($s) {
    $copy = Join-Path $backupDir (($s.Path -replace '[:\\]', '_'))
    if ($Revert) {
        if (Test-Path -LiteralPath $copy) { Copy-Item -LiteralPath $copy $s.Path -Force; "Restored: $($s.Path)" }
        return
    }
    if (-not (Test-Path -LiteralPath $copy)) { Copy-Item -LiteralPath $s.Path $copy }
    $l = $sh.CreateShortcut($s.Path)
    $l.IconLocation = (Join-Path $Store $map[$s.Exe]) + ',0'
    $l.Save()
    "Icon set: $($s.Path)"
}

$userRoots = "$env:APPDATA\Microsoft\Windows\Start Menu", [Environment]::GetFolderPath('Desktop')
$allRoots  = "$env:ProgramData\Microsoft\Windows\Start Menu", "$env:PUBLIC\Desktop"

if ($Elevated) {   # second pass, running as admin: shared shortcuts only
    Get-Shortcuts $allRoots | ForEach-Object { Update-Shortcut $_ }
    Start-Sleep 2
    return
}

New-Item -ItemType Directory -Force $backupDir | Out-Null
if (-not $Revert) {
    Copy-Item -Recurse -Force (Join-Path $PSScriptRoot 'pdf24'), (Join-Path $PSScriptRoot 'pdfgear') $Store
}
Get-Shortcuts $userRoots | ForEach-Object { Update-Shortcut $_ }

# .pdf file icon (only touches the current user's registry)
$key = 'HKCU:\Software\Classes\PdfGear.App.1\DefaultIcon'
if ($Revert) {
    if (Test-Path $key) { Remove-Item 'HKCU:\Software\Classes\PdfGear.App.1' -Recurse; '.pdf icon restored' }
} elseif ($PdfFileIcon) {
    New-Item -Force $key | Out-Null
    Set-Item $key -Value ((Join-Path $Store 'pdfgear\ico\PDFgear-Documento-PDF.ico') + ',0')
    '.pdf icon set (visible when PDFgear is your default PDF app)'
}

# shortcuts shared by all users need admin rights
if (Get-Shortcuts $allRoots) {
    $a = @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', "`"$PSCommandPath`"", '-Elevated', '-Store', "`"$Store`"")
    if ($Revert) { $a += '-Revert' }
    Start-Process powershell.exe -Verb RunAs -Wait -ArgumentList $a
}
ie4uinit.exe -show
'Done. If an icon still looks old, sign out and back in (Windows icon cache).'

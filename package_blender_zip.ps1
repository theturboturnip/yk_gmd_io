# Native PowerShell solution for generating ZIP file, taken from https://stackoverflow.com/a/59018865/4248422

Write-Output "Zipping addon..."

# top level from where to start and location of the zip file
$path = "."
# top path that we want to keep in the source code zip file
$subdir = "yk_gmd_blender"
# location of the zip file
$ZipFile = "${path}\yk_gmd_blender.zip"

# change current directory
Set-Location "$path"

# collecting list of files that we want to archive excluding those that we don't want to preserve
$Files = @(Get-ChildItem "${subdir}" -Recurse -File | Where-Object { $_ -Match "^*.py$" })
$FullFilenames = $files | ForEach-Object -Process { Write-Output -InputObject $_.FullName }

# remove old zip file
if (Test-Path $ZipFile)
{
    Remove-Item $ZipFile -ErrorAction Stop
}

#create zip file
Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem
$zip = [System.IO.Compression.ZipFile]::Open(($ZipFile), [System.IO.Compression.ZipArchiveMode]::Create)

# write entries with relative paths as names
foreach ($fname in $FullFilenames)
{
    $rname = $( Resolve-Path -Path $fname -Relative ) -replace '\.\\', ''
    Write-Output $rname
    $zentry = $zip.CreateEntry($rname)
    $zentryWriter = New-Object -TypeName System.IO.BinaryWriter $zentry.Open()
    $zentryWriter.Write([System.IO.File]::ReadAllBytes($fname))
    $zentryWriter.Flush()
    $zentryWriter.Close()
}

# release zip file
$zip.Dispose()
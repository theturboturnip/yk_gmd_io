#zip -r yk_gmd_blender.zip yk_gmd_blender -x "yk_gmd_blender/**/__pycache__/*"
#$filePath = "./yk_gmd_blender/"
#$ZipName = "yk_gmd_blender_build.zip"
#
#$PyFiles = Get-ChildItem -Recurse -Path $filePath -Include *.py
#
#$PyFiles |
#
#Get-ChildItem -Path "./yk_gmd_blender/*" -Include *.py -Recurse | Compress-Archive -Force -DestinationPath "yk_gmd_blender_build.zip"

Set-Alias 7zip "$env:ProgramFiles\7-Zip\7z.exe"
Remove-Item yk_gmd_blender.zip
# Use 7zip to add all files from yk_gmd_blender (including the root folder yk_gmd_blender) *excluding* pyc and __pycache__ files/dirs.
7zip a yk_gmd_blender.zip ./yk_gmd_blender/ -r "-xr!*.pyc" "-xr!__pycache__"
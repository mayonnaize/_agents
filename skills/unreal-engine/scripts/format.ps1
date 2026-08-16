$Source = Join-Path $PSScriptRoot "../Source"
$clangFormat = Join-Path $PSScriptRoot "../Resources/.clang-format"

$files = Get-ChildItem -Path $Source -Include *.cpp,*.h -File -Recurse | ForEach-Object FullName
clang-format.exe -i $files -style=file:"$clangFormat"

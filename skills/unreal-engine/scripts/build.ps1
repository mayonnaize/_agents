# コマンドライン引数
param(
    # Win64等のビルド対象のプラットフォーム
    [string]$platform = $args[0],
    # Development等のビルド設定
    [string]$clientconfig = $args[1]
)

chcp 65001

if ([string]::IsNullOrEmpty($platform) -or [string]::IsNullOrEmpty($clientconfig)) {
    Write-Output "Command Line Args are required."
    exit 1
} else {
    Write-Output "platform: $platform"
    Write-Output "clientconfig: $clientconfig"
}

# インクルード
$utils = Join-Path $PSScriptRoot "utils.ps1"
Write-Output $utils
. $utils

$RunUAT = Get-RunUAT

# .uprojectファイル
$projectPath = Get-UProject

& $RunUAT `
    "BuildCookRun" `
    "-project=$projectPath" `
    "-noP4" `
    "-platform=$platform" `
    "-clientconfig=$clientconfig" `
    "-cook" `
    "-allmap" `
    "-build" `
    "-stage" `
    "-pak" `
    "-partialgc"

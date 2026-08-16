chcp 65001

# インクルード
$utils = Join-Path $PSScriptRoot utils.ps1
echo $utils
. $utils

$RunUAT = Get-RunUAT

$UE5EditorExe = Get-UEEditorExe

$ProjectName = Get-UProject

$ReportOutputPath = Join-Path $PSScriptRoot ..\TestReport
echo $ReportOutputPath

# ! エディタビルド
& $RunUAT `
    "BuildCookRun" `
    "-project=$ProjectName" `
    "-platform=Win64" `
    "-clientconfig=Development" `
    "-build"

# ! テスト
# historiaのコマンドから-gameを削除: https://historia.co.jp/archives/9805/
# RenderOffscreenを使うことで描画スレッドも使いながら画面を非表示にできる(nullrhiは描画スレッドを使わない)
# テストの実行結果: https://docs.unrealengine.com/5.0/en-US/automation-test-report-server-in-unreal-engine/
# https://www.emidee.net/ue4/2018/11/13/UE4-Unit-Tests-in-Jenkins.html
# https://src.redpoint.games/redpointgames/continuous-testing-for-unreal-engine/-/tree/main?ref_type=heads
. $UE5EditorExe `
    $ProjectName `
    -ExecCmds="Automation RunTests MyTest;Quit" `
    -ReportExportPath="$ReportOutputPath" `
    -AbsLog="$ReportOutputPath/RunTests.log" `
    -RenderOffscreen `
    -NoSplash `
    -Log `
    -LOGTIMES `
    -NoPause

Start-Sleep -Seconds 10

while($true) {
    Start-Sleep -Seconds 1
    $content = Get-Content $ReportOutputPath/RunTests.log -raw
    if ($content -match "TEST COMPLETE. EXIT CODE: (-?\d+)") {
        $exitCode = $Matches[1]
        Write-Output "Exit code: $exitCode"
        if ($exitCode -eq 0) {
            Write-Output "Success."
            exit 0
        } else {
            Write-Output "Failed."
            exit -1
        }

    } else {
        Write-Output "Test Complete not found. Checking again after 1 second..."
    }
}

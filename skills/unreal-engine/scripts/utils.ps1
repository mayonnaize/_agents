chcp 65001

# RunUAT.batの取得
function Get-RunUAT{
    # UEのルートディレクトリパス ($env:UE5_ROOT を使用)
    $UE_ROOT = $env:UE5_ROOT
    if ([string]::IsNullOrEmpty($UE_ROOT)) {
        Write-Error "UE5_ROOT environment variable is not defined."
        return $null
    }
    $ret_val = Join-Path "$UE_ROOT" "Engine\Build\BatchFiles\RunUAT.bat"
    return $ret_val
}

# UnrealEditor.exeの取得
function Get-UEEditorExe {

    # UEのルートディレクトリパス
    $UE_ROOT = $env:UE5_ROOT
    if ([string]::IsNullOrEmpty($UE_ROOT)) {
        Write-Error "UE5_ROOT environment variable is not defined."
        return $null
    }
    $ret_val = Join-Path $UE_ROOT "Engine\Binaries\Win64\UnrealEditor.exe"
    return $ret_val
}

# .uprojectファイルの取得
function Get-UProject{
    $projectPath = ""

    $folderPath = Join-Path $PSScriptRoot "..\"
    Get-ChildItem -Path $folderPath -Recurse -Filter "*.uproject" | ForEach-Object {
        $projectPath = $_.FullName
    }
    return $projectPath
}

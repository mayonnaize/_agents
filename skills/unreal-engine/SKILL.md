---
name: unreal-engine
description: "Use when: UE5プロジェクトのビルド, テスト実行, コードフォーマット, Unreal Engine 5, BuildCookRun, Automation Test, clang-format, パッケージング, クック, ステージング。ビルドパラメータの選択、テスト結果の解析、フォーマット実行を自動化する。"
---

# Unreal Engine 5 自動化スキル

このスキルは `skills/unreal-engine/scripts/` 配下のスクリプトを使って、UE5プロジェクトのビルド・テスト・フォーマットをエージェントが自動実行するためのガイドです。

## 前提条件の確認

スクリプト実行前に必ず確認すること:

1. **`$env:UE5_ROOT` が設定されているか確認する**
   ```powershell
   Write-Output $env:UE5_ROOT
   ```
   未設定の場合はユーザーに設定を依頼してエラーを返す。

2. **実行対象の `.uproject` ファイルがスクリプトの親ディレクトリ配下に存在するか確認する**
   ```powershell
   Get-ChildItem -Path . -Recurse -Filter "*.uproject"
   ```

---

## ワークフロー

### 1. タスクの判別

ユーザーのリクエストから以下のいずれかを判断する:

| キーワード | 実行スクリプト |
|---|---|
| ビルド / build / パッケージ / cook / stage | `build.ps1` |
| テスト / test / Automation / 自動テスト | `test.ps1` |
| フォーマット / format / clang-format / 整形 | `format.ps1` |

---

### 2. ビルド実行 (`build.ps1`)

**パラメータ**:
- `platform`: ターゲットプラットフォーム (例: `Win64`, `Android`, `iOS`)
- `clientconfig`: ビルド設定 (例: `Development`, `Shipping`, `DebugGame`)

**実行コマンド**:
```powershell
& "$PSScriptRoot/build.ps1" <platform> <clientconfig>
```

**パラメータが未指定の場合のデフォルト**:
- platform: `Win64`
- clientconfig: `Development`

**成功/失敗の判定**:
- 終了コード `0` → 成功
- それ以外 → ビルドエラー。ターミナル出力の `ERROR:` または `FAILED` を含む行をユーザーに提示する。

---

### 3. テスト実行 (`test.ps1`)

**実行コマンド**:
```powershell
& "$PSScriptRoot/test.ps1"
```

**テスト名のカスタマイズ**:
スクリプト内の `-ExecCmds="Automation RunTests MyTest;Quit"` の `MyTest` 部分がテストフィルタ。
ユーザーから特定のテスト名が指示された場合はスクリプトを一時編集して実行する。

**結果判定**:
- ログファイル (`TestReport/RunTests.log`) 内の `TEST COMPLETE. EXIT CODE: 0` → 成功
- `EXIT CODE:` が `0` 以外 → 失敗。`TestReport/` ディレクトリのレポートをユーザーに案内する。

**テストレポートの場所**:
```
skills/unreal-engine/TestReport/
```

---

### 4. フォーマット実行 (`format.ps1`)

**実行コマンド**:
```powershell
& "$PSScriptRoot/format.ps1"
```

**前提**:
- `clang-format.exe` が PATH に通っていること
- `../Resources/.clang-format` にスタイル定義ファイルが存在すること

**成功確認**:
- 終了コード `0` かつ標準エラー出力がなければ成功

---

## エラー対応フロー

```
エラー発生
├─ UE5_ROOT 未設定 → 環境変数の設定方法をユーザーに案内
├─ .uproject が見つからない → プロジェクトルートからスクリプトを実行するよう案内
├─ RunUAT.bat が見つからない → $env:UE5_ROOT のパスが正しいか確認を依頼
├─ UnrealEditor.exe が見つからない → UE5エディタのインストールを確認
└─ ビルド/テスト失敗 → ログの ERROR/FAILED 行を抽出してユーザーに提示
```

---

## スクリプト構成

```
skills/unreal-engine/scripts/
├── utils.ps1    # 共通ユーティリティ (Get-RunUAT, Get-UEEditorExe, Get-UProject)
├── build.ps1    # BuildCookRun によるビルド・クック・パッケージング
├── test.ps1     # Automation Test の実行と結果判定
└── format.ps1   # clang-format によるソースコード整形
```

## 環境変数

| 変数名 | 説明 | 例 |
|---|---|---|
| `UE5_ROOT` | Unreal Engine 5 のインストールルートパス | `C:\Program Files\Epic Games\UE_5.4` |

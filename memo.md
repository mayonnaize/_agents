## AIエージェント設定仕様の統合まとめ

### 1. スコープ別パス一覧表

| 機能             | エージェント    | グローバルスコープ                                                    | プロジェクトスコープ                                                                           |
| ---------------- | --------------- | --------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| **Skills**       | **Antigravity** | `~/.gemini/config/skills/`                                            | `.agents/skills/` (互換: `.agent/skills/`)                                                     |
|                  | **Codex**       | `~/.agents/skills/`                                                   | `.agents/skills/`                                                                              |
|                  | **Copilot**     | `~/.copilot/skills/`, `~/.agents/skills/`                             | `.github/skills/`, `.agents/skills/`, `.claude/skills/`                                        |
| **Rules**        | **Antigravity** | `~/.gemini/config/rules/`                                             | `.agents/rules/` (互換: `.agent/rules/`)                                                       |
|                  | **Codex**       | `~/.agents/rules/`                                                    | `.agents/rules/`                                                                               |
|                  | **Copilot**     | `~/.copilot/rules/`, `~/.agents/rules/`                               | `.github/rules/`, `.agents/rules/`, `.claude/rules/`                                           |
| **Hooks**        | **Antigravity** | `~/.gemini/config/hooks.json`                                         | `.agents/hooks.json`                                                                           |
|                  | **Codex**       | `~/.codex/hooks.json`, `~/.codex/config.toml`                         | `.codex/hooks.json`, `.codex/config.toml`                                                      |
|                  | **Copilot**     | `~/.copilot/hooks/*.json`                                             | `.github/hooks/*.json`                                                                         |
| **指示ファイル** | **Antigravity** | `~/.gemini/GEMINI.md`, `~/.gemini/AGENTS.md`                          | `GEMINI.md`, `AGENTS.md`                                                                       |
|                  | **Codex**       | `~/.codex/AGENTS.override.md``~/.codex/AGENTS.md`                     | `AGENTS.override.md`, `AGENTS.md`                                                              |
|                  | **Copilot**     | `~/.copilot/copilot-instructions.md``~/.copilot/instructions/**/*.md` | `.github/copilot-instructions.md`, `AGENTS.md``CLAUDE.md`, `GEMINI.md`, `*.instructions.md` 等 |
| **MCP**          | **Antigravity** | `~/.gemini/config/mcp_config.json`                                    | `.agents/mcp_config.json`                                                                      |
|                  | **Codex**       | `~/.codex/config.toml`                                                | `.codex/config.toml`                                                                           |
|                  | **Copilot**     | `~/.copilot/mcp-config.json`                                          | `.mcp.json`, `.github/mcp.json`                                                                |
| **Plugins**      | **Codex**       | `~/.agents/plugins/marketplace.json`                                  | `.agents/plugins/marketplace.json`                                                             |
|                  | **Copilot**     | (VS Code拡張または設定UI経由で指定)                                   | (UIまたはコマンド経由でローカルリポジトリを指定)                                               |
|                  | **Antigravity** | (ドキュメントに詳細パスの公開なし)                                    | (同上)                                                                                         |

---

### 2. オープン標準（.agents）の対応状況

AIエージェント間で設定を共有するための `AGENTS.md` および `.agents/` ディレクトリ規格に対する各ツールのスタンスは以下の通りです。

* **Skills**: 3つのツール全てが `.agents/skills/` をサポートしており、クロスプラットフォームでの共有が最も進んでいる領域です。
* **カスタム指示**: プロジェクトルートの `AGENTS.md` は3ツール全てで共通して読み込まれます。エージェント固有のファイル（`CLAUDE.md` や `GEMINI.md` など）に対する相互運用性の扱いはツールによって異なります。
* **Hooks / MCP**: 実行時のセキュリティやインターフェースに直結するため、共通規格は存在せず、各ツール固有のディレクトリ（`.codex/`, `.github/`, `~/.gemini/`）や設定ファイル（`config.toml` 等）に依存しています。

---

### 3. 各エージェントの仕様的特徴

* **Antigravity**
* グローバル設定は `~/.gemini/config/` へ集約し、プロジェクト設定は標準規格の `.agents/` を採用する、切り分けが明確なディレクトリ構造を持ちます。
* HooksおよびMCPの設定は単一のJSONファイル（`hooks.json`, `mcp_config.json`）で管理します。


* **Codex (ChatGPT)**
* HooksやMCPの管理において `config.toml` を多用し、設定を一元化する設計です。
* `AGENTS.md` の読み込みにおいて、`override` ファイルによる優先処理や、ディレクトリ階層を下りながら複数ファイルを結合する独自のマージロジックを持ちます。


* **GitHub Copilot**
* 後発としての相互運用性を重視しており、他社仕様（`CLAUDE.md`, `GEMINI.md`, `.claude/skills/` 等）のファイルを幅広くフォールバックとして読み込みます。
* Hooksにおいてディレクトリ内の全JSONファイルをマージしたり、MCP設定でカレントディレクトリからGitルートへ階層を遡って探索するなど、柔軟な再帰的探索ロジックを採用しています。

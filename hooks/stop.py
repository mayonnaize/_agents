import sys
import json
import hook_logger
import notify

def main():
    # 標準入力からのコンテキスト情報の破棄
    if not sys.stdin.isatty():
        sys.stdin.read()

    agent_name = sys.argv[1] if len(sys.argv) > 1 else 'Antigravity'

    # 実行ログの記録
    hook_logger.info(agent_name)

    # 通知の表示
    notify._show_notification(agent_name, 'stop')

    # ドキュメント更新確認指示の注入
    response = {
        "injectSteps": [
            {
                "ephemeralMessage": "タスクの完了報告を行う前に、必ず README.md や AGENTS.md、仕様書 などのドキュメント類の更新が必要かどうかを自己評価・確認すること。"
            }
        ]
    }
    print(json.dumps(response, ensure_ascii=False))
    sys.stdout.flush()

if __name__ == "__main__":

    main()

import sys
import json
import hook_logger
from plyer import notification

def _show_notification(agent_name, notify_type):
    if notify_type == 'action_needed':
        message = 'ユーザーのアクション（質問への回答など）が必要です。'
    elif notify_type == 'command_approval':
        message = 'コマンド実行の許可が必要です。'
    else:
        message = 'エージェントの作業が完了しました。'

    notification.notify(
        title=agent_name,
        message=message,
        app_name=agent_name,
        timeout=5
    )

def main():
    # 標準入力からのコンテキスト情報の破棄
    if not sys.stdin.isatty():
        sys.stdin.read()

    agent_name = sys.argv[1] if len(sys.argv) > 1 else 'Antigravity'
    notify_type = sys.argv[2] if len(sys.argv) > 2 else 'stop'

    # 実行ログの記録
    hook_logger.log_call(agent_name)

    _show_notification(agent_name, notify_type)

    if notify_type == 'action_needed':
        # 通知を出した上で、ツール実行自体は許可（allow）して本体の承認フローに任せる
        print(json.dumps({"decision": "allow"}))
        sys.exit(0)
    elif notify_type == 'command_approval':
        # 通知を出した上で、ツール実行自体は許可（allow）して本体の承認フローに任せる
        print(json.dumps({"decision": "allow"}))
        sys.exit(0)
    else:
        print(json.dumps({}))

if __name__ == "__main__":
    main()

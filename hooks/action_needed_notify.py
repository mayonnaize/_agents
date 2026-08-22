import sys
import json
import hook_logger
from plyer import notification

def _show_notification():
    notification.notify(
        title='Antigravity',
        message='ユーザーのアクション（質問への回答など）が必要です。',
        app_name='Antigravity',
        timeout=5
    )


def main():
    # 実行ログの記録
    hook_logger.log_call()

    # 標準入力からのコンテキスト情報の破棄
    if not sys.stdin.isatty():
        sys.stdin.read()

    # 通知実行
    _show_notification()

    # 規定の空JSON出力によるエージェントの正常停止
    print(json.dumps({"decision": "allow"}))
    sys.exit(0)

if __name__ == "__main__":
    main()

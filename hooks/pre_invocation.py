import sys
import json
import hook_logger

def main():
    # 実行ログの記録
    hook_logger.log_call()

    # 標準入力からのコンテキスト情報の破棄
    if not sys.stdin.isatty():
        sys.stdin.read()

    response = {
        "injectSteps": [
            {
                "ephemeralMessage": "/concise-grounded-replies スキルを読み込み、簡潔で根拠に基づいた応答形式を適用してください。"
            }
        ]
    }
    # 規定のJSON出力による指示の注入
    print(json.dumps(response, ensure_ascii=False))

if __name__ == "__main__":
    main()

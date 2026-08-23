import sys
import json
import hook_logger

def main():
    agent_name = sys.argv[1] if len(sys.argv) > 1 else 'Antigravity'
    
    # 実行ログの記録
    hook_logger.info(agent_name)

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
    # 文字化け防止のため ensure_ascii=True に変更
    print(json.dumps(response, ensure_ascii=True))

if __name__ == "__main__":
    main()

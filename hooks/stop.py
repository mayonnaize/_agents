import sys
import json
import hook_logger

def main():
    input_data = {}
    if not sys.stdin.isatty():
        stdin_content = sys.stdin.read()
        if stdin_content.strip():
            try:
                input_data = json.loads(stdin_content)
            except json.JSONDecodeError:
                pass

    agent_name = sys.argv[1] if len(sys.argv) > 1 else 'Antigravity'
    hook_logger.info(agent_name)

    execution_num = input_data.get("executionNum", 0)

    if execution_num == 0:
        response = {
            "decision": "continue",
            "reason": "/verification-before-completion スキルを読み込み、/sanitize-artifacts タスクの完了報告を行う前に、必ず README.md、AGENTS.md、仕様書などのドキュメント類の更新が必要かどうかを自己評価・確認すること。"
        }
    else:
        response = {
            "decision": "allow"
        }
        
    print(json.dumps(response, ensure_ascii=True))
    sys.stdout.flush()

if __name__ == "__main__":
    main()

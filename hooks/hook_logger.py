import sys
import datetime
from pathlib import Path

def log_call():
    # 呼び出し時刻の取得
    now = datetime.datetime.now()
    date_str = now.strftime('%Y%m%d')
    time_str = now.strftime('%H:%M:%S')

    # ログディレクトリの構築
    log_dir = Path.home() / '.agents' / 'logs'
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f'{date_str}.log'

    # エージェント名の推論（フックスクリプトの配置親ディレクトリ名、シンボリックリンクを解決）
    script_path = Path(sys.argv[0]).resolve()
    
    agent_name = "Unknown"
    if 'hooks' in script_path.parts:
        hooks_idx = script_path.parts.index('hooks')
        if hooks_idx > 0:
            agent_name = script_path.parts[hooks_idx - 1]

    # 実行ファイル名とコマンドライン引数の取得
    file_name = script_path.name
    args = sys.argv[1:]

    # ログエントリの生成と追記
    log_line = f"[{time_str}] Agent: {agent_name} | File: {file_name} | Args: {args}\n"
    
    with log_file.open('a', encoding='utf-8') as f:
        f.write(log_line)
